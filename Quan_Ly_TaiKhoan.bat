@echo off
chcp 65001 >nul
title Quản lý Tài khoản Dashboard ĐCL
cd /d "%~dp0"
python manage_users.py
pause
