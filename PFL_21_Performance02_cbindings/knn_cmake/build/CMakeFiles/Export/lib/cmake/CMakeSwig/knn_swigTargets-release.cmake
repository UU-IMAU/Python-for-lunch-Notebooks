#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "knn_swig" for configuration "Release"
set_property(TARGET knn_swig APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(knn_swig PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libknn_swig.so.1.0"
  IMPORTED_SONAME_RELEASE "libknn_swig.so.1.0"
  )

list(APPEND _IMPORT_CHECK_TARGETS knn_swig )
list(APPEND _IMPORT_CHECK_FILES_FOR_knn_swig "${_IMPORT_PREFIX}/lib/libknn_swig.so.1.0" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
