#include <stdio.h>
#include <stdlib.h>
#include <modbus/modbus.h>
#include <errno.h>

#define RS485_DEVICE "/dev/ttyS1"
#define BAUD_RATE 9600
#define SLAVE_ID 1
#define STARTING_ADDRESS 40001
#define QUANTITY_OF_REGISTERS 2

int main() {
    modbus_t *ctx;
    float value;

    // Initialize Modbus context with RTU mode
    ctx = modbus_new_rtu(RS485_DEVICE, BAUD_RATE, 'O', 7, 1);  // 'O' for ASCII, 7 data bits, 1 stop bit
    if (ctx == NULL) {
        fprintf(stderr, "Unable to create Modbus context: %s\n", modbus_strerror(errno));
        return 1;
    }

    // Set Modbus slave ID
    modbus_set_slave(ctx, SLAVE_ID);

    // Connect to Modbus slave
    if (modbus_connect(ctx) == -1) {
        fprintf(stderr, "Modbus connection failed: %s\n", modbus_strerror(errno));
        modbus_free(ctx);
        return 1;
    }

    uint16_t raw_data[QUANTITY_OF_REGISTERS];

    // Read Modbus registers
    int read_result = modbus_read_registers(ctx, STARTING_ADDRESS, QUANTITY_OF_REGISTERS, raw_data);
    if (read_result == -1) {
        fprintf(stderr, "Modbus read error: %s\n", modbus_strerror(errno));
        modbus_close(ctx);
        modbus_free(ctx);
        return 1;
    } else if (read_result != QUANTITY_OF_REGISTERS) {
        fprintf(stderr, "Unexpected number of registers read: %d\n", read_result);
        modbus_close(ctx);
        modbus_free(ctx);
        return 1;
    }

    // Interpret the raw data as a float
    value = *((float*)raw_data);

    printf("Received float value: %f\n", value);

    // Close Modbus connection
    modbus_close(ctx);
    modbus_free(ctx);

    return 0;
}
