@echo off
chcp 65001 >nul
cd /d "%~dp0"
title MIS PRUEBAS DE EUCLIDES
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

:correr
cls
%PYCMD% probar.py --archivo mis_pruebas.txt
echo.
echo   [A] abrir mis_pruebas.txt para escribir pruebas
echo   [R] repetir las pruebas
echo   [S] salir
choice /c ARS /n /m "  Que hago? "
if errorlevel 3 exit /b 0
if errorlevel 2 goto correr
start /wait notepad "%~dp0mis_pruebas.txt"
goto correr
