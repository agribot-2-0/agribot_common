The standard.rc file contains the standard, unmodified pylint convention

pylint is using .pylintrc file to read current configuration, like disabled warining types and maximal line length. You may modify this file, current modifications (differences from standard.rc) for Agribot projects are:

- disabling: missing-docstring
- dis-disabling: invalid-name
- changing file_name_convention to 'any', for the rest (variables, methods etc) it is still snake_case


HOW TO:
Configuration is read from the directory where pylint was started, so to check your files using Agribot configuration,
you must do it from the pylint_conf directory. Then write for example

pylint ../../agribot_commander/scripts/*.py
