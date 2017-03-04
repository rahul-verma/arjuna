#!/bin/bash

SRC_DIR=$(dirname $0);
java -cp ${SRC_DIR}/dependencies/jars/*:${SRC_DIR}/lib/*:. com.autocognite.Unitee "$@"

