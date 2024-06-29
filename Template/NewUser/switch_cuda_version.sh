#!/bin/bash

# 查找 /usr/local 下存在的 CUDA 版本目录
cuda_dirs=()
while IFS= read -r -d '' dir; do
    cuda_dirs+=("$dir")
done < <(find /usr/local -maxdepth 1 -type d -name "cuda-*" -print0)

# 如果没有找到任何 CUDA 版本，则提示并退出
if [ ${#cuda_dirs[@]} -eq 0 ]; then
    echo "警告：未在 /usr/local 下找到任何 CUDA 版本目录。"
    exit 1
fi

# 显示可用 CUDA 版本列表供用户选择
echo "请选择一个 CUDA 版本:"
for ((i=0; i<${#cuda_dirs[@]}; i++)); do
    echo "[$(($i+1))] ${cuda_dirs[i]##*/}"
done
read -p "请输入您的选择 (1-${#cuda_dirs[@]}): " choice

# 设置 CUDA_HOME
if [ "$choice" -gt 0 ] && [ "$choice" -le ${#cuda_dirs[@]} ]; then
    export CUDA_HOME="${cuda_dirs[$(($choice-1))]}"
    export CUDAToolkit_ROOT="$CUDA_HOME"

    current_path="$PATH"

    export PATH="$CUDA_HOME/bin:$current_path"
    export PATH="$PATH:$CUDA_HOME/bin"

    export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:$CUDA_HOME/lib64/"
    export LIBRARY_PATH="$LIBRARY_PATH:$CUDA_HOME/lib64"
    echo "已成功设置CUDA_HOME为$CUDA_HOME"
else
    echo "无效的选择，请重新运行并输入正确的选项。"
fi
