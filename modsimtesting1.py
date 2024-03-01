import serial
import time

# Configure serial port
ser = serial.Serial(
    port='/dev/ttyS0',  # Serial port connected to RS485 module
    baudrate=9600,      # Baud rate (match with ModSim settings)
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

# Function to send Modbus request and read response
def send_modbus_request(address, function_code, start_register, num_registers):
    # Modbus RTU request format: [address, function_code, start_register_high, start_register_low, num_registers_high, num_registers_low, CRC_high, CRC_low]
    request = bytes([address, function_code, start_register >> 8, start_register & 0xFF, num_registers >> 8, num_registers & 0xFF])
    # Calculate CRC and append to request
    crc = crc16(request)
    request += crc.to_bytes(2, 'big')

    # Send request
    ser.write(request)
    time.sleep(0.1)  # Wait for response to arrive

    # Read response
    response = ser.read(ser.in_waiting)
    return response

# Function to calculate CRC16
def crc16(data):
    crc = 0xFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x0001:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc

# Example usage
if __name__ == "__main__":
    # ModSim slave address
    slave_address = 1
    # Modbus function code for reading holding registers
    function_code = 3
    # Starting register address to read from
    start_register = 0
    # Number of registers to read
    num_registers = 5

    response = send_modbus_request(slave_address, function_code, start_register, num_registers)
    print("Response:", response.hex())

# Close serial port
ser.close()
