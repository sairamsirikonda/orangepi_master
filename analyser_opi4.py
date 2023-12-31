#!/root/orangepi_master/venv/bin/python

from pymodbus.client.sync import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException

# Configuration
serial_port = '/dev/ttyS0'  # Adjust this based on your setup
baud_rate = 9600

# Create Modbus Serial Client
client = ModbusSerialClient(method='rtu', port=serial_port, baudrate=baud_rate)

def read_from_analyzer():
    try:
        # Specify the slave address and register range to read
        slave_address = 1  # Replace with the correct slave address
        start_register = 1  # Replace with the correct start register
        num_registers = 2  # Adjust based on the number of registers to read

        # Read holding registers from the analyzer
        result = client.read_holding_registers(start_register, num_registers, unit=slave_address)

        if result.isError():
            print(f"Error reading from the analyzer: {result}")
            return None

        return result.registers
    except ModbusIOException as e:
        print(f"Modbus communication error: {e}")
        return None

# Example usage
if __name__ == "__main__":
    try:
        if client.connect():
            data = read_from_analyzer()
            client.close()

            if data is not None:
                print(f"Received data from the analyzer: {data}")
        else:
            print("Failed to connect to the Modbus serial client.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
