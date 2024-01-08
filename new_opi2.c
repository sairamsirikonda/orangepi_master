#include <stdio.h>
#include <stdlib.h>
#include <modbus/modbus.h>
#include <errno.h>  // Add this line to include the errno header

#define RS485_DEVICE "/dev/ttyS1"
#define BAUD_RATE 9600
#define SLAVE_ID 1
#define STARTING_ADDRESS 40001
#define QUANTITY_OF_REGISTERS 2

int main() {
    modbus_t *ctx;
    float value;

    ctx = modbus_new_rtu(RS485_DEVICE, BAUD_RATE, 'N', 8, 1);
    if (ctx == NULL) {
        fprintf(stderr, "Unable to create Modbus context\n");
        return 1;
    }

    modbus_set_slave(ctx, SLAVE_ID);

    if (modbus_connect(ctx) == -1) {
        fprintf(stderr, "Modbus connection failed: %s\n", modbus_strerror(errno));
        modbus_free(ctx);
        return 1;
    }

    uint16_t raw_data[QUANTITY_OF_REGISTERS];

    if (modbus_read_registers(ctx, STARTING_ADDRESS, QUANTITY_OF_REGISTERS, raw_data) == -1) {
        fprintf(stderr, "Modbus read error: %s\n", modbus_strerror(errno));
        modbus_close(ctx);
        modbus_free(ctx);
        return 1;
    }

    value = *((float*)raw_data);

    printf("Received float value: %f\n", value);

    modbus_close(ctx);
    modbus_free(ctx);

    return 0;
}
