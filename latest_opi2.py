import serial
import minimalmodbus

# Define serial port settings
ser = serial.Serial("/dev/ttyS1", baudrate=9600, parity="N", stopbits=1, bytesize=8)

# Create Modbus client object
mb = minimalmodbus.Instrument(ser.port, 1)  # Replace 1 with the device address if different

# Read gas concentration (address 40001)
try:
    gas_concentration = mb.read_register(40001, "float32")
    print("Gas Concentration:", gas_concentration, "ppm")  # Update units based on manual
except Exception as e:
    print("Error reading gas concentration:", e)

# Additional code for reading other addresses (optional)
# ...

# Close serial port
ser.close()
