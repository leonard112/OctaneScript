#!/bin/bash

set -e

if [ "$RELEASE_STATUS" == "DEV" ]; then
    export PACKAGE_NAME="$NAME_LOWER-$VERSION($COMMIT_SHORT)-$RELEASE_STATUS"
else
    export PACKAGE_NAME="$NAME_LOWER-$VERSION"
fi

# Update metadata 
sed -i "s/Alpha DEV/$VERSION:$COMMIT_SHORT $RELEASE $RELEASE_STATUS/" Main.py
cat Main.py

cd .. && export CONTROL_FILE="package_debian/package/DEBIAN/control"
sed -i "s/package/$VERSION:$PACKAGE_NAME/" $CONTROL_FILE
sed -i "s/arch/$VERSION:$ARCH/" $CONTROL_FILE
sed -i "s/maintainer/$VERSION:$ARCH/" $CONTROL_FILE
sed -i "s/version/$VERSION:$COMMIT_SHORT $RELEASE $RELEASE_STATUS/" $CONTROL_FILE
cat $CONTROL_FILE

# Install dependencies
cd $SRC_DIR && pip install -r requirements.txt

# Test
pytest --cov=src test

# Build
pyinstaller --onefile  --name octane  Main.py
echo -e "SMOKE TEST:" && cd dist && ./octane --version

# Publish Tar
echo -e "${SFTP_KEY}" > /tmp/sftp_rsa
chmod 400 /tmp/sftp_rsa
cp $LICENSE .
tar -czvf $PACKAGE_NAME.tgz *
sftp -o "StrictHostKeyChecking=no" -i /tmp/sftp_rsa lcarcaramo@frs.sourceforge.net:/home/frs/project/octane-lang/$RELEASE_LOWER/$OS/$ARCH/$RELEASE_STATUS_LOWER/tar <<< $"put ${PACKAGE_NAME}.tgz"

# Package For Debian
mkdir -p $DEB_PACKAGE_DIR/package/usr/bin && cp octane $DEB_PACKAGE_DIR/package/usr/bin
cd $DEB_PACKAGE_DIR && dpkg --build $PACKAGE_NAME
sftp -o "StrictHostKeyChecking=no" -i /tmp/sftp_rsa lcarcaramo@frs.sourceforge.net:/home/frs/project/octane-lang/$RELEASE_LOWER/$OS/$ARCH/$RELEASE_STATUS_LOWER/debian <<< $"put ${PACKAGE_NAME}.deb"

sftp -o "StrictHostKeyChecking=no" -i /tmp/sftp_rsa lcarcaramo@frs.sourceforge.net:/home/frs/project/octane-lang <<< $"put ${README}"
