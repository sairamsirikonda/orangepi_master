#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>
#include <string.h>

// Define the GPIO pin
#define DE_RE_PIN "/sys/class/gpio/gpio7/value"  // Modify for GPIO pin 7

// Open the serial port
int open_serial_port(const char *port_name) {
    int port = open(port_name, O_RDWR | O_NOCTTY | O_NDELAY);
    if (port == -1) {
        perror("Error opening serial port");
        exit(EXIT_FAILURE);
    }
    return port;
}

// Set serial port parameters
void set_serial_params(int port) {
    struct termios serial_params;
    tcgetattr(port, &serial_params);

    // Set baudrate (modify as needed)
    cfsetispeed(&serial_params, B9600);
    cfsetospeed(&serial_params, B9600);

    // 8N1 (8 data bits, no parity, 1 stop bit)
    serial_params.c_cflag &= ~PARENB;
    serial_params.c_cflag &= ~CSTOPB;
    serial_params.c_cflag &= ~CSIZE;
    serial_params.c_cflag |= CS8;

    tcsetattr(port, TCSANOW, &serial_params);
}

// Function to send a Modbus request and receive the response
void send_modbus_request(int port, uint16_t register_address) {
    // Enable transmission (DE and RE low)
    int de_re_fd = open(DE_RE_PIN, O_WRONLY);
    write(de_re_fd, "0", 1);
    close(de_re_fd);

    // Construct the Modbus RTU request
    uint8_t command[] = {0x01, 0x03, (uint8_t)((register_address >> 8) & 0xFF), (uint8_t)(register_address & 0xFF), 0x00, 0x02};

    // Print the Modbus request being sent
    printf("Sent command:");
    for (int i = 0; i < sizeof(command) / sizeof(command[0]); i++) {
        printf(" 0x%02X", command[i]);
    }
    printf("\n");

    // Send the Modbus request
    write(port, command, sizeof(command));

    // Wait for transmission to complete
    tcdrain(port);

    // Disable transmission (DE and RE high)
    de_re_fd = open(DE_RE_PIN, O_WRONLY);
    write(de_re_fd, "1", 1);
    close(de_re_fd);

    // Receive the Modbus response
    uint8_t response[8];
    read(port, response, sizeof(response));

    // Print the Modbus response received
    printf("Received response:");
    for (int i = 0; i < sizeof(response) / sizeof(response[0]); i++) {
        printf(" 0x%02X", response[i]);
    }
    printf("\n");
}

int main() {
    // Open the serial port
    int serial_port = open_serial_port("/dev/ttyS0");

    // Set serial port parameters
    set_serial_params(serial_port);

    // Example usage
    uint16_t registers[] = {40001, 40003, 40005};
    for (int i = 0; i < sizeof(registers) / sizeof(registers[0]); i++) {
        send_modbus_request(serial_port, registers[i]);
    }

    // Close the serial port
    close(serial_port);

    return 0;
}
