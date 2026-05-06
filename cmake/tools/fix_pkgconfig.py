#! /usr/bin/python3
import argparse
import glob
import os

tParser = argparse.ArgumentParser()
tParser.add_argument('src')
tParser.add_argument('dst')
tParser.add_argument('--oldinstallpath', help='The old value of the install path which should be replaced.')
tArgs = tParser.parse_args()

# Get the mandatory arguments.
strSrc = tArgs.src
strDst = tArgs.dst

# The "old install dir" is optional and defaults to the destination folder.
strInstallDir = tArgs.oldinstallpath
if not strInstallDir:
    strInstallDir = strDst

# Create the destination folder if it does not exist yet.
os.mkdir(strDst)

for strSrcFile in glob.iglob(os.path.join(strSrc, '*.pc')):
    print('  Processing file "%s".' % (strSrcFile))
    # Read the complete PKGCONFIG file.
    tFileSrc = open(strSrcFile, 'r')
    strPkgConfig = tFileSrc.read()
    tFileSrc.close()

    # Replace all occurences of the install directory with a path relative to the file.
    strPkgConfig = strPkgConfig.replace(strInstallDir, '${pcfiledir}/..')

    # Replace all references to a 'lib64' folder with a plain 'lib' folder.
    strPkgConfig = strPkgConfig.replace('/lib64', '/lib')

    # Write the processed data.
    strDstFile = os.path.join(
        strDst,
        os.path.basename(strSrcFile)
    )
    print('  Writing to "%s".' % (strDstFile))
    tFileDst = open(strDstFile, 'w')
    tFileDst.write(strPkgConfig)
    tFileDst.close()
