cmake_minimum_required(VERSION 2.8)

project(cpp_client)

string(TIMESTAMP VERSION "%Y%m%d")
message ("VERSION: " ${VERSION})

# SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -O3 -Wall ")
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -g -Wall ")
message ("cxx Flags: " ${CMAKE_CXX_FLAGS})

include_directories("/usr/include/google/protobuf")
include_directories("/usr/local/include/grpc/")

file( GLOB APP_SOURCES "*.cpp" "*.cc" )
add_executable( client_main ${APP_SOURCES} )
target_link_libraries( client_main pthread grpc++ protobuf)
