# Postprocessing scripts

### Script to rewrite bag with stationary values for IMU and/or magnetometer: postprocessing/rewrite_imu_and_mag_stationary_from_bag.py
Script useful to test Madgwick/Kalman filter simulating noiseless behavior of one (or both) of the sensors:

- if `-rewrite_imu` is set to true, sensor_msgs/Imu is rewritten with:
    - 0.0 for all angular velocities
    - 0.0 for accelerations in x and y axis
    - 9.807 for accelerations in z axis
- if `-rewrite_mag` is set to true, sensor_msgs/MagneticField is rewritten with mean value of magnetic field  
  
---

- Required arguments

  | Flag | Meaning            | Default value |
  |------|--------------------|---------------|
  | `-i` | Path to input bag  | -             |
  | `-o` | Path to output bag | -             |

- Optional arguments

  | Flag           | Meaning                                 | Default value         |
  |----------------|-----------------------------------------|-----------------------|
  | `-imu_topic`   | IMU topic                               | /agribot/imu/raw/data |
  | `-mag_topic`   | Magnetometer topic                      | /agribot/imu/raw/mag  |
  | `-rewrite_imu` | Rewrite IMU data as stationary          | true                  |
  | `-rewrite_mag` | Rewrite magnetometer data as stationary | true                  |
