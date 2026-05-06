CMAKE_MINIMUM_REQUIRED(VERSION 3.22)

SET(UPSTREAM_VERSION "3.7.11")
SET(PACKAGE_VERSION  "1")

PROJECT("org.gmplib-gmp"
  VERSION "${UPSTREAM_VERSION}.${PACKAGE_VERSION}"
)

INCLUDE(cmake/version.cmake)
INCLUDE(cmake/platform.cmake)
MESSAGE("Building for: ${JONCHKI_PLATFORM}")

# Python is needed for the hash and patch tool.
FIND_PACKAGE(Python3 REQUIRED COMPONENTS Interpreter)
SET(PYTHON_EXECUTABLE "${Python3_EXECUTABLE}")

# Set some installation folders.
INCLUDE(cmake/muhkuh_installation_folders.cmake)

OPTION(BUILDCFG_ONLY_JONCHKI_CFG "Build only the jonchki configuration. This is used for the resolve phase. The default is OFF."
       "OFF")

ADD_SUBDIRECTORY(gnutls)
