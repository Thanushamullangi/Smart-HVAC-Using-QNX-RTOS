#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/dispatch.h>
#include <sys/neutrino.h>

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
    int coid;
    HVAC_Message msg;
    HVAC_Reply reply;

    printf("=================================\n");
    printf("   SMART HVAC IPC CLIENT\n");
    printf("=================================\n");

    coid = name_open(SERVER_NAME, 0);
    if (coid == -1) {
        perror("Connection to HVAC server failed");
        return EXIT_FAILURE;
    }

    printf("Connected to HVAC server!\n");

    /* Sample values. Change these to test other decision scenarios. */
    msg.temperature = 24;
    msg.co2 = 500;
    msg.occupancy = 0;

    printf("\nSending HVAC sensor data...\n");
    printf("Temperature: %d C\n", msg.temperature);
    printf("CO2: %d ppm\n", msg.co2);
    printf("Occupancy: %d people\n", msg.occupancy);

    if (MsgSend(coid, &msg, sizeof(msg), &reply, sizeof(reply)) == -1) {
        perror("Message sending failed");
        name_close(coid);
        return EXIT_FAILURE;
    }

    printf("\n========== SERVER RESPONSE ==========\n");
    printf("%s\n", reply.response);

    name_close(coid);
    return EXIT_SUCCESS;
}
