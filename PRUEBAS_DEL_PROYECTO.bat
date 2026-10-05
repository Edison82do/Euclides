@echo off
chcp 65001 >nul
cd /d "%~dp0"
title TODAS LAS PRUEBAS DE EUCLIDES
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

echo.
echo   [R] rapido  (unos segundos: fronteras + muestra fija)
echo   [H] hierro  (el rango entero, numero a numero: TARDA: unos 15-30 minutos)
choice /c RH /n /m "  Cual? "
if errorlevel 2 (
  %PYCMD% pruebas\correr_todas.py --hierro
) else (
  %PYCMD% pruebas\correr_todas.py
)
echo.
echo   La salida entera de cada archivo queda en pruebas\ultima_salida.txt
pause
