#!/bin/bash
# shellcheck disable=SC1090

set -e

env_name="client"

conda_bin_path=$(which conda)
conda_path=$(dirname $(dirname ${conda_bin_path}))
set_var_sh_path="${conda_path}/etc/profile.d/conda.sh"

echo "Try to source ${set_var_sh_path}"

source ${set_var_sh_path}

# Check env is exist
conda env list | grep ${env_name} || {
    conda create -n ${env_name} python=3.12 -y
}

# conda init
conda activate ${env_name}

python_path=$(which python)
echo "Python path: ${python_path}"

# Install requirements
${python_path} -m pip install -r requirements.txt

env_file=".env.sh"
if [ -f "$env_file" ]; then
    source "$env_file" || {
        echo "Failed to source $env_file"
        exit 1
    }
fi

# if ! cd src; then
#     echo "Failed to change directory to src"
#     exit 1
# fi

if ! command -v python &>/dev/null; then
    echo "Python is not installed"
    exit 1
fi

${python_path} src/main.py
