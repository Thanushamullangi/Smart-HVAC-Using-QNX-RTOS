#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/dispatch.h>
#include <sys/neutrino.h>
#include <errno.h>

#define SERVER_NAME "smart_hvac_test"

typedef struct {
    int temperature;
    int co2;
    int occupancy;
} HVAC_Message;

typedef struct {
    int status;
    char response[150];
} HVAC_Reply;

int main(void)
{
    name_attach_t *attach;
    HVAC_Message msg;
    HVAC_Reply reply;

    attach = name_attach(NULL, SERVER_NAME, 0);
    if (attach == NULL) {
        int err = errno;
        printf("Server attachment failed!\n");
        printf("Error code: %d\n", err);
        printf("Error details: %s\n", strerror(err));
        return EXIT_FAILURE;
    }

    printf("=================================\n");
    printf("   SMART HVAC IPC SERVER\n");
    printf("=================================\n");
    printf("Server started successfully!\n");
    printf("Waiting for HVAC client...\n");

    while (1) {
        int rcvid = MsgReceive(attach->chid, &msg, sizeof(msg), NULL);
        if (rcvid == -1) {
            perror("MsgReceive failed");
            continue;
        }

        printf("\n----- HVAC DATA RECEIVED -----\n");
        printf("Temperature : %d C\n", msg.temperature);
        printf("CO2 Level   : %d ppm\n", msg.co2);
        printf("Occupancy   : %d people\n", msg.occupancy);

        reply.status = 0;
        if (msg.temperature > 30 || msg.co2 > 1000) {
            strcpy(reply.response,
                   "WARNING: High HVAC load! Activate cooling and ventilation.");
        } else if (msg.occupancy == 0) {
            strcpy(reply.response,
                   "Room empty. Switch HVAC to energy-saving mode.");
        } else {
            strcpy(reply.response,
                   "HVAC operating normally. Conditions are comfortable.");
        }

        printf("HVAC Decision: %s\n", reply.response);
        if (MsgReply(rcvid, EOK, &reply, sizeof(reply)) == -1) {
            perror("MsgReply failed");
        }
    }

    name_detach(attach, 0);
    return EXIT_SUCCESS;
}
