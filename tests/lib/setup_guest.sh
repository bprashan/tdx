#!/bin/bash

# this script is supposed to be executed under root
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
export no_proxy=127.0.0.1,localhost
sudo yum install -y python3 python3-pip cpuid git

cd ${SCRIPT_DIR}/tdx-tools/
python3 -m pip install ./ 2>&1 | tee install.log
git clone https://github.com/stefano-garzarella/iperf-vsock /tmp/iperf-vsock
cd /tmp/iperf-vsock
./bootstrap.sh
mkdir build
cd build
../configure
make