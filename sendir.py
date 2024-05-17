def control_mosfet(gpio_pin, duration=1):
    import RPi.GPIO as GPIO
    import time

    # Setup
    GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
    GPIO.setup(gpio_pin, GPIO.OUT)

    try:
        # Turn on the MOSFET
        GPIO.output(gpio_pin, GPIO.HIGH)
        time.sleep(duration)  # Keep it on for specified duration

        # Turn off the MOSFET
        GPIO.output(gpio_pin, GPIO.LOW)

    finally:
        GPIO.cleanup()  # Reset the GPIO pins to a safe state