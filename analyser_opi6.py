import struct
import serial

# Configuration
slave_address = 1  # Change to the correct slave address
baud_rate = 9600
serial_port = '/dev/ttyS0'

# Function to read a 32-bit float from Modbus address 40001
def read_float_from_modbus(address, slave):
    try:
        ser = serial.Serial(port=serial_port, baudrate=baud_rate, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)
        
        # Modbus request: read holding registers (function code 0x03)
        # Request format: [Slave Address][Function Code][Starting Address Hi][Starting Address Lo][Quantity of Registers Hi][Quantity of Registers Lo][CRC Hi][CRC Lo]
        command_to_send = struct.pack('>BBBBHH', slave, 0x03, (address - 1) >> 8, (address - 1) & 0xFF, 0x00, 0x02)  # 0x00, 0x02 = read 2 registers (32-bit float)
        ser.write(command_to_send)
        
        # Read response (adjust bytes read based on Modbus data)
        response = ser.read(7 + 1)  # 7 bytes (header) + 1 byte (byte count)
        
        # Print the received response for debugging
        print(f"Received response: {response}")
        
        # Extracting the float value from the response (assuming it's a big-endian float)
        if len(response) >= 4:
            byte_count = response[2]
            value = struct.unpack('>f', response[3:3 + byte_count])[0]
            return value
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()

# Read the 32-bit float value from Modbus address 40001
data = read_float_from_modbus(40001, slave_address)
print("Process Value:", data)  # Output the received 32-bit float value
