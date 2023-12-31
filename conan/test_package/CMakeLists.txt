cmake_minimum_required(VERSION 3.15)
project(bgfx_test)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)


find_package( bgfx CONFIG REQUIRED)

add_executable(bgfx_test bgfx_test.cpp)
target_link_libraries( bgfx_test bgfx::bgfx )
