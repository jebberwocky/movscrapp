#!/bin/bash
# Setup
# Helper functions
info() {
  echo -e "\033[1;34m$@\033[0m"
}

error() {
  echo -e "\033[1;31m$@\033[0m" >&2
}

directory="/mnt/pokkoaall/cronwork/pugua"

info "copying requirements"
scp ./requirements.txt ubuntu@pukkoa.cc:${directory}
info "copying pugua.py"
scp ./pugua.py ubuntu@pukkoa.cc:${directory}
#info "copying default.ini"
#scp ./default.ini ubuntu@pukkoa.cc:${directory}