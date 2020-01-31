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

## Mark cpp header files for installation
install(DIRECTORY include/${PROJECT_NAME}/
  DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
  FILES_MATCHING PATTERN "*.h"
  PATTERN ".svn" EXCLUDE
)

#############
## Testing ##
#############
