@echo off
chcp 65001 >nul
title 软件启动器

cd /d "%~dp0"
python start.py
pause
