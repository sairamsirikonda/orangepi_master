#include <stdio.h>
#include <stdlib.h>
#include <modbus/modbus.h>

#define RS485_DEVICE "/dev/ttyS1"  // Adjust the serial device based on your Orange Pi configuration
#define BAUD_RATE 9600             // Adjust the baud rate based on your gas analyzer's specifications
#define SLAVE_ID 1                 // Adjust the Modbus slave ID based on your gas analyzer's configuration
#define STARTING_ADDRESS 40001     // Starting address for reading data
#define QUANTITY_OF_REGISTERS 2    // Number of registers to read (assuming a float is 2 registers)

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

    // Assuming raw_data contains two 16-bit values that represent a float
    value = *((float*)raw_data);

    printf("Received float value: %f\n", value);

    modbus_close(ctx);
    modbus_free(ctx);

    return 0;
}
