@echo off
chcp 65001 >nul
cd /d "%~dp0"
title PROBADOR DE EUCLIDES

set PYCMD=
where py >nul 2>nul && set PYCMD=py -3
if "%PYCMD%"=="" if exist "C:\Program Files\Python312\python.exe" set PYCMD="C:\Program Files\Python312\python.exe"
if "%PYCMD%"=="" if exist "C:\Program Files\Python311\python.exe" set PYCMD="C:\Program Files\Python311\python.exe"

if "%PYCMD%"=="" (
  echo.
  echo No encuentro Python en este equipo.
  echo Instala Python desde python.org y vuelve a intentarlo.
  echo.
  pause
  exit /b 1
)

%PYCMD% probar.py
echo.
pause
