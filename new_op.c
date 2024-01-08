#include <wiringPi.h>
#include <wiringSerial.h>
#include <stdio.h>
#include <string.h>

int main() {
    int serial_port;
    char buffer[10];

    if (wiringPiSetup() == -1) {
        fprintf(stderr, "Error setting up WiringPi\n");
        return 1;
    }

    serial_port = serialOpen("/dev/ttyS1", 9600);  // Adjust the device path and baud rate as needed
    if (serial_port == -1) {
        fprintf(stderr, "Unable to open serial device\n");
        return 1;
    }

    // Command to read memory location 4001 (assuming it's a 16-bit address)
    const char readCommand[] = {0x01, 0x03, 0x40, 0x01, 0x00, 0x01, 0x24, 0x0D};

    serialPuts(serial_port, readCommand);

    // Wait for the response (adjust the delay based on your device's response time)
    delay(100);

    // Read the response
    int bytesRead = serialDataAvail(serial_port);
    if (bytesRead > 0) {
        serialRead(serial_port, buffer, bytesRead);
        printf("Received data: ");
        for (int i = 0; i < bytesRead; ++i) {
            printf("%02X ", (unsigned char)buffer[i]);
        }
        printf("\n");
    } else {
        fprintf(stderr, "No data received\n");
    }

    // Close the serial port
    serialClose(serial_port);

    return 0;
}
