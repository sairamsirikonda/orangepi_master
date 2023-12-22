#include <stdio.h>
#include <modbus.h>

int main() {
    modbus_t *ctx;
    uint16_t tab_reg[32];

    // Modbus context initialization
    ctx = modbus_new_rtu("/dev/ttyS0", 9600, 'N', 8, 1);
    if (ctx == NULL) {
        fprintf(stderr, "Unable to create the libmodbus context\n");
        return -1;
    }

    // Connect to the Modbus device (replace the Modbus address with the correct one)
    if (modbus_set_slave(ctx, 1) == -1) {
        fprintf(stderr, "modbus_set_slave: %s\n", modbus_strerror(errno));
        modbus_free(ctx);
        return -1;
    }

    if (modbus_connect(ctx) == -1) {
        fprintf(stderr, "Connection failed: %s\n", modbus_strerror(errno));
        modbus_free(ctx);
        return -1;
    }

    // Read from Modbus address 40001 (holding register) with a length of 2
    int rc = modbus_read_registers(ctx, 40001, 2, tab_reg);
    if (rc == -1) {
        fprintf(stderr, "Read failed: %s\n", modbus_strerror(errno));
        modbus_close(ctx);
        modbus_free(ctx);
        return -1;
    }

    // Print the received values
    printf("Data read: %d, %d\n", tab_reg[0], tab_reg[1]);

    // Disconnect and clean up
    modbus_close(ctx);
    modbus_free(ctx);

    return 0;
}
