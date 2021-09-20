# MXD EXPORT

## DESCRIPTION
Mxd export is a command-line application that uses parallel processing for exporting ESRI ArcMap files (mxd) to different image formats (tif, jpg, pdf, png).

## CONFIG
Config is based on a command-line interface and/or text config files. Both ways can be used independently or mixed together.

### COMMAND-LINE INTERFACE (CLI)

Run cmd.exe in your Windows OS. Navigate to folder containing the app. If you have ArcGIS 10.0 Python in your system path you can just run it by writing 'mxd_export.py' along with required parameters. Otherwise you need to precede it with the path to 'python.exe' installed with ArcGIS 10.0.

For example:

    mxd_export.py -i C:\SOURCE_MXD -o C:\OUTPUT\PDF -t pdf
    mxd_export.py -i C:\SOURCE_MXD -o C:\OUTPUT\TIF -t tiff --cpu 4 --keywords N33102Ab1,N33102Ab2 -w

#### Parameters

List of optional and required parameters:

| short |        long         | optional |              description              |
| ----- | ------------------- | :------: | ------------------------------------- |
|  -h   | --help              |   ---    | displays help                         |
|  -i   | --input             |          | path to folder containing mxd files   |
|  -o   | --output            |          | output folder path                    |
|  -t   | --file_type         |          | output file type                      |
|  -w   | --overwrite         |   YES    | overwrite output files                |
|       | --cpu               |   YES    | number of simultaneous processes      |
|       | --export_parameters |   YES    | parameters for image files export     |
|       | --config            |   YES    | config file path                      |
| filtering |
|  -p   | --pattern           |   YES    | filename filter pattern eg. N34058*   |
|  -k   | --keywords          |   YES    | keywords based filename filter<br>eg. -k N34058Ad3,N34058Ad2 |

### CONFIG FILE

Mxd export can be configured through text files. This is a convenient and preferred way.

Use CLI `--config` parameter with the path to your config file.

    mxd_export.py --config config\myconfig.conf

You can base your configs on a template:

    config\template.conf

There are three sections of parameters inside the file - `[GENERAL] [FILTERS]` and a special group `[DEFAULT]`.

It is required that you provide `input_folder`, `output_folder`, `output_type` parameters in `[GENERAL]` section. Values for the rest will be taken from the `[DEFAULT]` section. If you want to overwrite the defaults, you can also add those parameters to `[GENERAL]` with new values. Notice that `filename_pattern` and `keywords` go to `[FILTERS]`.

To temporarily deactivate parameters precede them with `#` sign:

    #keywords = N34050Ca2_RS, N34061Da3, N33095Bb3

### MIXED CONFIG

If you chose to load your config from a text file, you are still allowed to add more parameters through CLI that will overwrite those inside the config file. This way allows you to have template config in the file and change some parameters on the fly. Here are some examples:

    mxd_export.py --config config\template_jpg.conf -o D:\new_jpgs
    mxd_export.py --config config\template_jpg.conf -o D:\selected_jpgs -p N33102*

**IMPORTANT!**
Additional CLI parameters take precedence over text file config **only** if `--config` is the first one.

### ADDITIONAL INFO

#### file_type

List of available image formats:

- png, jpg, pdf, tiff, gtiff

#### CPU

By  default the application detects the max number of available CPU cores and uses 2 less. One will be used if your PC has only one or two cores.

You can overwrite this with your own values. The application will return an error if you exceed the max number of available CPU cores.

#### export_parameters

For each image format there's a separate set of export parameters. Check [ESRI's docs](http://help.arcgis.com/en/arcgisdesktop/10.0/help/index.html#/ExportToTIFF/00s300000009000000/) for details.

You can provide those parameters as key:value pairs separated with a comma (no space).

    --export_params resolution:300,tiff_compression:LZW

Without using `--export_params` all setting are set to their default values as stated in ARGIS 10.0 docs with the exception of `resolution`. This is by default set to `resolution:300`.

## REQUIREMENTS

ArcGIS 10.0, Python 2.6.5

## AUTHOR

Przemek Garasz
