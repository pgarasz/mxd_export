# -*- coding: utf-8 -*-
import sys
import arcpy.mapping

from utils import ArcPyOpenMXD as open_mxd


DEFAULT_PARAMETERS = {'png':  {'resolution': 300},
                      'jpg':  {'resolution': 300},
                      'pdf':  {'resolution': 300},
                      'tiff': {'resolution': 300},
                      'gtiff':{'resolution': 300,
                               'geoTIFF_tags': True},
                      }


def to_png(mxd_path, output, semaphor, params):
    """Exports mxd to png

    Export parameters help
    http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/ExportToPNG/00s30000002s000000/
    """
    if not params:
        params = DEFAULT_PARAMETERS['png']

    with open_mxd(mxd_path) as mxd:

        arcpy.mapping.ExportToPNG(mxd, output, **params)
        sys.stdout.flush()
        semaphor.release()


def to_jpg(mxd_path, output, semaphor, params):
    """Exports mxd to jpg

    Export parameters help
    http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/ExportToJPEG/00s300000038000000/
    """
    if not params:
        params = DEFAULT_PARAMETERS['jpg']

    with open_mxd(mxd_path) as mxd:

        arcpy.mapping.ExportToJPEG(mxd, output, **params)
        sys.stdout.flush()
        semaphor.release()


def to_tiff(mxd_path, output, semaphor, params):
    """Exports mxd to tiff

    Export parameters help
    http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/ExportToTIFF/00s300000009000000/
    """
    if not params:
        params = DEFAULT_PARAMETERS['tiff']

    with open_mxd(mxd_path) as mxd:

        arcpy.mapping.ExportToTIFF(mxd, output, **params)
        sys.stdout.flush()


def to_gtiff(mxd_path, output, semaphor, params):
    """Exports mxd to gtiff

    Export parameters help
    http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/ExportToTIFF/00s300000009000000/
    """
    if not params:
        params = DEFAULT_PARAMETERS['gtiff']

    with open_mxd(mxd_path) as mxd:

        arcpy.mapping.ExportToTIFF(mxd, output, **params)
        sys.stdout.flush()
        semaphor.release()


def to_pdf(mxd_path, output, semaphor, params):
    """Exports mxd to pdf

    Export parameters help
    http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/ExportToPDF/00s300000027000000/
    """
    if not params:
        params = DEFAULT_PARAMETERS['pdf']

    with open_mxd(mxd_path) as mxd:
        arcpy.mapping.ExportToPDF(mxd, output, **params)
        sys.stdout.flush()
        semaphor.release()


EXPORT_FUNCTIONS = {'png':  [to_png, 'png'],
                    'jpg':  [to_jpg, 'jpg'],
                    'pdf':  [to_pdf, 'pdf'],
                    'tiff': [to_tiff, 'tiff'],
                    'gtiff': [to_gtiff, 'gtiff']
                    }
