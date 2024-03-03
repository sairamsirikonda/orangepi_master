import serial

# Replace with the actual device file name for your serial port
port = "/dev/S0"

# Set serial port configuration
baudrate = 9600
bytesize = serial.EIGHTBITS
parity = serial.PARITY_NONE
stopbits = serial.STOPBITS_ONE

# Open the serial port
ser = serial.Serial(port, baudrate, bytesize, parity, stopbits)

# Test message to send
test_message = "Hello from Orange Pi Zero!"

# Send the message to ModSim32
ser.write(test_message.encode())

# Close the serial port (optional for now, but recommended in production code)
# ser.close()

print("Test message sent to ModSim32.")
