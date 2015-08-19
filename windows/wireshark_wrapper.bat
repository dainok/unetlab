@ECHO OFF
SET USERNAME="root"
SET PASSWORD="unl"

SET S=%1
SET S=%S:capture://=%
FOR /f "tokens=1,2 delims=/ " %%a IN ("%S%") DO SET HOST=%%a&SET INT=%%b
IF "%INT%" == "pnet0" SET FILTER=" not port 22"

ECHO "Connecting to %USERNAME%@%HOST%..."

"C:\Program Files\UNetLab\plink.exe" -ssh -pw %PASSWORD% %USERNAME%@%HOST% "tcpdump -l -u -i %INT% -s 0 -w -%FILTER%" | "C:\Program Files\Wireshark\Wireshark.exe" -k -i -
