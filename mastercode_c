#include <wiringPi.h>
#include <wiringSerial.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <termios.h>

#define TX_PIN 8  // Change this to the GPIO pin connected to the TX pin of your MAX485
#define RX_PIN 10  // Change this to the GPIO pin connected to the RX pin of your MAX485
#define DE_PIN 13  // Change this to the GPIO pin connected to the DE pin of your MAX485

int serialPort;

void setupSerial() {
    serialPort = serialOpen("/dev/ttyS1", 9600);  // Adjust the port and baudrate as needed
    if (serialPort < 0) {
        fprintf(stderr, "Unable to open serial device: %s\n", strerror(errno));
        return;
    }

    serialFlush(serialPort);
}

void setupGPIO() {
    wiringPiSetup();
    pinMode(TX_PIN, OUTPUT);
    pinMode(RX_PIN, INPUT);
    pinMode(DE_PIN, OUTPUT);
}

void setTransmissionMode(int mode) {
    digitalWrite(DE_PIN, mode);
    digitalWrite(RX_PIN, !mode);
}

int main() {
    setupSerial();
    setupGPIO();

    while (1) {
        // Read data from the master
        if (serialDataAvail(serialPort)) {
            char data = serialGetchar(serialPort);
            printf("Received data: %c\n", data);

            // Process the received data as needed

            // Respond to the master
            // For example, you can send an acknowledgment back to the master
            serialPutchar(serialPort, 'A');
            delay(1000);  // Add a delay to avoid flooding the serial port
        }

        // Your main logic can go here

        // You can add more functionality based on your requirements
    }

    return 0;
}
