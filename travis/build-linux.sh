#!/bin/bash

set -e

# Install dependencies
pip install -r requirements.txt

# Test
cd .. && pytest --cov=src src/test

# Build
cd $SRC_DIR && pyinstaller --onefile  --name octane  Main.py
echo "SMOKE TEST:" && cd dist && ./octane --version

# Publish
echo -e "${SFTP_KEY}" > /tmp/sftp_rsa
chmod 400 /tmp/sftp_rsa
cp $LICENSE .
tar -czvf $FILE_NAME_LINUX *
sftp -o "StrictHostKeyChecking=no" -i /tmp/sftp_rsa lcarcaramo@frs.sourceforge.net:/home/frs/project/octane-lang/alpha/linux <<< $"put ${FILE_NAME_LINUX}"
sftp -o "StrictHostKeyChecking=no" -i /tmp/sftp_rsa lcarcaramo@frs.sourceforge.net:/home/frs/project/octane-lang <<< $"put ${README}"
