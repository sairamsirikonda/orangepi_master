import OPi.GPIO as GPIO  # Use OPi.GPIO instead of RPi.GPIO for Orange Pi
import serial
import time

# Configure GPIO pins for DE and RE
DE_RE_PIN = 7  # GPIO pin number for DE and RE

# Configure serial port
ser = serial.Serial(
    port='/dev/ttyS0',  # Serial port connected to RS485 module
    baudrate=9600,      # Baud rate (match with ModSim settings)
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

# Setup GPIO
#GPIO.setboard(GPIO.PCPCPLUS)  # Set board type for Orange Pi PC Plus
GPIO.setmode(GPIO.BOARD)  # Use board pin numbering
GPIO.setup(DE_RE_PIN, GPIO.OUT)

# Function to set DE and RE pins
def set_rs485_mode(mode):
    GPIO.output(DE_RE_PIN, mode)

# Function to send Modbus request and read response
def send_modbus_request(address, function_code, start_register, num_registers):
    # Enable transmission mode
    set_rs485_mode(True)
    time.sleep(0.1)  # Ensure DE/RE pins settle

    # Modbus RTU request format: [address, function_code, start_register_high, start_register_low, num_registers_high, num_registers_low, CRC_high, CRC_low]
    request = bytes([address, function_code, start_register >> 8, start_register & 0xFF, num_registers >> 8, num_registers & 0xFF])
    # Calculate CRC and append to request
    crc = crc16(request)
    request += crc.to_bytes(2, 'big')

    # Send request
    ser.write(request)
    time.sleep(0.1)  # Wait for response to arrive

    # Disable transmission mode
    set_rs485_mode(False)

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
# Cleanup GPIO
GPIO.cleanup()
