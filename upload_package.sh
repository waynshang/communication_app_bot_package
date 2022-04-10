#!/usr/bin/env bash
bumpver update --patch --no-commit
python3 setup.py sdist
DIST_MODULE_NAME="communicationAppModule-"
VERSION=$(bumpver show -n)
VERSION=$(echo "$VERSION" | grep 'Current Version: ' | cut -d\  -f3)
echo $VERSION
URL="https://upload.pypi.org/legacy/"
DIST="$DIST_MODULE_NAME$VERSION.tar.gz"
twine upload -u wayneshang -p --repository-url $URL dist/$DIST --verbose