@echo off
chcp 65001
cd /d "C:\Users\ldkxn\Desktop\cursor\my-project\lifeinsight\paipan"
call ..\..\venv\Scripts\activate.bat
python triple_chart_parser.py --birth-date 1998-09-26 --birth-time 10:00 --timezone +8 --longitude 123.4 --latitude 41.8 --gender 0 --save-file --location Shenyang
echo.
echo 运行完成！
pause 