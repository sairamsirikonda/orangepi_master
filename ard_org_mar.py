import minimalmodbus
import serial
import time

# Define the serial port settings
PORT = '/dev/ttyGS0'  # Replace with the actual serial port
BAUDRATE = 9600
BYTESIZE = 8
PARITY = 'N'
STOPBITS = 1

# Define the Modbus slave address
SLAVE_ADDRESS = 1

# Create a serial port object
ser = serial.Serial(PORT, baudrate=BAUDRATE, bytesize=BYTESIZE, parity=PARITY, stopbits=STOPBITS)

# Create a Modbus slave instrument
instrument = minimalmodbus.Instrument(ser, SLAVE_ADDRESS)

try:
    while True:
        # Read a register from the Modbus master (Arduino)
        register_value = instrument.read_register(0, functioncode=3)  # Read register 0 (address 0) using function code 3

        # Print the received value
        print("Received value:", register_value)

        # Wait for a while before reading again
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    # Close the serial port
    ser.close()
