#!/bin/sh

SRC_DIR=$(dirname $0);
java -cp ${SRC_DIR}/../lib/java/*:${SRC_DIR}/../ext/java/*:. com.autocognite.Arjuna "$@"

