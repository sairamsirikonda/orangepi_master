import serial
from pymodbus.client.rs485 import ModbusRTUClient
from pymodbus.converters import ModbusConverters

# Replace with your specific values
PORT = '/dev/ttyS0'  # Replace with the actual serial port device file
SLAVE_ADDRESS = 1  # Replace with the slave address of your gas analyzer
REGISTER_ADDRESS = 40001  # Starting register address
NUMBER_OF_REGISTERS = 5  # Number of registers to read

# Configure serial port
ser = serial.Serial(PORT, baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)

# Create Modbus client
client = ModbusRTUClient(ser)

try:
    # Read data from registers
    result = client.read_holding_registers(REGISTER_ADDRESS, NUMBER_OF_REGISTERS)

    if result.is_exception():
        print("Error reading registers:", result)
    else:
        # Convert read data to float values
        float_values = ModbusConverters.decode_ieee_float(result.registers)

        # Process the float values (replace with your specific logic)
        for i in range(NUMBER_OF_REGISTERS):
            print(f"Register value {i+1}: {float_values[i]:.2f}")  # Format to 2 decimal places

finally:
    # Close serial port
    ser.close()
    print("Serial port closed.")
