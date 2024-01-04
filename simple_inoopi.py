import serial

ser = serial.Serial('/dev/ttyS1', 9600)  # Change '/dev/ttyS1' to the correct serial port

while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').strip()
        print(f"Received from Arduino: {data}")
