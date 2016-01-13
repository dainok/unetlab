@ECHO OFF

REM http://www.dostips.com/DtTipsStringManipulation.php#Snippets.RemoveBothEnds
REM http://ss64.com/nt/syntax-replace.html

SET S=%1
SET S=%S:docker://=%
SET S=tcp://%S%

REM UNetLab Host (tcp://unl.example.com:4243)
SET _endbit=%S:*4243=%
CALL SET H=%%S:%_endbit%=%%
SET H=%H:4243*=%

REM Docker ID (7a1acefa-aa8c-492e-9eb2-4362e41b621c-1-1)
SET _endbit=%S:*?=%
CALL SET I=%%S:%_endbit%=%%
SET I=%I:*4243/=%
SET I=%I:~0,-1%

REM Node Name
SET N=%S:*?=%

start "%N%" "C:\Program Files\UNetLab\docker.exe" -H=%H% attach %I%
