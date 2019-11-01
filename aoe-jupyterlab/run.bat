REM @echo off

SET myWork=%USERPROFILE%\Code\AOE\EDE\

docker run -p 8888:8888 -v %myWork%:/home/jovyan/work -t aoe-jupyterlab:latest

cmd /k