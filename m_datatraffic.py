from pymodbus.client.sync import ModbusSerialClient
import time

# Define the serial port and baudrate
client = ModbusSerialClient(method='rtu', port='/dev/ttyS1', baudrate=9600)
# Change '/dev/ttyUSB0' to your actual serial port

# Function to read data from slave
def read_from_slave(unit, address, count):
    try:
        if client.connect():
            # Read holding registers
            response = client.read_holding_registers(address, count, unit=unit)
            client.close()
            return response.registers
        else:
            print("Failed to connect to Modbus device.")
            return None
    except ModbusIOException as e:
        print(f"Modbus communication error: {e}")
        return None
