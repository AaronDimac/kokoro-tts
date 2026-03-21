@echo off
powershell -ExecutionPolicy Bypass -File "%~dp0generate_body_wavs.ps1" %*
