#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>

#define DE_RE_PIN "/sys/class/gpio/gpio7/value"
#define B9600     9600
#define TCSANOW   0

void send_modbus_request(int serial_port, uint16_t register_address);
void process_modbus_response(uint16_t register_address, uint8_t *response);
void process_process_value(uint8_t *response);
void process_monitor_status(uint8_t *response);
void process_active_alarm(uint8_t *response);
void process_active_relay(uint8_t *response);
void process_error_status(uint8_t *response);

int main() {
    int serial_port = open("/dev/ttyS1", O_RDWR);
    if (serial_port == -1) {
        perror("Error opening serial port");
        return 1;
    }

    struct termios serial_params;
    if (set_serial_params(serial_port, B9600, &serial_params) != 0) {
        return 1;
    }

    int de_re_fd = open(DE_RE_PIN, O_WRONLY);
    if (de_re_fd == -1) {
        perror("Error opening GPIO pin");
        close(serial_port);
        return 1;
    }

    uint16_t registers[] = {40001, 40003, 40005};
    size_t num_registers = sizeof(registers) / sizeof(registers[0]);

    for (size_t i = 0; i < num_registers; ++i) {
        send_modbus_request(serial_port, registers[i]);
        // Add any additional processing logic if needed
    }

    close(de_re_fd);
    close(serial_port);
    return 0;
}

int set_serial_params(int port, speed_t baudrate, struct termios *params) {
    if (tcgetattr(port, params) != 0) {
        perror("Error getting serial port attributes");
        return 1;
    }

    cfsetispeed(params, baudrate);
    cfsetospeed(params, baudrate);

    params->c_cflag &= ~PARENB;
    params->c_cflag &= ~CSTOPB;
    params->c_cflag &= ~CSIZE;
    params->c_cflag |= CS8;

    if (tcsetattr(port, TCSANOW, params) != 0) {
        perror("Error setting serial port attributes");
        return 1;
    }

    return 0;
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
