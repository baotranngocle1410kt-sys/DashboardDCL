@echo off
title Cap Nhat Dashboard DCL
chcp 65001 > nul
cd /d "%~dp0"
python Cap_Nhat_Web.py
pause
