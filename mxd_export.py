# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------------------------
# name:      map_export
# author:    Przemek Garasz
# version:   2.0.2
# desc:      Multiprocessing ArcGIS mxd files export to image formats
# -------------------------------------------------------------------------------------------

import os
import sys
import pickle
import optparse
import datetime
import multiprocessing

import logging
import logging.config

from mapping.export import EXPORT_FUNCTIONS, DEFAULT_PARAMETERS
from mapping.config import parse_cli, load_config_from_file, validate_options, DEFAULT_CPU_LIMIT
from mapping.utils import make_file_paths_list


if __name__ == '__main__':

    # logger config ------------------------------------------------------

    logpath = os.path.splitext(os.path.basename(__file__))[0] + '.log'
    logging.config.fileConfig("config\logging.conf",
                              defaults={'logpath': logpath},
                              disable_existing_loggers=False)
    multiprocessing.log_to_stderr(logging.ERROR)

    # config -------------------------------------------------------------

    opts, args = parse_cli(sys.argv[1:])

    input_folder = opts.input_folder
    output_folder = opts.output_folder
    output_type = opts.output_type

    overwrite = opts.overwrite
    cpu_limit = opts.cpu_limit

    filename_pattern = opts.filename_pattern
    keyword_filters = opts.keywords

    export_params = opts.export_params

    if not cpu_limit:
        cpu_limit = DEFAULT_CPU_LIMIT
    if not filename_pattern:
        filename_pattern = '*'
    if not export_params:
        export_params = DEFAULT_PARAMETERS[output_type]

    validate_options(opts)

    # main ---------------------------------------------------------------

    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    mxd_paths = make_file_paths_list(input_folder, 'mxd', filename_pattern)

    if keyword_filters:
        mxd_paths = [path for path in mxd_paths if any(kw in path for kw in keyword_filters if kw)]
        logging.info(' Filtered files: {0}'.format(len(mxd_paths)))
        print

    total = len(mxd_paths)

    jobs = []
    sema = multiprocessing.Semaphore(cpu_limit)

    logging.info('\n' + 'Exporting' + '\n')
    start_time = datetime.datetime.now()

    for i, path in enumerate(mxd_paths):

        mxd_basename = os.path.basename(path)
        output = os.path.join(output_folder, mxd_basename.replace('mxd', EXPORT_FUNCTIONS[output_type][1]))

        if not overwrite:
            if os.path.exists(output):
                logging.warning('[   EXISTS   ] {0}  ({1} z {2})'.format(mxd_basename, i+1, total))
                continue

        sema.acquire()

        args = (path, output, sema, export_params)

        logging.info('[  SAVING  ] {0}  ({1} z {2})'.format(mxd_basename, i+1, total))
        p = multiprocessing.Process(name=mxd_basename,
                                    target=EXPORT_FUNCTIONS[output_type][0],
                                    args=args
      )
        jobs.append(p)
        p.start()

    for j in jobs:
        j.join()

        if j.exitcode <> 0:
            logging.error(('[   !!!ERROR!!!    ] {0} exitcode = {1} '.format(j.name, j.exitcode)))

    print '\n' + 'SUMMARY:'
    print '\n' + 'Elapsed time: {0}'.format(datetime.datetime.now() - start_time)
    print

    raw_input('Press Enter to close')
