/**
 * wrappers/include/ts.c
 *
 * Terminal server functions for wrappers.
 *
 * @author Andrea Dainese <andrea.dainese@gmail.com>
 * @copyright 2014-2016 Andrea Dainese
 * @license BSD-3-Clause https://github.com/dainok/unetlab/blob/master/LICENSE
 * @link http://www.unetlab.com/
 * @version 20160719
 */

#include <errno.h>
#include <netinet/in.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

#include "params.h"
#include "log.h"
#include "ts.h"

//--[ Telnet Commands ]--------------------------------------------------------
#define IS       0 // Sub-process negotiation IS command
#define SEND     1 // Sub-process negotiation SEND command
#define SE     240 // End of subnegotiation parameters
#define NOP    241 // No operation
#define DATMK  242 // Data stream portion of a sync.
#define BREAK  243 // NVT Character BRK
#define IP     244 // Interrupt Process
#define AO     245 // Abort Output
#define AYT    246 // Are you there
#define EC     247 // Erase Character
#define EL     248 // Erase Line
#define GA     249 // The Go Ahead Signal
#define SB     250 // Sub-option to follow
#define WILL   251 // Will; request or confirm option begin
#define WONT   252 // Wont; deny option request
#define DO     253 // Do = Request or confirm remote option
#define DONT   254 // Don't = Demand or confirm option halt
#define IAC    255 // Interpret as Command
//--[ Telnet Options ]---------------------------------------------------------
#define BINARY   0 // Transmit Binary
#define ECHO     1 // Echo characters back to sender
#define RECON    2 // Reconnection
#define SGA      3 // Suppress Go-Ahead
#define TTYPE   24 // Terminal Type
#define NAWS    31 // Negotiate About Window Size
#define LINEMO  34 // Line Mode

extern int device_id;
extern int tenant_id;

// Terminal Server: listen
int ts_listen(int port, int *server_socket) {
    int rc = -1;
    int y = 1;
    struct sockaddr_in6 server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    
    // Opening socket
    *server_socket = socket(AF_INET6, SOCK_STREAM, 0);
    if (*server_socket < 0) {
        rc = 1;
        UNLLog(LLERROR, "Error while setting TS (socket).  ERR: %s (%i).\n", strerror(errno), rc);
        return rc;
    }

    // Setting options
    server_addr.sin6_family = AF_INET6;
    server_addr.sin6_port = htons(port);
    server_addr.sin6_addr = in6addr_any;
    if (setsockopt(*server_socket, SOL_SOCKET, SO_REUSEADDR, &y, sizeof(int)) < 0) {
        rc = 2;
        UNLLog(LLERROR, "Error while setting TS (setsockopt). ERR: %s (%i).\n", strerror(errno), rc);
        return rc;
    }

    // Binding (checking if address is already in use)
    if (bind(*server_socket, (struct sockaddr *) &server_addr, sizeof(server_addr)) < 0) {
        rc = 3;
        UNLLog(LLERROR, "Error while setting TS (binding). ERR: %s (%i).\n", strerror(errno), rc);
        return rc;
    }
    if (listen(*server_socket, 5) < 0) {
        rc = 4;
        UNLLog(LLERROR, "Error while setting TS (listening). ERR: %s (%i).\n", strerror(errno), rc);
        return rc;
    }
    UNLLog(LLINFO, "TS configured.\n");
    return 0;
}

