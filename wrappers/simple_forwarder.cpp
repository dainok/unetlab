
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <signal.h>

#include "iol_functions.h"
#include "include/ts.h"
#include "include/tap.h"

int device_id = -1;                         // Device ID
int tenant_id = -1;                         // Tenant ID
int tsclients_socket[FD_SETSIZE];           // Telnet active clients (socket), tsclients_socket[0] is the index

int child_eth = 2;                          // Ethernet porgroups
int child_ser = 2;                          // Serial portgroups
int taps_number = 0;
int source_tap = -1;  // Number of the source TAP interface;

int  frames_processed = 0;
int  bytes_processed  = 0;

int ts_port = 32777;
int *tapHandles;
char xchangeBuffer[16000];
char *defaultTapPrefix = "vnet";

void usage(char * bin) {
  printf("Usage: %s <standard options>\n", bin);
  printf("Standard Options:\n");
  printf("-T <n>    *Tenant ID\n");
  printf("-D <n>    *Device ID\n");
  printf("-n <n>    *Number of TAP interfaces to try to open to\n");
  printf("-s <n>    *Source TAP interface\n");
  printf("-t <n>     Diagnostic port number. Default is %i\n", ts_port);
  printf("-v <s>     TAP interfaces' prefix. Default is %s\n", defaultTapPrefix);
  printf("* Mandatory option\n");
  printf("WARNING: use the above parameters' order!\n");
  printf("Description: %s translates frames from the source TAP interface to all the others\n", bin);
  printf("Example: %s -T 0 -D 1 -n 50 -s 16 -v vunl\n", bin);
  printf("  will translate frames from 'vunl0_1_16' TAP to all the other TAP interfaces in range [vunl0_1_0 .. vunl0_1_49] that have been successfully open by %s\n\n",bin);
  exit(1);
}

void openTaps() {
  char tapName[256];
  for(int i = 0; i < taps_number; i++) {
    //sprintf(tapName,"vnet%i_%i_%i",tenant_id,device_id,i);
    sprintf( tapName, "%s%i_%i_%i", defaultTapPrefix, tenant_id, device_id, i);
    if (tap_listen(tapName, &tapHandles[i]) != 0 ) {
      if ( i == source_tap ) {
        printf("Failed to open source tap:%s\n", tapName);
        exit(1);
      }
      tapHandles[i] = 0;
    } else {
      printf("Successfully open: %s\n", tapName);
    }
  }
}

int main(int argc, char *argv[]) {
  int rc;
  char client_input = '\0';               // Store single char from client
  fd_set active_fd_set;                   // Contains active FD using in select()
  FD_ZERO(&active_fd_set);
  fd_set read_fd_set;                     // Contains FD selected in current loop
  FD_ZERO(&read_fd_set);
  
  int opt;
  // Adding options to child's CMD line
  while ((opt = getopt(argc, argv, ":T:D:n:s:t:v:")) != -1) {
    switch (opt) {
      case 'T':
        // Mandatory: Tenant ID
        tenant_id = atoi(optarg);
        if (tenant_id < 0) {
          printf("ERR: tenant_id must be integer.\n");
          exit(1);
        }
        break;
      case 'D':
        // Mandatory: Device ID
        device_id = atoi(optarg);
        if (tenant_id < 0) {
          printf("ERR: device_id must be integer.\n");
          exit(1);
        }
        break;
        
        // Mandatory: number of TAP interfaces
      case 'n':
        taps_number = atoi(optarg);
        if (taps_number < 2) {
          printf("Number of TAP interfaces must be greater than 1\n");
          exit(1);
        }
        break;
        
        // Mandatory: Source TAP interface
      case 's':
        source_tap = atoi(optarg);
        if ((source_tap < 0) && (source_tap > taps_number - 1)) {
          printf("Number of TAP interfaces must be greater than 1, and come after -n CLI parameter\n");
          exit(1);
        }
        break;
        
        // Optional: diagnotic TCP port [default: 32777]
      case 't':
        ts_port = atoi(optarg);
        if ((ts_port < 0) || (ts_port > 0xFFFF)) {
          printf("Diagnotic port number must be in range [0..65K]\n");
          exit(1);
        }
        break;

        // Optional: TAP's prefix [default: vnet]
      case 'v':
        defaultTapPrefix = optarg;
        break;

      default:
        usage(argv[0]);
        exit(1);
    }
  }
  
  if (tenant_id < 0) {
    printf("ERR: No tenant id\n");
    usage(argv[0]);
  }
  if (device_id < 0) {
    printf("ERR: No device id\n");
    usage(argv[0]);
  }
  if (taps_number == 0) {
    printf("ERR: No TAPs number\n");
    usage(argv[0]);
  }
  if (source_tap == 0) {
    printf("ERR: No source TAP\n");
    usage(argv[0]);
  }

  
  tapHandles = (int*)calloc(taps_number,sizeof(int));
  
  
  int ts_socket = -1;
  tsclients_socket[0] = 0;
  if ((rc = ts_listen(ts_port, &ts_socket)) != 0) {
    printf("Failed to open TCP socket (%i).\n", rc);
    exit(1);
  }
  
  openTaps();
  
  
  
  FD_SET(ts_socket, &active_fd_set);
  FD_SET(tapHandles[source_tap], &active_fd_set);
  
  // main cycle:
  while(1) {
    read_fd_set = active_fd_set;
    int active_fd = -1;                     // Contains current active FD
    if ((active_fd = select(FD_SETSIZE, &read_fd_set, NULL, NULL, NULL)) <= 0) {
      printf("ERR: failed to select()\n");
      kill(0, SIGTERM);
      break;
    }
    //printf("Select: %i descriptors are ready\n",active_fd);
    
    
    // Check if new client is coming
    if (FD_ISSET(ts_socket, &read_fd_set)) {
      if ((rc = ts_accept(&active_fd_set, ts_socket, "", tsclients_socket, 0)) != 0) {
        printf("ERR: failed to accept a new client (%i).\n", rc);
      } else {
        printf("New telnet client is accepted\n");
      }
    }
    
    
    // Check for output from all telnet clients
    if (ts_receive(&client_input, &read_fd_set, &active_fd_set, tsclients_socket) == 0) {
      //printf("got %i\n",client_input);
      if (client_input == 'p') {  // 'p' stands for "ping"
        printf("Got ping request, replying that we're still alive\n");
        ts_broadcast_string("alive\n", &active_fd_set, tsclients_socket);
      } else if (client_input == 's') { // 's' stands for "stat"
        char statInfo[256];
        snprintf(statInfo, sizeof(statInfo),"Frames: %i Bytes: %i\n",frames_processed,bytes_processed);
        printf("Got stat request, reporting brief statistics: %s",statInfo);
        ts_broadcast_string(statInfo, &active_fd_set, tsclients_socket);
      } 
      
    }
    
    if (FD_ISSET(tapHandles[source_tap],&read_fd_set)) {
      int lenght = read(tapHandles[source_tap],xchangeBuffer,sizeof(xchangeBuffer));
      if (lenght > 0) {
        frames_processed++;
        bytes_processed  += lenght;
        for (int i = 1; i < taps_number; i++) {
          if ((i != source_tap) && (tapHandles[i] != 0)) {
            if (write(tapHandles[i],xchangeBuffer,lenght) != lenght) {
              printf("Failed to write data to TAP n %i\n",i);
            }
          }
        }
      }
    }
    
  }
  
  return 0;
}

