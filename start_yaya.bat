@echo off
REM YAYA �������������ű� (Windows)

echo ========================================
echo   YAYA �������������ű�
echo ========================================
echo.

REM ���ô��������Ҫ���� Edge-TTS��
set https_proxy=http://192.168.243.171:7890
set http_proxy=http://192.168.243.171:7890
echo ����������: %https_proxy%
echo.

REM ���� conda ���������ʹ�� conda��
REM call conda activate llm

echo ѡ��Ҫ�����İ汾:
echo [1] ������ (SenseVoice + Edge-TTS) - �Ƽ�
echo.

set /p choice="������ѡ�� (1/2): "

if "%choice%"=="1" (
    echo �������������� YAYA ����...
    python yaya_voice_server_full.py
) else if "%choice%"=="2" (
    echo ���������򻯰� YAYA ����...
    python yaya_voice_server_simple.py
) else (
    echo ��Чѡ������������...
    python yaya_voice_server_full.py
)

pause