// Terminal Server: accept new connection
int ts_accept(fd_set *fd_set, int server_socket, char *xtitle, int *client_socket, int sendHeaders) {
    unsigned char header[] = {
        IAC, WILL, ECHO,        // Sending IAC WILL ECHO
        IAC, WILL, SGA,         // Sending IAC WILL SGA
        IAC, WILL, BINARY,      // Sending IAC WILL BINARY
        IAC, DO, BINARY,        // Requesting BINARY mode (fix ^@ and show run)
        '\033', ']', '0', ';'   // Sending title header
    };
    char trailer[] = {'\007'};  // Sending title trailer
    int newclient_socket;
    int rc = -1;
    struct sockaddr_in6 client_addr;
    memset(&client_addr, 0, sizeof(client_addr));
    socklen_t client_addrlen = sizeof(client_addr);

    if ((newclient_socket = accept(server_socket, (struct sockaddr *) &client_addr, &client_addrlen)) < 0) {
        // Failed to accept
        rc = 1;
        UNLLog(LLERROR, "Failed to accept new TS client (accept). ERR: %s (%i).\n", strerror(errno), rc);
        close(newclient_socket);
        return rc;
    } else {
        if (client_socket[0] + 1 > FD_SETSIZE) {
            // Maximum FD reached
            rc = 2;
            UNLLog(LLERROR, "Failed to accept new TS client (MAX FD). ERR: %s (%i).\n", strerror(errno), rc);
            close(newclient_socket);
            return rc;
        }
        // Initialize the new client
        if (sendHeaders) {
            send(newclient_socket, &header, sizeof(header) / sizeof(header[0]), 0);
            send(newclient_socket, xtitle, strlen(xtitle), 0);
	    send(newclient_socket, &trailer, sizeof(trailer) / sizeof(trailer[0]), 0);
	}
        // Add client to the FDSET
        UNLLog(LLINFO, "Adding client socket descriptor (%i).\n", newclient_socket);
        FD_SET(newclient_socket, fd_set);
        // Add client to the active client list
        client_socket[++client_socket[0]] = newclient_socket;
    }
    UNLLog(LLINFO, "New client connected (%i), total is %i.\n", newclient_socket, client_socket[0]);
    return 0;
}

void ts_broadcast_string(char * string, fd_set *fd_set, int *client_socket) {
  while(*string != 0) {
    ts_broadcast(*string,fd_set,client_socket);
    string++;
  }
}

// Terminal Server: broadcast a char to all clients
void ts_broadcast(char c, fd_set *fd_set, int *client_socket) {
    int i = -1;

    for (i = 1; i <= client_socket[0]; i++) {
        if (send(client_socket[i], &c, 1, 0) < 0) {
            // Failed to send, remove client from FD SET
            UNLLog(LLERROR, "Failed to send data to client, closing it (%i).\n", client_socket[i]);
            close(client_socket[i]);
            FD_CLR(client_socket[i], fd_set);
            // Remove client from client_socket array
            if (i == client_socket[0]) {
                // Last client is failed, simply decrement the total
                client_socket[0]--;
            } else {
                // Other clients follows, swap with the last
                client_socket[i] = client_socket[client_socket[0]];
                client_socket[0]--;
                // Must send to the current position again
                i--;
            }
        }
    }
}

int close_client(int * client_socket, int i, fd_set * fd_active) {
    UNLLog(LLERROR, "Failed to receive data from client, closing it (%i).\n", client_socket[i]);
    close(client_socket[i]);
    FD_CLR(client_socket[i], fd_active);
    // Remove client from client_socket array
    if (i == client_socket[0]) {
        // Last client is failed, simply decrement the total
        client_socket[0]--;
        return 0;
    } else {
        // Other clients follows, swap with the last
        client_socket[i] = client_socket[client_socket[0]];
        client_socket[0]--;
        // Must select() the current position again
        //i--;
        return 1;
    }
}

// Terminal Server: receive a char from a client
int ts_receive(unsigned char *c, fd_set *fd_read, fd_set *fd_active, int *client_socket) {
    int i;

    for (i = 1; i <= client_socket[0]; i++) {
        if (FD_ISSET(client_socket[i], fd_read)) {
            if (recv(client_socket[i], c, 1, 0) <= 0) {
                // Failed to receive, remove client from FD SET
                if (close_client(client_socket,i,fd_active)) {
                  i--;
                }
/*                
                UNLLog(LLERROR, "Failed to receive data from client, closing it (%i).\n", client_socket[i]);
                close(client_socket[i]);
                FD_CLR(client_socket[i], fd_active);
                // Remove client from client_socket array
                if (i == client_socket[0]) {
                    // Last client is failed, simply decrement the total
                    client_socket[0]--;
                } else {
                    // Other clients follows, swap with the last
                    client_socket[i] = client_socket[client_socket[0]];
                    client_socket[0]--;
                    // Must select() the current position again
                    i--;
                }
*/                
            } else {
                // Whar are invalid characters??? Commented out:
                //if (*c < 0) {
                //    // Received invalid char
                //    return 1;
                //}
                if (*c == IAC) {
                    // Received telnet command, skip one more command
                    char devNull[2];
                    if (recv(client_socket[i], (void*)devNull, 2, 0) <= 0) { 
                      close_client(client_socket,i,fd_active);
                    }
                    return 1;
                }
                return 0;
            }
        }
    }
    return 1;
}
