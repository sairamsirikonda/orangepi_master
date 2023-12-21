import serial

# Configuration
slave_address = 0x01  # Slave address
baud_rate = 9600
serial_port = '/dev/ttyS0'

# Create serial connection with no parity and 1 stop bit
ser = serial.Serial(port=serial_port, baudrate=baud_rate, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=1)

def read_from_slave():
    # Example Modbus read command (read two registers starting from address 0)
    command_to_send = bytes([slave_address, 0x03, 0x00, 0x00, 0x00, 0x02, 0x84, 0x0A])  # Modify as needed
    ser.write(command_to_send)

    # Read response
    response = ser.read(8)  # Adjust the number of bytes to read based on your expected response length
    return response

try:
    # Example usage
    data = read_from_slave()
    print(data)  # Output the received data
except Exception as e:
    print(f"Error: {e}")
finally:
    # Close the serial connection when done
    ser.close()
