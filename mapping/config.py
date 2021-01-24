# -*- coding: utf-8 -*-
import os
import optparse
import codecs
import errno

from ConfigParser import SafeConfigParser
from multiprocessing import cpu_count

from export import EXPORT_FUNCTIONS

DEFAULT_CPU_LIMIT = cpu_count() - 2 if cpu_count() > 2 else 1


class OptionNotFound(Exception):
    def __init__(self, msg, *args, **kwargs):
        msg = 'Option ' + msg + ' not found'
        super(OptionNotFound, self).__init__(msg, *args, **kwargs)


class ConfigFileParser(SafeConfigParser):
    def getlist(self, section, option, sep=','):
        value = self.get(section, option)
        return string_to_list(value, sep)

    def getdict(self, section, option, sep=',', sym=':'):
        value = self.get(section, option)
        return string_to_dict(value, sep, sym)

    def getlistint(self, section, option, sep=','):
        return [int(x) for x in self.getlist(section, option, sep)]

    def getdirpath(self, section, option):
        path = self.get(section, option)
        if os.path.isdir(path):
            return path
        else:
            raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)

    def getfilepath(self, section, option):
        path = self.get(section, option)
        if os.path.isfile(path):
            return path
        else:
            raise OSError(errno.ENOENT, os.strerror(errno.ENOENT), path)


def remove_whitespace(s):
    from string import whitespace as ws
    return filter(lambda c: c not in ws, s)


def string_to_list(s, sep=','):
    if s == '':
        return list()
    if sep in s:
        return remove_whitespace(s).split(sep)
    else:
        l = []
        l.append(s.strip())
        return l


def string_to_dict(s, sep=',', sym=':'):
    if s == '':
        return dict()
    if not sym in s:
        raise ValueError('Provided argument is not of "key{0}: value" type'.format(sym))

    dic = {}

    for p in string_to_list(s):
        try:
            key, value = p.split(sym)
        except ValueError:
            raise ValueError(str(p) + ' is not a "key: value" argument')

        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                pass

        dic[key] = value

    return dic


def load_config_from_file(path):
    parser = ConfigFileParser()

    with codecs.open(path, 'r', encoding='utf-8') as f:
        parser.readfp(f)

    return parser


def parse_cli(sys_args):

    def keywords_callback(option, opt, value, parser):
        setattr(parser.values, option.dest, string_to_list(value))

    def export_params_callback(option, opt, value, parser):
        setattr(parser.values, option.dest, string_to_dict(value))

    def file_config_callback(option, opt, value, parser):

        file_config = load_config_from_file(value)

        parser.values.input_folder = file_config.get('GENERAL', 'input_folder')
        parser.values.output_folder = file_config.get('GENERAL', 'output_folder')
        parser.values.output_type = file_config.get('GENERAL', 'output_type')

        parser.values.overwrite = file_config.getboolean('GENERAL', 'overwrite')
        parser.values.cpu_limit = file_config.getint('GENERAL', 'cpu_limit')

        parser.values.export_params = file_config.getdict('GENERAL', 'export_params')

        parser.values.filename_pattern = file_config.get('FILTERS', 'filename_pattern')
        parser.values.keywords = file_config.getlist('FILTERS', 'keywords')

    parser = optparse.OptionParser(usage='%prog [options] <arg1> <arg2> [<arg3>...]')

    parser.add_option('-i', '--input',
                      action="store",
                      dest="input_folder",
                      help='Folder with mxd files')
    parser.add_option('-o', '--output',
                      action="store",
                      dest="output_folder",
                      help='Output folder')
    parser.add_option('-t', '--file_type',
                      action="store",
                      dest="output_type",
                      type='choice',
                      default='pdf',
                      choices=EXPORT_FUNCTIONS.keys(),
                      help='Output file types')
    parser.add_option('-w', '--overwrite',
                      action='store_true',
                      dest='overwrite',
                      default=False,
                      help='Overwrite output files')
    parser.add_option('--cpu',
                      action="store",
                      dest="cpu_limit",
                      type='int',
                      default=DEFAULT_CPU_LIMIT,
                      help='Number of used process')
    parser.add_option('--export_params',
                      action="callback",
                      callback=export_params_callback,
                      dest="export_params",
                      type="str",
                      help='Image file parameters. Eg. --export_params resolution:300,tiff_compression:LZW \
                            More details in ESRI arcpy docs')
    parser.add_option('--config',
                      action="callback",
                      callback=file_config_callback,
                      dest="config_file",
                      type="str",
                      help='Config file path')

    filters_opts = optparse.OptionGroup(parser,
                            'Mxd folder filtering options'
                            )
    filters_opts.add_option('-p', '--pattern',
                            action="store",
                            dest="filename_pattern",
                            default='*',
                            help='Filename filter. Eg. -p N34058*')
    filters_opts.add_option('-k', '--keywords',
                            action="callback",
                            callback=keywords_callback,
                            dest="keywords",
                            type='str',
                            help='Keywords based filename search. Eg. -k N34058Ad3,N34058Ad2,N33102Bd1')

    parser.add_option_group(filters_opts)

    if sys_args:
        return parser.parse_args(sys_args)
    else:
        parser.print_help()
        exit(2)


def validate_options(opts):
    if opts.input_folder:
        if not os.path.isdir(opts.input_folder):
            raise OSError(opts.input_folder + ' <- source folder does not exist')
    else:
        raise OptionNotFound('input_folder')

    if opts.output_folder:
        if not os.path.isabs(opts.output_folder):
            raise OSError(opts.output_folder + ' <- incorrect output folder path')
    else:
        raise OptionNotFound('output_folder')

    if opts.output_type:
        if not opts.output_type in EXPORT_FUNCTIONS.keys():
            raise Exception(str(opts.output_type) + ' <- incorrect file type')
    else:
        raise Exception('output file format not defined')

    if opts.cpu_limit:
        if not isinstance(opts.cpu_limit, int):
            raise TypeError('cpu_lmit must be an integer')
        if opts.cpu_limit > cpu_count():
            raise ValueError('Insufficient number of CPU cores')
    else:
        raise Exception('cpu_limit was not defined')

    if opts.filename_pattern:
        if not isinstance(opts.filename_pattern, basestring):
            raise TypeError('filename_pattern must be a string')
        if '*' not in opts.filename_pattern:
            raise ValueError('no "*" in filename_pattern')

    if opts.keywords:
        if not isinstance(opts.keywords, (list, tuple)):
            raise TypeError('keywords must be a list or a tuple')
        for word in opts.keywords:
            if not isinstance(word, basestring):
                raise TypeError('one or more keywords is not of string type')

    if opts.export_params:
        if not isinstance(opts.export_params, dict):
            raise TypeError('export_params must be a dictionary')
