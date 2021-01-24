# -*- coding: utf-8 -*-
import os
import glob
import logging
import arcpy


logger = logging.getLogger(__name__)


class FileNotFoundError(Exception):
    pass


class ArcPyOpenMXD:
    """Context manager for opening mxd"""

    def __init__(self, path):
        if os.path.isfile(path):
            self.path = path
        else:
            raise FileNotFoundError(u'File not found ' + str(path))

    def __enter__(self):
        self.mxd = arcpy.mapping.MapDocument(self.path)
        return self.mxd

    def __exit__(self, *args):
        del self.mxd


def _exit_with_error(msg):
    logger.error(msg)
    raw_input('Press Enter to close')
    exit(1)


def make_file_paths_list(dir_path, extension, filename_pattern='*'):
    """Returns a list of paths to files in a folder"""

    file_search_pattern = filename_pattern + '.' + extension

    logger.info('\n' + 'Looking for "{0}" files in {1} folder'.format(file_search_pattern, dir_path))

    if not os.path.isdir(dir_path):
        _exit_with_error(' [ ERROR! ] Folder does not exist')

    file_paths_list = glob.glob(os.path.join(dir_path, file_search_pattern))

    if len(file_paths_list) != 0:
        logger.info(' Number of files found: {1}'.format(file_search_pattern, len(file_paths_list)))
        return sorted(file_paths_list)
    else:
        _exit_with_error(' [ ERROR! ] There are no "{0}" files in the folder'.format(file_search_pattern))
