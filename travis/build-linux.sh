#!/bin/bash

set -e

if [ "$RELEASE_STATUS" == "DEV" ]; then
    export PACKAGE_NAME="$NAME_LOWER-$VERSION-$COMMIT_SHORT-$RELEASE_STATUS"
else
    export PACKAGE_NAME="$NAME_LOWER-$VERSION"
fi

# Update metadata 
sed -i "s/Alpha DEV/$VERSION($COMMIT_SHORT) $RELEASE $RELEASE_STATUS/" Main.py
cat Main.py

cd .. && export CONTROL_FILE="package_debian/package/DEBIAN/control"
sed -i "s/package/$PACKAGE_NAME/" $CONTROL_FILE
sed -i "s/arch/$ARCH/" $CONTROL_FILE
sed -i "s/maintainer/$MAINTAINER/" $CONTROL_FILE
sed -i "s/version/$VERSION.$COMMIT_SHORT/" $CONTROL_FILE
cat $CONTROL_FILE

# Install dependencies
cd $SRC_DIR && pip install -r requirements.txt

# Test
pytest --cov=src test

# Build
pyinstaller --onefile  --name os  Main.py
echo -e "SMOKE TEST:" && cd dist && ./os --version

# Publish Tar
echo -e "${SFTP_KEY}" > /tmp/sftp_rsa
chmod 400 /tmp/sftp_rsa
cp $LICENSE .
tar -czvf $PACKAGE_NAME.tgz *
export TAR_UPLOAD_LOCATION="$PUBLISH_REPO/$RELEASE_LOWER/$OS/$ARCH/$RELEASE_STATUS_LOWER/tar"
sftp -o "StrictHostKeyChecking=no" -i /tmp/sftp_rsa $TAR_UPLOAD_LOCATION <<< $"put ${PACKAGE_NAME}.tgz"

# Package For Debian
mkdir -p $DEB_PACKAGE_DIR/package/usr/bin && cp octane $DEB_PACKAGE_DIR/package/usr/bin
mkdir -p $DEB_PACKAGE_DIR/package/usr/share/doc && cp LICENSE $DEB_PACKAGE_DIR/package/usr/share/doc/copyright
cd $DEB_PACKAGE_DIR && mv package $PACKAGE_NAME
dpkg --build $PACKAGE_NAME
export DEB_UPLOAD_LOCATION="$PUBLISH_REPO/$RELEASE_LOWER/$OS/$ARCH/$RELEASE_STATUS_LOWER/debian"
sftp -o "StrictHostKeyChecking=no" -i /tmp/sftp_rsa $DEB_UPLOAD_LOCATION <<< $"put ${PACKAGE_NAME}.deb"

sftp -o "StrictHostKeyChecking=no" -i /tmp/sftp_rsa $PUBLISH_REPO <<< $"put ${README}"
