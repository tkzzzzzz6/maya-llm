@echo off
REM YAYA 语音服务启动脚本 (Windows)

echo ========================================
echo   YAYA 语音服务启动脚本
echo ========================================
echo.

REM 设置代理（如果需要访问 Edge-TTS）
set https_proxy=http://192.168.243.93:7890  
set http_proxy=http://192.168.243.93:7890
echo 代理已配置: %https_proxy%
echo.

REM 激活 conda 环境（如果使用 conda）
REM call conda activate llm

python yaya_voice_server_full.py
