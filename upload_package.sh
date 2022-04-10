#!/usr/bin/env bash
#--major/--minor/--patch
UPDATE_VERSION="patch"
if [[ $1 ]]; then UPDATE_VERSION=$1; fi

bumpver update --$UPDATE_VERSION --no-commit
python3 setup.py sdist
DIST_MODULE_NAME="communicationAppModule-"
VERSION=$(bumpver show -n)
VERSION=$(echo "$VERSION" | grep 'Current Version: ' | cut -d\  -f3)
echo $VERSION
URL="https://upload.pypi.org/legacy/"
DIST="$DIST_MODULE_NAME$VERSION.tar.gz"
twine upload -u wayneshang --repository-url $URL dist/$DIST --verbose