## ! DO NOT MANUALLY INVOKE THIS setup.py, USE CATKIN INSTEAD

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

# fetch values from package.xml
SETUP_ARGS = generate_distutils_setup(packages=[
    'agribot_common', 'agribot_common.database', 'agribot_common.logs_backup',
    'agribot_common.tools.imu_calibration', 'agribot_common.tools.imu_mag_postprocessing',
    'agribot_common.tools.imu_scripts', 'agribot_common.tools.log_and_plot',
    'agribot_common.tools.mag_calibration', 'agribot_common.tools.rosbag_live',
    'agribot_common.tools.rosbag_postprocessing', 'agribot_common.tools.rosbag_viewer'
],
                                      package_dir={'': 'scripts'})

setup(**SETUP_ARGS)
