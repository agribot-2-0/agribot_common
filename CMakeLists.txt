cmake_minimum_required(VERSION 2.8.3)
project(agribot_common)
add_compile_options(-std=c++17 -Wall -Wextra -pedantic -Werror)

find_package(catkin REQUIRED)

catkin_python_setup()

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES ${PROJECT_NAME} agribot_common
)

###########
## Build ##
###########
include_directories(include/)
add_library(agribot_common src/Can.cpp src/CanFrame.cpp)

include_directories(include/agribot_common/connection)
add_library(agribot_connection
  src/connection/Buffer.cpp
  src/connection/IFrame.cpp
  src/connection/IParser.cpp
  src/connection/LsbFirstParsingStrategy.cpp
  src/connection/MsbFirstParsingStrategy.cpp
  src/connection/TcpSocket.cpp
)

#############
## Install ##
#############

install(TARGETS agribot_common agribot_connection
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

install(PROGRAMS
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

#############
## Testing ##
#############
