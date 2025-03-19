#!/bin/bash

# 设置基本参数
CONFIG_PATH="configs/MSDFont/MSDFont_Train_Stage1_trans_model_predx0_miniUnet.yaml"
GPUS="0,"
MIN_FREE_SPACE_GB=30
CHECK_INTERVAL_SECONDS=600
LOGS_DIR="/home/zihun/workspace/fontspace/MSDFont/StableDiffusion/logs/stage1_1"
LOGS_FOLDER="/home/zihun/workspace/fontspace/MSDFont/StableDiffusion/logs/stage1_1.log"
TIMESTAMP=$(date '+%Y-%m-%d_%H:%M:%S')
DEBUG_LOG="${LOGS_FOLDER}/debug_${TIMESTAMP}.log"
TRAIN_LOG="${LOGS_FOLDER}/train_${TIMESTAMP}.log"

# 创建日志目录
mkdir -p $LOGS_FOLDER

# 清空之前的训练产物
if [ -d "$LOGS_DIR" ]; then
    echo "清空之前的训练产物..."
    rm -rf $LOGS_DIR/*
fi

# 创建训练目录
mkdir -p $LOGS_DIR

# 记录调试信息的函数
log_debug() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $DEBUG_LOG
}

log_debug "训练脚本开始执行"
log_debug "配置文件: $CONFIG_PATH"
log_debug "使用GPU: $GPUS"
log_debug "训练时间戳: $TIMESTAMP"

# 禁用 DeepSpeed
export PL_DISABLE_DEEPSPEED=1
log_debug "已禁用 DeepSpeed (PL_DISABLE_DEEPSPEED=1)"

# 检查Python和CUDA版本
log_debug "Python版本: $(python --version 2>&1)"
log_debug "CUDA是否可用: $(python -c 'import torch; print(torch.cuda.is_available())')"
log_debug "CUDA版本: $(python -c 'import torch; print(torch.version.cuda if torch.cuda.is_available() else "不可用")')"
log_debug "可用GPU数量: $(python -c 'import torch; print(torch.cuda.device_count())')"

# 检查磁盘空间函数
check_disk_space() {
    local free_space=$(df -BG --output=avail $LOGS_DIR | tail -n 1 | tr -d 'G')
    log_debug "当前可用磁盘空间: ${free_space}GB"
    
    if [ $free_space -lt $MIN_FREE_SPACE_GB ]; then
        log_debug "磁盘空间不足! 当前可用: ${free_space}GB, 最小要求: ${MIN_FREE_SPACE_GB}GB"
        return 1
    fi
    
    return 0
}

# 清理旧的检查点文件
clean_old_checkpoints() {
    log_debug "开始清理旧的检查点文件..."
    
    # 保留最新的last.ckpt和最新的3个epoch检查点
    for ckpt_dir in $(find $LOGS_DIR -type d -name "checkpoints"); do
        # 保留last.ckpt
        if [ -f "$ckpt_dir/last.ckpt" ]; then
            touch "$ckpt_dir/last.ckpt"  # 更新时间戳
        fi
        
        # 获取最新的3个epoch检查点
        find "$ckpt_dir" -name "epoch=*.ckpt" -type f -printf "%T@ %p\n" | sort -nr | head -n 3 | cut -d' ' -f2- | while read file; do
            touch "$file"  # 更新时间戳
        done
        
        # 删除其他所有检查点
        find "$ckpt_dir" -name "*.ckpt" -type f -not -newermt "1 minute ago" -delete
    done
    
    log_debug "清理完成"
}

# 检查配置文件是否存在
if [ ! -f "$CONFIG_PATH" ]; then
    log_debug "错误: 配置文件 $CONFIG_PATH 不存在!"
    exit 1
fi

# 检查数据路径是否存在
DATA_DIR=$(grep -A5 "data_dirs" $CONFIG_PATH | grep -o '"/[^"]*"' | tr -d '"')
if [ ! -z "$DATA_DIR" ] && [ ! -d "$DATA_DIR" ]; then
    log_debug "警告: 数据目录 $DATA_DIR 不存在或不可访问!"
fi

# 主循环
main() {
    # 首先检查磁盘空间
    if ! check_disk_space; then
        log_debug "尝试清理空间..."
        clean_old_checkpoints
        
        # 再次检查空间
        if ! check_disk_space; then
            log_debug "清理后磁盘空间仍然不足! 请手动清理空间后重试。"
            exit 1
        fi
    fi
    
    # 启动训练
    log_debug "启动训练..."
    
    # 在前台运行训练，重定向输出到日志文件
    log_debug "执行命令: python main.py --base $CONFIG_PATH -t --gpus $GPUS --logdir /home/zihun/workspace/fontspace/MSDFont/StableDiffusion/logs --name stage1_1 --postfix ''"
    python main.py --base $CONFIG_PATH -t --gpus $GPUS --logdir /home/zihun/workspace/fontspace/MSDFont/StableDiffusion/logs --name stage1_1 --postfix '' 2>&1 | tee -a $TRAIN_LOG
    
    EXIT_CODE=$?
    log_debug "训练结束，退出代码: $EXIT_CODE"
    
    if [ $EXIT_CODE -ne 0 ]; then
        log_debug "训练异常退出! 请检查日志文件 $TRAIN_LOG 获取详细错误信息。"
    fi
    
    return $EXIT_CODE
}

# 执行主函数
main
log_debug "训练脚本执行完毕"
