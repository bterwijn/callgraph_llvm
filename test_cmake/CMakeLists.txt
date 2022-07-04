cmake_minimum_required(VERSION 3.10)

# set the project name
project(Tutorial)

# add the executable
add_library(lib SHARED lib/lib.cpp)
target_include_directories(lib PUBLIC
  "${PROJECT_SOURCE_DIR}/lib")

# add the llvm target
get_target_property(lib_includes lib INCLUDE_DIRECTORIES)
add_custom_target(lib.llvm ALL
  COMMAND clang++ -w -I ${lib_includes} -S -emit-llvm lib/lib.cpp -o lib/lib.llvm
  DEPENDS lib/lib.llvm
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  COMMENT "building LLVM ${CMAKE_CURRENT_SOURCE_DIR}"
  )

# add the executable
add_executable(main main.cpp)
target_link_libraries(main PUBLIC lib)
target_include_directories(main PUBLIC
  "${PROJECT_SOURCE_DIR}/lib"
  )
   
# add the llvm target
get_target_property(main_includes main INCLUDE_DIRECTORIES)
add_custom_target(main.llvm ALL
  COMMAND clang++ -w -I ${main_includes} -S -emit-llvm main.cpp -o main.llvm
  DEPENDS main.cpp
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
  COMMENT "building LLVM ${main_includes}"
  )
