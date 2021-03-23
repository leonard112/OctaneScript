#!/bin/bash

set -e

if [ "$OS" == "windows" ]; then
    choco install python3 --version=3.9.1
    choco install nsis
    export PATH="/c/Program Files (x86)/NSIS:$PATH"
fi

if [ "$RELEASE_STATUS" == "DEV" ]; then
    PACKAGE_NAME="$NAME_LOWER-$VERSION-$COMMIT_SHORT-$RELEASE_STATUS-$OS-amd64"
    WINDOWS_INSTALLER_VERSION_TAG="$VERSION ($COMMIT_SHORT) $RELEASE_STATUS"
else
    PACKAGE_NAME="$NAME_LOWER-$VERSION-$OS-amd64"
    WINDOWS_INSTALLER_VERSION_TAG=$VERSION
fi

# Update metadata 
sed -i "s/Alpha DEV/$VERSION-$COMMIT_SHORT $RELEASE $RELEASE_STATUS/" Main.py

if [ "$OS" == "linux" ]; then 
    cd .. && CONTROL_FILE="package_debian/package/DEBIAN/control"
    sed -i "s/package/$PACKAGE_NAME/" $CONTROL_FILE
    sed -i "s/arch/$ARCH/" $CONTROL_FILE
    sed -i "s/maintainer/$MAINTAINER/" $CONTROL_FILE
    sed -i "s/version/$VERSION.$COMMIT_SHORT/" $CONTROL_FILE
    cat $CONTROL_FILE
elif [ "$OS" == "windows" ]; then
    cd $WINDOWS_INSTALLER_DIR
    INSTALLER_CREATION_SCRIPT="installer.nsi"
    sed -i "s/DEV/$WINDOWS_INSTALLER_VERSION_TAG/" $INSTALLER_CREATION_SCRIPT
    sed -i "s/octanescript-installer/$PACKAGE_NAME-installer/" $INSTALLER_CREATION_SCRIPT
fi

# Install dependencies
if [ "$OS" == "linux" ]; then
    cd $SRC_DIR && pip install -r requirements.txt
elif [ "$OS" == "windows" ]; then
    cd $SRC_DIR && py -m pip install -r requirements.txt
    export PATH="/c/Python39/Scripts:$PATH"
fi

# Test
cd .. && pytest --cov=src src/test && cd src

# Build
if [ "$OS" == "linux" ]; then 
    pyinstaller --onefile --icon=$ICON --name os  Main.py
    echo -e "SMOKE TEST:" && cd dist && ./os --version
elif [ "$OS" == "windows" ]; then 
    pyinstaller --onefile --icon=$ICON --name os.exe  Main.py
    echo -e "SMOKE TEST:" && cd dist && ./os.exe --version
fi

# Publish Archive
echo -e "${SFTP_KEY}" > /tmp/sftp_rsa
chmod 400 /tmp/sftp_rsa
cp $LICENSE .
if [ "$OS" == "linux" ]; then 
    tar -czvf $PACKAGE_NAME.tgz *
    TAR_UPLOAD_LOCATION="$PUBLISH_REPO/$RELEASE_LOWER/$OS/$ARCH/$RELEASE_STATUS_LOWER/tar"
    sftp -o "StrictHostKeyChecking=no" -i /tmp/sftp_rsa $TAR_UPLOAD_LOCATION <<< $"put ${PACKAGE_NAME}.tgz"
elif [ "$OS" == "windows" ]; then
    tar.exe -a -c -f $PACKAGE_NAME.zip *
    ZIP_UPLOAD_LOCATION="$PUBLISH_REPO/$RELEASE_LOWER/$OS/$ARCH/$RELEASE_STATUS_LOWER/zip"
    sftp -o "StrictHostKeyChecking=no" -i /tmp/sftp_rsa $ZIP_UPLOAD_LOCATION <<< $"put ${PACKAGE_NAME}.zip"
fi

# Package For Debian
if [ "$OS" == "linux" ]; then
    mkdir -p $DEB_PACKAGE_DIR/package/usr/bin && cp os $DEB_PACKAGE_DIR/package/usr/bin
    mkdir -p $DEB_PACKAGE_DIR/package/usr/share/doc && cp LICENSE $DEB_PACKAGE_DIR/package/usr/share/doc/copyright
    cd $DEB_PACKAGE_DIR && mv package $PACKAGE_NAME
    dpkg --build $PACKAGE_NAME
    DEB_UPLOAD_LOCATION="$PUBLISH_REPO/$RELEASE_LOWER/$OS/$ARCH/$RELEASE_STATUS_LOWER/debian"
    sftp -o "StrictHostKeyChecking=no" -i /tmp/sftp_rsa $DEB_UPLOAD_LOCATION <<< $"put ${PACKAGE_NAME}.deb"
fi

# Create Windows Installer
if [ "$OS" == "windows" ]; then
    cd $WINDOWS_INSTALLER_DIR
    cp ../src/dist/* $WINDOWS_INSTALLER_DIR
    makensis $INSTALLER_CREATION_SCRIPT
    INSTALLER_UPLOAD_LOCATION="$PUBLISH_REPO/$RELEASE_LOWER/$OS/$ARCH/$RELEASE_STATUS_LOWER/installer"
    sftp -o "StrictHostKeyChecking=no" -i /tmp/sftp_rsa $INSTALLER_UPLOAD_LOCATION <<< $"put ${PACKAGE_NAME}-installer.exe"
fi

sftp -o "StrictHostKeyChecking=no" -i /tmp/sftp_rsa $PUBLISH_REPO <<< $"put ${README}"
