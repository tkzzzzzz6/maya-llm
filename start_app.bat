@echo off
chcp 65001 >nul
echo ╔════════════════════════════════════════════╗
echo ║   🦆 麻鸭语音助手 v2.0                    ║
echo ║   前后端分离版本                           ║
echo ╚════════════════════════════════════════════╝
echo.
echo 📁 项目结构：
echo    ├── src/backend/   后端逻辑
echo    └── src/frontend/  前端界面
echo.
echo 正在启动...
echo.

python app.py --port 7860

pause

