cmake_minimum_required(VERSION 2.8.3)
project(agribot_common)

find_package(catkin REQUIRED)

catkin_package(
  LIBRARIES ${PROJECT_NAME} agribot_common
)

###########
## Build ##
###########
include_directories(include/)
add_library(agribot_common src/Can.cpp)

#############
## Install ##
#############

install(TARGETS agribot_common
    ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
    LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
    RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

## Mark cpp header files for installation
install(DIRECTORY include/${PROJECT_NAME}/
  DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
  FILES_MATCHING PATTERN "*.h"
  PATTERN ".svn" EXCLUDE
)

#############
## Testing ##
#############
