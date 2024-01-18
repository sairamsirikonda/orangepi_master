#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>
#include <string.h>

// Define the GPIO pin
#define DE_RE_PIN "GPIO7"  // Replace with the appropriate GPIO pin

// Function to send a Modbus request and receive the response
void send_modbus_request(int fd, uint16_t register_number);

int main() {
    // Open the serial port
    int serial_fd = open("/dev/ttyS1", O_RDWR | O_NOCTTY);
    if (serial_fd == -1) {
        perror("Error opening serial port");
        exit(EXIT_FAILURE);
    }

    // Set up the GPIO pin
    int gpio_fd = open(DE_RE_PIN, O_WRONLY);
    if (gpio_fd == -1) {
        perror("Error opening GPIO pin");
        close(serial_fd);
        exit(EXIT_FAILURE);
    }

    // Example usage
    uint16_t registers[] = {40001, 40003, 40005};
    size_t num_registers = sizeof(registers) / sizeof(registers[0]);

    for (size_t i = 0; i < num_registers; ++i) {
        send_modbus_request(serial_fd, registers[i]);
    }

    // Close file descriptors
    close(gpio_fd);
    close(serial_fd);

    return 0;
}

// Function to send a Modbus request and receive the response
void send_modbus_request(int fd, uint16_t register_number) {
    // Enable transmission (set GPIO pin low)
    write(fd, "0", 1);

    // Convert register to Modbus address
    uint16_t modbus_address = register_number - 1;

    // Construct the Modbus RTU request
    uint8_t command[] = {1, 3, (modbus_address >> 8) & 0xFF, modbus_address & 0xFF, 0, 2};  // Modify as needed

    // Print the Modbus request being sent (for debugging)
    printf("Sent command:");
    for (size_t i = 0; i < sizeof(command) / sizeof(command[0]); ++i) {
        printf(" 0x%02X", command[i]);
    }
    printf("\n");

    // Send the Modbus request
    write(fd, command, sizeof(command));

    // Wait for transmission to complete
    usleep(100000);  // 100 ms (adjust as needed)

    // Disable transmission (set GPIO pin high)
    write(fd, "1", 1);

    // Receive the Modbus response
    uint8_t response[8];
    ssize_t num_bytes = read(fd, response, sizeof(response));

    // Print the Modbus response received (for debugging)
    printf("Received response:");
    for (ssize_t i = 0; i < num_bytes; ++i) {
        printf(" 0x%02X", response[i]);
    }
    printf("\n");

    // Process the response
    if (num_bytes > 0) {
        // Extract raw value from Modbus response
        uint32_t raw_value = (response[3] << 24) | (response[4] << 16) | (response[5] << 8) | response[6];

        // Assuming a scaling factor of 0.1 (adjust based on device documentation)
        double scaling_factor = 0.1;
        double gas_concentration_ppm = raw_value * scaling_factor;

        printf("Gas Concentration at register %d: %f PPM\n", register_number, gas_concentration_ppm);
    } else {
        printf("No response received for register %d\n", register_number);
    }
}
