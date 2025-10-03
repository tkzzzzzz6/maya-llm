@echo off
chcp 65001 >nul
echo ╔═══════════════════════════════════════╗
echo ║     🦆 麻鸭语音助手 Web UI           ║
echo ║   Maya Voice Assistant v1.0          ║
echo ╚═══════════════════════════════════════╝
echo.
echo 正在启动 Web 界面...
echo.
echo 提示：
echo   - 首次运行需要下载模型（约2-3GB），请耐心等待
echo   - 启动后在浏览器访问: http://localhost:7860
echo   - 按 Ctrl+C 可停止服务
echo.

python maya_webui.py --port 7860

pause

