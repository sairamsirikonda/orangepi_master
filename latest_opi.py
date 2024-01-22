import serial
import minimalmodbus
import time  # Added for potential delays or timing requirements

# Define whether the gas analyzer uses MODBUS
gas_analyzer_uses_modbus = True  # True or False


# Configure serial port settings (adjust as needed)
ser = serial.Serial('/dev/ttyS1', baudrate=9600, parity='N', stopbits=1, bytesize=8)

# Create MODBUS client object (if applicable)
if gas_analyzer_uses_modbus:
    mb = minimalmodbus.Instrument(ser.port, 001)  # Replace '1' with gas analyzer's MODBUS address
    mb.mode = minimalmodbus.MODE_RTU

# Main loop to continuously read data
while True:
    try:
        if gas_analyzer_uses_modbus:
            # Read data using MODBUS functions
            value = mb.read_register(40007)  # Replace with register address to read
            print("Gas Peak Reading (MODBUS):", value)
        else:
            # Read data using serial commands (replace with appropriate commands)
            ser.write(b'Read Data Command\r\n')
            time.sleep(0.1)  # Delay if needed for response
            response = ser.readline().decode()  # Decode response if necessary
            print("Gas Data (Serial):", response)

    except Exception as e:
        print("Error:", e)

    time.sleep(1)  # Adjust delay between readings as needed
