#!/bin/bash

DEFAULT_TAG="0.1.0-dev.1"


function read_tags() {
  echo "Parsing tags list"
  LAST_DEV_TAG=$(echo "$TAGS" | grep dev | sort -t "." -k1,1n -k2,2n -k3,3n -k4,4n | tail -1)
  LAST_RC_TAG=$(echo "$TAGS" | grep RC | sort -t "." -k1,1n -k2,2n -k3,3n -k4,4n | tail -1)

  echo "Last dev tag is: $LAST_DEV_TAG and last RC tag is: $LAST_RC_TAG"
}

function next_dev_tag() {
    read_tags
    if [ -z $LAST_DEV_TAG ] ; then
      echo "Last dev tag not found, returning default version"
      VERSION=$DEFAULT_TAG
    else
      VERSION_BASE_AND_SUFFIX=(`echo $LAST_DEV_TAG | tr '-' ' '`)
      VERSION_BASE="${VERSION_BASE_AND_SUFFIX[0]}"
      SUFFIX=${VERSION_BASE_AND_SUFFIX[@]: -1:1}

      echo "Base: $VERSION_BASE, Suffix: $SUFFIX"
      
      VERSION_ARRAY=(`echo $VERSION_BASE | tr '.' ' '`)
      MAJOR="${VERSION_ARRAY[0]}"
      MINOR="${VERSION_ARRAY[1]}"
      PATCH="${VERSION_ARRAY[2]}"

      if [ -z $PATCH ]; then
        echo "Patch version part not found, defaulting to 0"
        PATCH="0"
      fi

      echo "Major: $MAJOR, Minor: $MINOR, Patch: $PATCH"

      MATCHING_RC=$(echo "$TAGS" | grep -E "$MAJOR\.$MINOR.?-RC\.")

      if [ -z $MATCHING_RC ] ; then
        echo "Matching RC version not found, incrementing dev version"
        SUFFIX_ARRAY=(`echo $SUFFIX | tr '.' ' '`)
        SUFFIX_VERSION=${SUFFIX_ARRAY[@]: -1:1}
        NEXT_SUFFIX_VERSION=$((${SUFFIX_VERSION}+1))
        echo "Suffix version: $NEXT_SUFFIX_VERSION"
        VERSION="$MAJOR.$MINOR.$PATCH-dev.$NEXT_SUFFIX_VERSION"

      else
        echo "Found matching RC version: $MATCHING_RC, incrementing minor version"
        NEXT_MINOR=$((${MINOR}+1))
        VERSION="$MAJOR.$NEXT_MINOR.$PATCH-dev.1"
      fi
    fi

    echo "Version: $VERSION"
    
}

function assertEq() {
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  NC='\033[0m'

  if [ "$1" == "$2" ] ; then 
    echo -e "${GREEN}OK${NC} - ${1} is equal to ${2}"
  else
    echo -e "${RED}Fail${NC} - ${1} is not equal to ${2}"
  fi
}


echo "--TESTS--"
echo "Should return default tag if tags list is empty"
TAGS=""
next_dev_tag
assertEq $VERSION $DEFAULT_TAG

echo "----"
echo "Should return next dev tag if no RC tag is present"
read -r -d '' TAGS <<- EOM
    0.1-dev.1
    0.1-dev.10
    0.1-dev.11
    0.1-dev.2
    0.1-dev.3
    0.1-dev.4
    0.1-dev.5
    0.1-dev.6
    0.1-dev.7
    0.1-dev.8
    0.1-dev.9
EOM
next_dev_tag
assertEq $VERSION "0.1.0-dev.12"

echo "----"
echo "Should bump minor if RC tag is present"
read -r -d '' TAGS <<- EOM
    0.1-dev.1
    0.1-dev.10
    0.1-dev.11
    0.1-dev.2
    0.1-dev.3
    0.1-dev.4
    0.1-dev.5
    0.1-dev.6
    0.1-dev.7
    0.1-dev.8
    0.1-dev.9
    0.1-RC.1
EOM
next_dev_tag
assertEq $VERSION "0.2.0-dev.1"