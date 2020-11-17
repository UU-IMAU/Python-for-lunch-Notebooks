set_property(SOURCE knn_swig.i PROPERTY CPLUSPLUS ON)
set_property(SOURCE knn_swig.i PROPERTY SWIG_MODULE_NAME knn_swig_py)
swig_add_library(knn_swig_py
  TYPE SHARED
  LANGUAGE python
  OUTPUT_DIR ${CMAKE_BINARY_DIR}/python/${PROJECT_NAME}
  SOURCES knn_swig.i)

target_include_directories(knn_swig_py
  PRIVATE
  ../include
  ${Python_INCLUDE_DIRS}
  )
set_property(TARGET knn_swig_py PROPERTY SWIG_USE_TARGET_INCLUDE_DIRECTORIES ON)

# note: macOS is APPLE and also UNIX !
if(APPLE)
  set_target_properties(knn_swig_py PROPERTIES
    SUFFIX ".so"
    INSTALL_RPATH "@loader_path;@loader_path/../../${PROJECT_NAME}/.libs"
    )
  set_property(TARGET knn_swig_py APPEND PROPERTY
    LINK_FLAGS "-flat_namespace -undefined suppress"
    )
elseif(UNIX)
  set_target_properties(knn_swig_py PROPERTIES
    INSTALL_RPATH "$ORIGIN:$ORIGIN/../../${PROJECT_NAME}/.libs"
    )
endif()
target_link_libraries(knn_swig_py PRIVATE knn_swig)

# Variable PYTHON_LIBRARIES can contains keyword `optimized`
# which won't be interpreted inside a generator expression.
# i.e. we can't use: $<$<PLATFORM_ID:Windows>:${PYTHON_LIBRARIES}>
# see: https://cmake.org/cmake/help/git-stage/command/target_link_libraries.html#command:target_link_libraries
if(MSVC)
  target_link_libraries(knn_swig_py PRIVATE ${Python_LIBRARIES})
endif()
