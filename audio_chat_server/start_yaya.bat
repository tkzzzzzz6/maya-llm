@echo off
REM YAYA �������������ű� (Windows)

echo ========================================
echo   YAYA �������������ű�
echo ========================================
echo.

REM ���ô��������Ҫ���� Edge-TTS��
set https_proxy=http://192.168.243.93:7890  
set http_proxy=http://192.168.243.93:7890
echo ����������: %https_proxy%
echo.

REM ���� conda ���������ʹ�� conda��
REM call conda activate llm

python yaya_voice_server_full.py
