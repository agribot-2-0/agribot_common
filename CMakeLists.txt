cmake_minimum_required(VERSION 2.8.3)
project(agribot_common)
add_compile_options(-std=c++17 -Wall -Wextra -pedantic -Werror)

find_package(catkin REQUIRED COMPONENTS
roscpp
std_msgs
std_srvs
)

catkin_python_setup()

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES ${PROJECT_NAME} agribot_common agribot_connection
  CATKIN_DEPENDS 
  roscpp
  std_msgs
  std_srvs
)

###########
## Build ##
###########
include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)
link_directories(
  ${PROJECT_SOURCE_DIR}
)

add_library(agribot_common src/Can.cpp src/CanFrame.cpp)

add_library(agribot_connection
  src/connection/buffer/Buffer.cpp
  src/connection/parsing_strategy/LsbFirstParsingStrategy.cpp
  src/connection/parsing_strategy/MsbFirstParsingStrategy.cpp
  src/connection/socket/TcpSocket.cpp
)

add_executable(performance_indices_node src/performance_indices/performance_indices_node.cpp src/performance_indices/PerformanceIndices.cpp)
target_link_libraries(performance_indices_node ${catkin_LIBRARIES})
add_dependencies(performance_indices_node ${catkin_EXPORTED_TARGETS})

#############
## Install ##
#############

install(TARGETS agribot_common agribot_connection performance_indices_node
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

install(DIRECTORY launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  PATTERN ".svn" EXCLUDE
)

install(PROGRAMS
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

#############
## Testing ##
#############

if (CATKIN_ENABLE_TESTING)
  catkin_add_gtest(connection-test 
    test/connection_test.cpp
    src/connection/parsing_strategy/LsbFirstParsingStrategy.cpp
    src/connection/parsing_strategy/MsbFirstParsingStrategy.cpp
  )
  target_link_libraries(connection-test ${catkin_LIBRARIES} gtest)
endif()
