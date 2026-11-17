@echo off
chcp 65001 >nul
cd /d "%~dp0"
py -m pip install -r requirements.txt
if errorlevel 1 (
  echo Não foi possível instalar as dependências. Verifique se o Python está instalado.
  pause
  exit /b 1
)
py app.py
pause
