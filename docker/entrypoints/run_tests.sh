#!/usr/bin/env bash
set -e

trap error_handler ERR

error_handler() {
  exitcode=$?
  echo -e "$SET_ERROR_TEXT $BASH_COMMAND failed!!! $RESET_FORMATTING"
  # Some more clean up code can be added here before exiting
  exit $exitcode
}


echo "Running black ..." && python -m black library_app
