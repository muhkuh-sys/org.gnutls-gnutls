INCLUDE(ExternalProject)

# Get the VCS version for the jonchki configuration.
INCLUDE(${CMAKE_HOME_DIRECTORY}/cmake/version.cmake)

# Filter the jonchki configuration.
CONFIGURE_FILE(installer/gnutls.xml
               ${CMAKE_BINARY_DIR}/gnutls-${PROJECT_VERSION}.xml
               @ONLY)

#----------------------------------------------------------------------------
#
# Build the project.
#
IF((${BUILDCFG_ONLY_JONCHKI_CFG} STREQUAL "OFF"))
	SET(GMP_INCLUDE "${CMAKE_BINARY_DIR}/build_requirements/jonchki/install/dev/include")
	SET(GMP_LIBS "${CMAKE_BINARY_DIR}/build_requirements/jonchki/install/dev/lib")

	SET(ZLIB_PREFIX "${CMAKE_BINARY_DIR}/build_requirements/jonchki/install/dev")
	SET(PKGCONFIG_JONCHKI "${CMAKE_CURRENT_BINARY_DIR}/../build_requirements/jonchki/install/dev/pkgconfig")

# Is this still necessary without 32bit builds?
#	# Set the host even if not cross compiling.
#	# Otherwise GNUTLS detects the CPU and tries to build with special
#	# support for it. In the first place this sounds very nice. But it
#	# fails on a 32bit OS running on a 64bit CPU - which is the case for
#	# Docker 32bit images.
#	IF(CMAKE_SYSTEM_NAME STREQUAL "Linux")
#		IF(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
#			SET(CONFIGURE_HOST "${JONCHKI_PLATFORM_CPU_ARCH}-pc-linux-gnu")
#		ELSE(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
#			MESSAGE(FATAL_ERROR "Trying to detect the system with a non-GCC compiler. This is currently not supported.")
#		ENDIF(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
#	ELSE(CMAKE_SYSTEM_NAME STREQUAL "Linux")
#		MESSAGE(FATAL_ERROR "Trying to detect the system on a non-linux OS. This is currently not supported.")
#	ENDIF(CMAKE_SYSTEM_NAME STREQUAL "Linux")

	MESSAGE("LIBGMP_INCLUDE_DIR: ${LIBGMP_INCLUDE_DIR}")
	MESSAGE("LIBGMP_LIBRARY: ${LIBGMP_LIBRARY}")
	MESSAGE("LIBNETTLE_PREFIX: ${LIBNETTLE_PREFIX}")
	ExternalProject_Add(TARGET_gnutls
	                    PREFIX ${CMAKE_CURRENT_BINARY_DIR}/gnutls
	                    URL ${CMAKE_CURRENT_SOURCE_DIR}/gnutls-${UPSTREAM_VERSION}.tar.xz
	                    URL_HASH SHA1=9001ec4c4ae9decd9aeed13fc6a9ca60b4ffb3a7
#	                    PATCH_COMMAND "${PYTHON_EXECUTABLE}" ${CMAKE_HOME_DIRECTORY}/cmake/tools/apply_patches.py --working-folder ${CMAKE_CURRENT_BINARY_DIR}/gnutls/src/TARGET_gnutls --patch-folder ${CMAKE_CURRENT_SOURCE_DIR}/patches --strip 1
	                    CONFIGURE_COMMAND ${CMAKE_COMMAND} -E env "GMP_CFLAGS=-I${GMP_INCLUDE}" "GMP_LIBS=-L${GMP_LIBS}" "PKG_CONFIG_PATH=${PKGCONFIG_JONCHKI}" ${CMAKE_CURRENT_BINARY_DIR}/gnutls/src/TARGET_gnutls/configure --prefix=${CMAKE_CURRENT_BINARY_DIR}/install --disable-doc --disable-tools --disable-tests --enable-static=yes --enable-shared=no --with-pic --with-included-libtasn1 --with-included-unistring --without-p11-kit --without-idn --with-libz-prefix=${ZLIB_PREFIX}
	                    BUILD_COMMAND make
	                    INSTALL_COMMAND make install
	                    TEST_COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_SOURCE_DIR}/cmake/tools/fix_pkgconfig.py ${CMAKE_BINARY_DIR}/gnutls/install/lib/pkgconfig ${CMAKE_BINARY_DIR}/gnutls/install/pkgconfig --oldinstallpath ${CMAKE_BINARY_DIR}/gnutls/install
	                    TEST_AFTER_INSTALL 1
	)

	SET(LIBGNUTLS_PREFIX       ${CMAKE_CURRENT_BINARY_DIR}/install    "The complete path to the libgnutls installation.")
	SET(LIBGNUTLS_LIBRARY      ${LIBGNUTLS_PREFIX}/lib/libgnutls.a    "The complete path to the libgnutls library.")
	SET(LIBGNUTLS_INCLUDE_DIR  ${LIBGNUTLS_PREFIX}/include            "The include folder for the libgnutls library.")

	# Create a package.
	SET(CPACK_OUTPUT_FILE_PREFIX ${CMAKE_BINARY_DIR}/../repository/org/gnutls/gnutls/${PROJECT_VERSION})
	SET(CPACK_INCLUDE_TOPLEVEL_DIRECTORY FALSE)
	SET(CPACK_GENERATOR "TXZ")

	INSTALL(FILES ${CMAKE_CURRENT_BINARY_DIR}/install/lib/libgnutls.a
	              ${CMAKE_CURRENT_BINARY_DIR}/install/lib/libgnutls.la
	              ${CMAKE_CURRENT_BINARY_DIR}/install/lib/libgnutlsxx.a
	              ${CMAKE_CURRENT_BINARY_DIR}/install/lib/libgnutlsxx.la
	        TYPE LIB)
	INSTALL(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/install/include/
	        DESTINATION include)

	INSTALL(FILES ${CMAKE_CURRENT_BINARY_DIR}/install/pkgconfig/gnutls.pc
	        DESTINATION pkgconfig)

	CONFIGURE_FILE(installer/install.lua 
	               ${CMAKE_CURRENT_BINARY_DIR}/package/install.lua
	               @ONLY)

	INSTALL (FILES ${CMAKE_CURRENT_BINARY_DIR}/package/install.lua
	         DESTINATION .)

	CONFIGURE_FILE(installer/gnutls.xml
	               ${CPACK_OUTPUT_FILE_PREFIX}/gnutls-${PROJECT_VERSION}-${JONCHKI_PLATFORM}.xml
	               @ONLY)

	SET(CPACK_PACKAGE_FILE_NAME "gnutls-${PROJECT_VERSION}-${JONCHKI_PLATFORM}")

	INCLUDE(CPack)

	#-----------------------------------------------------------------------------
	#
	# Create a custom target named "pack".
	# It builds the package and creates the hashes.
	#
	ADD_CUSTOM_TARGET(pack
	                  COMMAND ${CMAKE_MAKE_PROGRAM}
	                  COMMAND ${CMAKE_MAKE_PROGRAM} package
	                  COMMAND "${PYTHON_EXECUTABLE}" ${CMAKE_HOME_DIRECTORY}/cmake/tools/generate_hash.py ${CPACK_OUTPUT_FILE_PREFIX}/gnutls-${PROJECT_VERSION}-${JONCHKI_PLATFORM}.xml
	                  COMMAND "${PYTHON_EXECUTABLE}" ${CMAKE_HOME_DIRECTORY}/cmake/tools/generate_hash.py ${CPACK_OUTPUT_FILE_PREFIX}/gnutls-${PROJECT_VERSION}-${JONCHKI_PLATFORM}.tar.xz
	                  COMMENT "Pack the artifact and generate the hashes...")
ENDIF((${BUILDCFG_ONLY_JONCHKI_CFG} STREQUAL "OFF"))
