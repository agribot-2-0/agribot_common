# Magnetometer calibration scripts
Both scripts (online and offline) save calibration parameters to YAML files:
- mag_bias_from_bag.yaml (offline calibration)
- mag_bias_online.yaml (online calibration)

Base class for online and offline calibration: `mag/magnetometer_calibration.py`


### **Node for online magnetometer calibration: mag/magnetometer_calibration_online.py**

- Optional arguments

  | Flag  | Meaning                                                                                 | Default value                     |
  |-------|-----------------------------------------------------------------------------------------|-----------------------------------|
  | `-t`  | Magnetometer topic                                                                      | /agribot/imu/raw/mag              |
  | `-m`  | Magnetometer magnitude                                                                  | 4.9714e-5 (magnitude for Wrocław) |
  | `-pp` | Path to YAML file with previous parameters (if data was collected with non-zero params) | -                                 |

### **Script for offline magnetometer calibration: mag/magnetometer_calibration_from_bag.py**

- Required arguments

  | Flag | Meaning           | Default value |
  |------|-------------------|---------------|
  | `-i` | Path to input bag | -             |

- Optional arguments

  | Flag  | Meaning                                                                                 | Default value                     |
  |-------|-----------------------------------------------------------------------------------------|-----------------------------------|
  | `-t`  | Magnetometer topic                                                                      | /agribot/imu/raw/mag              |
  | `-m`  | Magnetometer magnitude                                                                  | 4.9714e-5 (magnitude for Wrocław) |
  | `-pp` | Path to YAML file with previous parameters (if data was collected with non-zero params) | -                                 |

### mag/magnetometer_z_calibration_from_bag.py

- Required arguments

  | Flag | Meaning           | Default value |
  |------|-------------------|---------------|
  | `-i` | Path to input bag | -             |

- Optional arguments

  | Flag | Meaning                          | Default value                            |
  |------|----------------------------------|------------------------------------------|
  | `-t` | Magnetometer topic               | /agribot/imu/raw/mag                     |
  | `-m` | Magnetometer magnitude in Z axis | 4.5804e-5 (Z axis magnitude for Wrocław) |

---

# Auxiliary magnetometer scripts

### Script to remove magnetometer outliers points from bag: mag/magnetometer_calibration_remove_outliers_from_bag.py

- Required arguments

  | Flag | Meaning            | Default value |
  |------|--------------------|---------------|
  | `-i` | Path to input bag  | -             |
  | `-o` | Path to output bag | -             |

- Optional arguments

  | Flag | Meaning                                                                  | Default value        |
  |------|--------------------------------------------------------------------------|----------------------|
  | `-t` | Magnetometer topic                                                       | /agribot/imu/raw/mag |
  | `-r` | Radius used in neighbors count                                           | 1.0e-6               |
  | `-n` | Minimal number of neighbors in radius required to qualify as valid point | 10                   |

### Script to plot magnetometer XYZ data from bag: mag/magnetometer_plot_from_bag.py

- Required arguments

  | Flag | Meaning           | Default value |
  |------|-------------------|---------------|
  | `-i` | Path to input bag | -             |

- Optional arguments

  | Flag | Meaning            | Default value        |
  |------|--------------------|----------------------|
  | `-t` | Magnetometer topic | /agribot/imu/raw/mag |

### Script to plot magnetometer XYZ data from 2 bags: mag/magnetometer_comparison_plot_from_2_bags.py

- Required arguments

  | Flag  | Meaning                  | Default value |
  |-------|--------------------------|---------------|
  | `-i1` | Path to first input bag  | -             |
  | `-i2` | Path to second input bag | -             |

- Optional arguments

  | Flag | Meaning            | Default value        |
  |------|--------------------|----------------------|
  | `-t` | Magnetometer topic | /agribot/imu/raw/mag |
