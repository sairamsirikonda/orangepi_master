from pymodbus.client.sync import ModbusSerialClient as ModbusClient

# Open the Modbus connection
client = ModbusClient(method='rtu', port='/dev/ttyS1', baudrate=9600, timeout=1, parity='N')
client.connect()

try:
    registers = [40001, 40003, 40005]

    for register in registers:
        # Example read operation
        result = client.read_input_registers(register - 1, 2, unit=1)

        # Print the complete Modbus response received
        print(f"Complete response for register {register}: {result}")

        # Process the response
        if result.isError():
            print(f"Error reading register {register}: {result}")
        else:
            values = result.registers
            print(f"Values at register {register}: {values}")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the Modbus connection
    client.close()
