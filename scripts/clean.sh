#!/bin/sh

set -e

SUCCESS_MESSAGE="CLEANED SUCCESSFULLY!"

BUILD_DIR="dejavu/"

for i in "${BUILD_DIR}"*_pb2*.py; do
  echo "Deleting $i"
  rm $i
done

echo "${SUCCESS_MESSAGE}"
