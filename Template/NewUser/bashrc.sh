# Default User Bash Configuration
# Template is save at /etc/skel/.bashrc
# Save this file as ~/.bashrc

# Load CUDA environment variables

# Modify this line to match your CUDA installation
export CUDA_HOME="/usr/local/cuda"

# Do not modify below this line!!!
export CUDAToolkit_ROOT="$CUDA_HOME"
export PATH="$PATH:$CUDA_HOME/bin"
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$CUDA_HOME/lib64/"
export LIBRARY_PATH="$LIBRARY_PATH:$CUDA_HOME/lib64"
