@ECHO OFF

SET S=%1
SET S=%S:docker://=%
SET S=tcp://%S%
SET _endbit=%S:*4243=%
CALL SET H=%%S:%_endbit%=%%
SET H=%H:4243*=%
SET N=%S%
SET N=%N:*4243/=%
start "Docker Console" "C:\Program Files\UNetLab\docker.exe" -H=%H% attach %N%
