import serial
import time

# Define the serial port and baudrate
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Change '/dev/ttyUSB0' to your actual serial port

# Function to send packet and read response
def read_from_slave(packet):
    ser.write(packet)  # Send the packet
    time.sleep(0.1)  # Adjust delay if needed
    response = ser.read_all()  # Read response
    return response

# Main loop
while True:
    # Define the packet to send
    packet = bytes.fromhex('01 04 9C 41 00 28 8E 50')

    # Read data from slave
    response = read_from_slave(packet)
    
    # Print the response
    print("Response:", response)
    
    # Adjust loop delay if needed
    time.sleep(1)

# Close the serial connection
ser.close()
