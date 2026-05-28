@echo off
rem -----------------------------------------------------------------------------
rem Gradle startup script for Windows
rem -----------------------------------------------------------------------------
setlocal

set DIRNAME=%~dp0
set PRG=%~dpnx0

java -jar "%DIRNAME%gradle\wrapper\gradle-wrapper.jar" %*
