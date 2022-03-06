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
      VERSION=$DEFAULT_TAG
    else
      VERSION_ARRAY=(`echo $LAST_DEV_TAG | tr '.' ' '`)
      # if number of elements is 3 this is old version pattern without patch - 0.1-dev.1
      # if it's four then version is in new format with patch 0.1.0-dev.1
      MAJOR="${VERSION_ARRAY[0]}"
      MINOR=$(echo ${VERSION_ARRAY[1]} | sed s/-dev//)
      #TODO: detect RC for last dev and bump minor
      # if echo $TAGS | grep -E "${VERSION_ARRAY[0]}\.${VERSION_ARRAY[1]}"..
      #   NEXT_MINOR=$((${MINOR}+1))
      #   VERSION=...
      # ...
      # TODO: else increment dev number
      # else
      #   VERSION_ARRAY=(`echo $LAST_DEV_TAG | tr '.' ' '`)
      #   # if number of elements is 3 this is old version pattern without patch - 0.1-dev.1
      #   # if it's four then version is in new format with patch 0.1.0-dev.1
      #   echo "Number of elements in version array: ${#VERSION_ARRAY[@]}"
      #   LAST_DEV_NUM=${VERSION_ARRAY[@]: -1:1}
      #   echo "Last dev dev number: $LAST_DEV_NUM"
      #   NEXT_DEV_NUM=$((${LAST_DEV_NUM}+1))
      #   echo "Next dev number: ${NEXT_DEV_NUM}"
      #   VERSION=$(echo $LAST_DEV_TAG | sed s/-dev.$LAST_DEV_NUM/-dev.$NEXT_DEV_NUM/)
      # fi
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
assertEq $VERSION "0.1-dev.12"

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
assertEq $VERSION "0.2-dev.1"