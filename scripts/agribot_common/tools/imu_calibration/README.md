# IMU (accelerometer + gyroscope) calibration scripts
Both scripts (online and offline) save calibration parameters to YAML files:
- imu_bias_from_bag.yaml (offline calibration)
- imu_bias_online.yaml (online calibration)

Base class for online and offline calibration: `imu/imu_calibration.py`


### **Node for online IMU calibration: imu/imu_calibration_online.py**

- Optional arguments

  | Flag | Meaning   | Default value         |
  |------|-----------|-----------------------|
  | `-t` | IMU topic | /agribot/imu/raw/data |

### **Script for offline IMU calibration: imu/imu_calibration_from_bag.py**

- Required arguments

  | Flag | Meaning           | Default value |
  |------|-------------------|---------------|
  | `-i` | Path to input bag | -             |

- Optional arguments

  | Flag | Meaning   | Default value         |
  |------|-----------|-----------------------|
  | `-t` | IMU topic | /agribot/imu/raw/data |
