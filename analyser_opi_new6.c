#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// Function prototypes
void send_modbus_request(int serial_port, uint16_t register_address);
void process_modbus_response(uint16_t register_address, uint8_t *response);
void process_process_value(uint8_t *response);
void process_monitor_status(uint8_t *response);
void process_active_alarm(uint8_t *response);
void process_active_relay(uint8_t *response);
void process_error_status(uint8_t *response);

int main() {
    // Open the serial port (replace "/dev/ttyS0" with your actual serial port)
    int serial_port = open_serial_port("/dev/ttyS0", 9600, 1);

    // Example usage
    uint16_t registers[] = {40001, 40003, 40004, 40005, 40006};
    size_t num_registers = sizeof(registers) / sizeof(registers[0]);

    for (size_t i = 0; i < num_registers; i++) {
        send_modbus_request(serial_port, registers[i]);
    }

    // Close the serial port
    close(serial_port);

    return 0;
}

// Other functions remain the same...


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

    // Process the response based on the register address
    process_modbus_response(register_address, response);
}

// Function to process Modbus response based on register address
void process_modbus_response(uint16_t register_address, uint8_t *response) {
    switch (register_address) {
        case 40001:
            process_process_value(response);
            break;
        case 40003:
            process_monitor_status(response);
            break;
        case 40004:
            process_active_alarm(response);
            break;
        case 40005:
            process_active_relay(response);
            break;
        case 40006:
            process_error_status(response);
            break;
        default:
            printf("Unhandled register address: %d\n", register_address);
    }
}

// Functions to process specific Modbus responses
void process_process_value(uint8_t *response) {
    // Assuming a float32_t value at registers 40001 and 40002
    uint32_t raw_value = (response[3] << 24) | (response[4] << 16) | (response[5] << 8) | response[6];
    float process_value = *((float *)&raw_value);
    printf("Process Value: %f\n", process_value);
}

void process_monitor_status(uint8_t *response) {
    // Assuming a uint16_t value at registers 40003 and 40004
    uint16_t monitor_status = (response[3] << 8) | response[4];
    printf("Monitor Status: %d\n", monitor_status);
}

void process_active_alarm(uint8_t *response) {
    // Assuming a uint16_t value at registers 40004 and 40005
    uint16_t active_alarm = (response[3] << 8) | response[4];
    printf("Active Alarm: %d\n", active_alarm);
}

void process_active_relay(uint8_t *response) {
    // Assuming a uint16_t value at registers 40005 and 40006
    uint16_t active_relay = (response[3] << 8) | response[4];
    printf("Active Relay: %d\n", active_relay);
}

void process_error_status(uint8_t *response) {
    // Assuming a uint16_t value at registers 40006 and 40007
    uint16_t error_status = (response[3] << 8) | response[4];
    printf("Error Status: %d\n", error_status);
}

int main() {
    // Open the serial port
    int serial_port = open_serial_port("/dev/ttyS0");

    // Set serial port parameters
    set_serial_params(serial_port);

    // Example usage
    uint16_t registers[] = {
