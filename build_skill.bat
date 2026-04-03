@echo off
setlocal

cd /d %~dp0
python .\build_skill.py %*
if errorlevel 1 (
  echo Build failed.
  exit /b 1
)

echo Build finished.
exit /b 0
