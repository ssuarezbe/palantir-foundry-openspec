@echo off
rem Runs the bundled OpenSpec CLI with telemetry off. Needs Node 20+ on PATH.
set OPENSPEC_TELEMETRY=0
node "%~dp0..\openspec-1.16.0\dist\cli\openspec.mjs" %*
