cmake_minimum_required(VERSION 3.21)

project(
    CacheMind
    VERSION 0.1.0
    LANGUAGES CXX
)

# ------------------------------------------
# Native C++20 smoke executable
# ------------------------------------------

add_executable(
    cachemind-native-smoke
    src/smoke.cpp
)

# ------------------------------------------
# C++ standard configuration
# ------------------------------------------

set_target_properties(
    cachemind-native-smoke
    PROPERTIES
    CXX_STANDARD 20
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
)

# ------------------------------------------
# GCC compiler diagnostics
# ------------------------------------------

if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    target_compile_options(
        cachemind-native-smoke
        PRIVATE
        -Wall
        -Wextra
        -Wpedantic
    )
endif()