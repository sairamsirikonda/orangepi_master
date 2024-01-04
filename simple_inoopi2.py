import time
import serial
import orangepi.gpio as GPIO  # Import the GPIO library for Orange Pi

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT, initial=GPIO.HIGH)  # Set DE/RE pin high to enable transmission

receive = serial.Serial(
    port='/dev/ttyS1',  # Adjust the serial port as per your Orange Pi setup
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

while True:
    if receive.in_waiting > 0:
        data = receive.read()  # Read a byte from the master
        pwm_value = int.from_bytes(data, byteorder='big')  # Convert byte to integer
        print("Received PWM Value from Master:", pwm_value)

        # Your logic to control the device based on the received PWM value goes here
        # Example: GPIO.output(YOUR_PIN, pwm_value > THRESHOLD)

        time.sleep(1.5)  # Adjust the delay as needed
