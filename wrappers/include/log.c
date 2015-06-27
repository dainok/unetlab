#include "log.h"

#include <stdarg.h>
#include <time.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/time.h>

#include "params.h"

extern int device_id;
extern int tenant_id;


int sLogLevel = LLINFO;


const char * sLevels[] = {"   ", "ERR", "WRN", "INF", "DBG", "VRB"};

void UNLLog(int nLevel, const char * szFormat, ...) {
  if (nLevel > sLogLevel) {
    return;
  }
  va_list args;
  va_start(args, szFormat);

  
  struct timeval  tv;
  gettimeofday(&tv, NULL);
  
  struct tm * curTime = gmtime(&(tv.tv_sec));
  printf("%i/%i %i:%i:%i.%i %s\t", curTime->tm_mday, curTime->tm_mon, curTime->tm_hour, curTime->tm_min, curTime->tm_sec, (int)((tv.tv_usec)) / 1000, sLevels[nLevel]);
  vprintf(szFormat,args);
  va_end(args);
  
}
/*
// Extended
void UNLLogE(int nLevel, const char * szFormat, ...) {
  if (nLevel > sLogLevel) {
    return;
  }
  va_list args;
  va_start(args, szFormat);
  time_t curTicks;
  time(&curTicks);
  struct tm * curTime = gmtime(&curTicks);
  printf("%i/%i %i:%i:%i %s %i:%i\t", curTime->tm_mday, curTime->tm_mon, curTime->tm_hour, curTime->tm_min, curTime->tm_sec, sLevels[nLevel], tenant_id, device_id);
  vprintf(szFormat,args);
  va_end(args);
}
*/
void CheckLogLevelFileTrigger(const char * szFileTrigger, int logLevel) {
  if ( access(szFileTrigger,F_OK) != -1 ) {
    sLogLevel = logLevel;
  }
}