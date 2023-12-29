import serial
import time

# Define the serial port parameters
serial_port = '/dev/ttyS1'  # Update this with the correct serial port for your Orange Pi
baud_rate = 9600

# Create a serial object
ser = serial.Serial(serial_port, baud_rate, timeout=1)

def read_co_data():
    try:
        # Send the command to request CO data
        command = bytes.fromhex('7D7B011001F2')
        ser.write(command)

        # Wait for a short time to allow the sensor to respond
        time.sleep(0.1)

        # Read the response
        response = ser.readline().decode('utf-8').strip()

        # Print the received data
        print("Received CO data:", response)

        # Parse and process the data as needed
        # (Make sure to replace this with your actual data processing logic)

    except serial.SerialException as e:
        print(f"Error reading from serial port: {e}")

    finally:
        # Close the serial port
        ser.close()

if __name__ == "__main__":
    read_co_data()