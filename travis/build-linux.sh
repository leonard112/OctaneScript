#!/bin/bash

set -e

# Install dependencies
apt-get install python
pip install -r requirements.txt

# Test
cd $TEST_DIR && python TestPrinter.py

# Build
cd $HOME_DIR && pyinstaller --onefile  --name octane  main.py
cp -r resources dist/ && cp -r core/usage dist/
echo "SMOKE TEST:" && cd dist && ./octane -version && cd ..

# Publish
echo -e "${SFTP_KEY}" > /tmp/sftp_rsa
chmod 400 /tmp/sftp_rsa
cd dist && tar -czvf $FILE_NAME_LINUX *
sftp -o "StrictHostKeyChecking=no" -i /tmp/sftp_rsa lcarcaramo@frs.sourceforge.net:/home/frs/project/octane-lang/alpha/linux <<< $"put ${FILE_NAME_LINUX}"
