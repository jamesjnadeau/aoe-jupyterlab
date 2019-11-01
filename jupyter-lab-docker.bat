REM @echo off

SET myWork=%USERPROFILE%\Code\AOE\EDE\

docker run -p 8888:8888 -e JUPYTER_ENABLE_LAB=yes -v %myWork%:/home/jovyan/work jupyter/scipy-notebook start-notebook.sh  

cmd /k