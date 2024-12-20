import RPi.GPIO as GPIO
from time import sleep

# Pin Definitions
TEMP_SENSOR_PIN = 4
PUMP_PIN = 17
HEATER_PIN = 27

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PUMP_PIN, GPIO.OUT)
GPIO.setup(HEATER_PIN, GPIO.OUT)


def read_temperature():
    # Example function to read temperature, implementation depends on sensor type
    temperature = 25.0  # Placeholder
    return temperature


def control_heater(temperature):
    if temperature < 24.0:
        GPIO.output(HEATER_PIN, GPIO.HIGH)
    else:
        GPIO.output(HEATER_PIN, GPIO.LOW)


def main():
    try:
        while True:
            temp = read_temperature()
            control_heater(temp)
            sleep(60)  # Check every minute
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
