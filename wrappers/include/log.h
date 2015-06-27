#ifndef _LOG_H_
#define _LOG_H_

// UNL Log Levels:
#define LLERROR     1
#define LLWARNING   2
#define LLINFO      3
#define LLDEBUG     4
#define LLVERBOSE   5

void CheckLogLevelFileTrigger(const char * szFileTrigger, int logLevel);

void UNLLog(int nLevel, const char * szFormat, ...);
void UNLLogE(int nLevel, const char * szFormat, ...); // Extended

#endif //_LOG_H_
