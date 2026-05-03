@echo off
chcp 936 >nul

echo ====================================
echo 启动菜单
echo ====================================
echo.
echo 1 - 启动第一个软件
echo 2 - 启动第二个软件  
echo 3 - 退出
echo.

set /p n=选择 (1-3):

if "%n%"=="1" goto s1
if "%n%"=="2" goto s2
if "%n%"=="3" exit /b
goto end

:s1
echo Starting Software 1...
start cmd /k "cd Software1 && streamlit run app.py --server.port 8502"
goto end

:s2
echo Starting Software 2...
start cmd /k "cd Software2 && streamlit run app.py --server.port 8501"
goto end

:end
pause
