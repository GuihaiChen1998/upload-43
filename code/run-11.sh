#!/bin/bash
set -euo pipefail

# 配置
PORT=8000
HEALTH_URL="http://localhost:${PORT}/health"
MAX_WAIT=300
WAIT_INTERVAL=2
LOG_DIR="./logs"
mkdir -p "$LOG_DIR"

# 等待 vLLM 服务就绪
wait_for_vllm() {
	    local model_name=$1
	        local start_time=$(date +%s)
		    
		    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 等待 vLLM 启动: $model_name"
		        
		        while true; do
				        if curl -s "$HEALTH_URL" > /dev/null 2>&1; then
						            echo "[$(date '+%Y-%m-%d %H:%M:%S')] vLLM 已就绪: $model_name"
							                return 0
									        fi
										        
										        local current_time=$(date +%s)
											        local elapsed=$((current_time - start_time))
												        
												        if [ $elapsed -ge $MAX_WAIT ]; then
														            echo "[$(date '+%Y-%m-%d %H:%M:%S')] 错误: vLLM 启动超时 ($MAX_WAIT 秒): $model_name"
															                return 1
																	        fi
																		        
																		        echo "[$(date '+%Y-%m-%d %H:%M:%S')] vLLM 尚未就绪，已等待 ${elapsed} 秒..."
																			        sleep $WAIT_INTERVAL
																				    done
																			    }

																		    # 启动 vLLM
																		    start_vllm() {
																			        local model_path=$1
																				    local model_name=$2
																				        
																				        echo "[$(date '+%Y-%m-%d %H:%M:%S')] =========================================="
																					    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 启动模型: $model_name"
																					        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 模型路径: $model_path"
																						    echo "[$(date '+%Y-%m-%d %H:%M:%S')] =========================================="
																						        
																						        # 检查并释放端口
																							    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
																								            echo "[$(date '+%Y-%m-%d %H:%M:%S')] 警告: 端口 $PORT 被占用，尝试释放..."
																									            fuser -k ${PORT}/tcp 2>/dev/null || true
																										            sleep 2
																											        fi
																												    
																												    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 启动 vLLM 服务..."
																												        CUDA_VISIBLE_DEVICES=1,2,3 vllm serve "$model_path" \
																														        --data-parallel-size 3 \
																															        --port $PORT \
																																        --gpu-memory-utilization 0.8 \
																																	        > "$LOG_DIR/vllm_${model_name}.log" 2>&1 &
																													    
																													    VLLM_PID=$!
																													        echo "[$(date '+%Y-%m-%d %H:%M:%S')] vLLM PID: $VLLM_PID"
																														    
																														    if ! wait_for_vllm "$model_name"; then
																															            echo "[$(date '+%Y-%m-%d %H:%M:%S')] vLLM 启动失败，查看日志:"
																																            tail -n 50 "$LOG_DIR/vllm_${model_name}.log"
																																	            kill $VLLM_PID 2>/dev/null || true
																																		            wait $VLLM_PID 2>/dev/null || true
																																			            return 1
																																				        fi
																																					    
																																					    return 0
																																				    }

																																			    # 停止 vLLM
																																			    stop_vllm() {
																																				        local model_name=$1
																																					    
																																					    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 停止 vLLM 服务: $model_name"
																																					        
																																					        if kill $VLLM_PID 2>/dev/null; then
																																							        wait $VLLM_PID 2>/dev/null || true
																																								        echo "[$(date '+%Y-%m-%d %H:%M:%S')] vLLM 已优雅关闭"
																																									    fi
																																									        
																																									        fuser -k ${PORT}/tcp 2>/dev/null || true
																																										    sleep 2
																																										        
																																										        python -c "import torch; torch.cuda.empty_cache()" 2>/dev/null || true
																																											    
																																											    echo "[$(date '+%Y-%m-%d %H:%M:%S')] GPU 状态:"
																																											        nvidia-smi | grep -E "(GPU|MiB| Processes)" || true
																																											}

																																										# 运行 Python 脚本
																																										run_script() {
																																											    local model=$1
																																											        local dataset=$2
																																												    local runs_dir=$3
																																												        
																																												        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 运行脚本: $model on $dataset"
																																													    
																																													    python scripts/11_topk_logprob_drop.py \
																																														            --model "$model" \
																																															            --dataset "$dataset" \
																																																            --runs-dir "$runs_dir" \
																																																	            --kmax 4 \
																																																		            --cap-by-gold \
																																																			            > "$LOG_DIR/run_${model}_${dataset}.log" 2>&1
																																													        
																																													        local exit_code=$?
																																														    
																																														    if [ $exit_code -eq 0 ]; then
																																															            echo "[$(date '+%Y-%m-%d %H:%M:%S')] 脚本成功: $model on $dataset"
																																																        else
																																																		        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 脚本失败 (退出码 $exit_code): $model on $dataset"
																																																			        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 查看日志:"
																																																				        tail -n 50 "$LOG_DIR/run_${model}_${dataset}.log"
																																																					    fi
																																																					        
																																																					        return $exit_code
																																																					}

																																																				# 主流程：启动 vLLM + 运行脚本 + 停止 vLLM
																																																				run_task() {
																																																					    local model_path=$1
																																																					        local model_name=$2
																																																						    local dataset=$3
																																																						        local runs_dir=$4
																																																							    
																																																							    if ! start_vllm "$model_path" "$model_name"; then
																																																								            echo "[$(date '+%Y-%m-%d %H:%M:%S')] 跳过任务: $model_name on $dataset"
																																																									            return 1
																																																										        fi
																																																											    
																																																											    run_script "$model_name" "$dataset" "$runs_dir"
																																																											        local exit_code=$?
																																																												    
																																																												    stop_vllm "$model_name"
																																																												        
																																																												        return $exit_code
																																																												}

																																																											# ==========================================
																																																											# 主程序入口
																																																											# ==========================================

																																																											echo "[$(date '+%Y-%m-%d %H:%M:%S')] 脚本开始执行"
																																																											echo "[$(date '+%Y-%m-%d %H:%M:%S')] 日志目录: $LOG_DIR"

																																																											command -v vllm >/dev/null 2>&1 || { echo "错误: vllm 命令未找到"; exit 1; }
																																																											command -v curl >/dev/null 2>&1 || { echo "错误: curl 未安装"; exit 1; }

																																																											FAILED_TASKS=()

																																																											# ==========================================
																																																											# Qwen3 系列 - hotpotqa
																																																											# ==========================================

																																																											echo "[$(date '+%Y-%m-%d %H:%M:%S')] >>> Qwen3 系列 - hotpotqa 数据集 <<<"

																																																											if ! run_task \
																																																												    "/data1/ekyang/cgh/cache/huggingface_hub/hub/models--Qwen--Qwen3-8B" \
																																																												        "qwen3-8b" \
																																																													    "hotpotqa" \
																																																													        "results/raw/hotpotqa/qwen3-8b"; then
																																																											    FAILED_TASKS+=("qwen3-8b_hotpotqa")
																																																											fi

																																																											if ! run_task \
																																																												    "/data1/ekyang/cgh/cache/huggingface_hub/hub/models--Qwen--Qwen3-4B" \
																																																												        "qwen3-4b" \
																																																													    "hotpotqa" \
																																																													        "results/raw/hotpotqa/qwen3-4b"; then
																																																											    FAILED_TASKS+=("qwen3-4b_hotpotqa")
																																																											fi

																																																											if ! run_task \
																																																												    "/data1/ekyang/cgh/cache/huggingface_hub/hub/models--Qwen--Qwen3-1.7B" \
																																																												        "qwen3-1.7b" \
																																																													    "hotpotqa" \
																																																													        "results/raw/hotpotqa/qwen3-1.7b"; then
																																																											    FAILED_TASKS+=("qwen3-1.7b_hotpotqa")
																																																											fi

																																																											# ==========================================
																																																											# Qwen3 系列 - musique
																																																											# ==========================================

																																																											echo "[$(date '+%Y-%m-%d %H:%M:%S')] >>> Qwen3 系列 - musique 数据集 <<<"

																																																											if ! run_task \
																																																												    "/data1/ekyang/cgh/cache/huggingface_hub/hub/models--Qwen--Qwen3-8B" \
																																																												        "qwen3-8b" \
																																																													    "musique" \
																																																													        "results/raw/musique/qwen3-8b"; then
																																																											    FAILED_TASKS+=("qwen3-8b_musique")
																																																											fi

																																																											if ! run_task \
																																																												    "/data1/ekyang/cgh/cache/huggingface_hub/hub/models--Qwen--Qwen3-4B" \
																																																												        "qwen3-4b" \
																																																													    "musique" \
																																																													        "results/raw/musique/qwen3-4b"; then
																																																											    FAILED_TASKS+=("qwen3-4b_musique")
																																																											fi

																																																											if ! run_task \
																																																												    "/data1/ekyang/cgh/cache/huggingface_hub/hub/models--Qwen--Qwen3-1.7B" \
																																																												        "qwen3-1.7b" \
																																																													    "musique" \
																																																													        "results/raw/musique/qwen3-1.7b"; then
																																																											    FAILED_TASKS+=("qwen3-1.7b_musique")
																																																											fi

																																																											# ==========================================
																																																											# Gemma3 系列 - hotpotqa
																																																											# ==========================================

																																																											echo "[$(date '+%Y-%m-%d %H:%M:%S')] >>> Gemma3 系列 - hotpotqa 数据集 <<<"

																																																											if ! run_task \
																																																												    "/data1/ekyang/cgh/cache/huggingface_hub/hub/models--google--gemma-3-12b-it" \
																																																												        "gemma3-12b" \
																																																													    "hotpotqa" \
																																																													        "results/raw/hotpotqa/gemma3-12b"; then
																																																											    FAILED_TASKS+=("gemma3-12b_hotpotqa")
																																																											fi

																																																											if ! run_task \
																																																												    "/data1/ekyang/cgh/cache/huggingface_hub/hub/models--google--gemma-3-4b-it" \
																																																												        "gemma3-4b" \
																																																													    "hotpotqa" \
																																																													        "results/raw/hotpotqa/gemma3-4b"; then
																																																											    FAILED_TASKS+=("gemma3-4b_hotpotqa")
																																																											fi

																																																											if ! run_task \
																																																												    "/data1/ekyang/cgh/cache/huggingface_hub/hub/models--google--gemma-3-1b-it" \
																																																												        "gemma3-1b" \
																																																													    "hotpotqa" \
																																																													        "results/raw/hotpotqa/gemma3-1b"; then
																																																											    FAILED_TASKS+=("gemma3-1b_hotpotqa")
																																																											fi

																																																											# ==========================================
																																																											# Gemma3 系列 - musique
																																																											# ==========================================

																																																											echo "[$(date '+%Y-%m-%d %H:%M:%S')] >>> Gemma3 系列 - musique 数据集 <<<"

																																																											if ! run_task \
																																																												    "/data1/ekyang/cgh/cache/huggingface_hub/hub/models--google--gemma-3-12b-it" \
																																																												        "gemma3-12b" \
																																																													    "musique" \
																																																													        "results/raw/musique/gemma3-12b"; then
																																																											    FAILED_TASKS+=("gemma3-12b_musique")
																																																											fi

																																																											if ! run_task \
																																																												    "/data1/ekyang/cgh/cache/huggingface_hub/hub/models--google--gemma-3-4b-it" \
																																																												        "gemma3-4b" \
																																																													    "musique" \
																																																													        "results/raw/musique/gemma3-4b"; then
																																																											    FAILED_TASKS+=("gemma3-4b_musique")
																																																											fi

																																																											if ! run_task \
																																																												    "/data1/ekyang/cgh/cache/huggingface_hub/hub/models--google--gemma-3-1b-it" \
																																																												        "gemma3-1b" \
																																																													    "musique" \
																																																													        "results/raw/musique/gemma3-1b"; then
																																																											    FAILED_TASKS+=("gemma3-1b_musique")
																																																											fi

																																																											# ==========================================
																																																											# 汇总
																																																											# ==========================================

																																																											echo ""
																																																											echo "[$(date '+%Y-%m-%d %H:%M:%S')] =========================================="
																																																											echo "[$(date '+%Y-%m-%d %H:%M:%S')] 所有任务执行完毕"

																																																											if [ ${#FAILED_TASKS[@]} -eq 0 ]; then
																																																												    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 全部 12 个任务成功 ✓"
																																																												        exit 0
																																																												else
																																																													    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 失败任务 (${#FAILED_TASKS[@]}/12):"
																																																													        for task in "${FAILED_TASKS[@]}"; do
																																																															        echo "  - $task"
																																																																    done
																																																																        exit 1
																																																											fi
