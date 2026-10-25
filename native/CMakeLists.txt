cmake_minimum_required(VERSION 3.21)

project(
    CacheMind
    VERSION 0.1.0
    LANGUAGES CXX
)

# --------------------------------------------------
# C++20 executable
# --------------------------------------------------

add_executable(
    cachemind-native-smoke
    src/smoke.cpp
)

# --------------------------------------------------
# Language standard
# --------------------------------------------------

set_target_properties(
    cachemind-native-smoke
    PROPERTIES
    CXX_STANDARD 20
    CXX_STANDARD_REQUIRED ON
    CXX_EXTENSIONS OFF
)

# --------------------------------------------------
# Compiler diagnostics
# --------------------------------------------------

if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    target_compile_options(
        cachemind-native-smoke
        PRIVATE
        -Wall
        -Wextra
        -Wpedantic
    )
endif()

# --------------------------------------------------
# Automated testing
# --------------------------------------------------

include(CTest)

if(BUILD_TESTING)
    add_test(
        NAME native_smoke
        COMMAND $<TARGET_FILE:cachemind-native-smoke>
    )
endif()