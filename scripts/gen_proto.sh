#!/bin/sh

set -e

SUCCESS_MESSAGE="FINISHED SUCCESSFULLY!"

BUILD_DIR="dejavu/"
PROTO_SRC_DIR="proto"

[ -d "${BUILD_DIR}" ] || mkdir -p "${BUILD_DIR}"

python -m grpc_tools.protoc \
  -I"${PROTO_SRC_DIR}" \
  --python_out=${BUILD_DIR} \
  --grpc_python_out=${BUILD_DIR} \
  "${PROTO_SRC_DIR}"/*.proto

echo "${SUCCESS_MESSAGE}"
