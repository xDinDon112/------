@echo off
setlocal
pushd "%~dp0"
py -3 -c "import sys; sys.exit(sys.version_info < (3, 10))" >nul 2>&1
if not errorlevel 1 goto use_py
python -c "import sys; sys.exit(sys.version_info < (3, 10))" >nul 2>&1
if not errorlevel 1 goto use_python
echo Install Python 3.10 or newer. For a quick view, open the HTML file.
goto failed

:use_py
py -3 start_local.py
if errorlevel 1 goto failed
goto done

:use_python
python start_local.py
if errorlevel 1 goto failed
goto done

:failed
pause
popd
exit /b 1

:done
popd
