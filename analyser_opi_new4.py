import minimalmodbus

# Open the Modbus connection
instrument = minimalmodbus.Instrument('/dev/ttyS0', 1)  # Replace '/dev/ttyS0' with your serial port

try:
    registers = [40001, 40003, 40005]

    for register in registers:
        # Example read operation
        result = instrument.read_registers(register - 1, 2)

        # Print the complete Modbus response received
        print(f"Complete response for register {register}: {result}")

        # Process the response
        values = result
        print(f"Values at register {register}: {values}")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close the Modbus connection
    instrument.close()
