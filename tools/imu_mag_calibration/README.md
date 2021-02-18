## IMU (accelerometer + gyroscope) calibration scripts:
  ### Base class: `imu/imu_calibration.py`
  
  ### **Node for online calibration: `imu/imu_calibration_online.py`**
  - Optional arguments

    | Flag | Meaning   | Default value         |
    |------|-----------|-----------------------|
    | -t   | IMU topic | /agribot/imu/raw/data |

  ### **Program for offline calibration from bag: `imu/imu_calibration_from_bag.py`**
  - Required arguments

    | Flag |           Meaning | Default value |
    |------|------------------:|---------------|
    | -i   | Path to input bag | -             |

  - Optional arguments

    | Flag | Meaning   | Default value         |
    |------|-----------|-----------------------|
    | -t   | IMU topic | /agribot/imu/raw/data |

---

## Magnetometer calibration scripts:
  - Base class: `imu/imu_calibration.py`
  - **Node for online calibration: `imu/imu_calibration_online.py`**
  - **Program for offline calibration from bag: `imu/imu_calibration_from_bag.py`**
