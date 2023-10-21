# Name: Matangini Gupta
# Student ID: 2210994810
# Task 8.1d-Raspberry Pi I2C
# SIT210 - Embedded Systems Development

# Import necessary libraries for I2C communication and time handling.
import smbus
import time

# Set the time interval (in seconds) between readings and define brightness level thresholds.
READING_INTERVAL = 1
TOO_BRIGHT_THRESHOLD = 400
BRIGHT_THRESHOLD = 350
MEDIUM_THRESHOLD = 150
DARK_THRESHOLD = 100

# Configure the I2C address for the light sensor and select continuous high-resolution mode.
ADD_LIGHT_SENSOR = 0x23  
RESOLUTION_HIGH = 0x20  

# Initialize the SMBus object for I2C communication on Raspberry Pi.
bus = smbus.SMBus(1)

# Set the light sensor to high-resolution mode using the specified I2C address and command.
bus.write_byte(ADD_LIGHT_SENSOR, RESOLUTION_HIGH)

# Function to retrieve and return the current light level from the light sensor.
def outputLight_intensity():
    bus.write_byte(ADD_LIGHT_SENSOR, RESOLUTION_HIGH)  # Set sensor to high-resolution mode.
    time.sleep(0.2)  # Wait for sensor to stabilize.
    lux_data = bus.read_i2c_block_data(ADD_LIGHT_SENSOR, 0x00, 2)  # Read 2 bytes of data from the sensor.
    lux = int((lux_data[1] + (256 * lux_data[0])) / 1.2)  # Calculate lux value based on sensor data.
    return lux

#Categorizes the light level based on lux readings into predefined categories/labels.
# Args:
#  lux (int): Light intensity in lux.
# Returns:
#  str: Categorized label ("Too bright", "Bright", "Medium", "Dark", "Too dark").
def light_intensity_label(lux):
    if lux >= TOO_BRIGHT_THRESHOLD:
        return "Too bright"
    if BRIGHT_THRESHOLD <= lux < TOO_BRIGHT_THRESHOLD:
        return "Bright"
    if MEDIUM_THRESHOLD <= lux < BRIGHT_THRESHOLD:
        return "Medium"
    if DARK_THRESHOLD <= lux < MEDIUM_THRESHOLD:
        return "Dark"
    if 0 <= lux < DARK_THRESHOLD:
        return "Too dark"

# Function to repeatedly print the current light level category.
def main():
    while True:
        light_intensity = outputLight_intensity()  # Get current light level from the sensor.
        label_light = light_intensity_label(light_intensity)  # Categorize the light level.
        print(f"Current Light Level: {light_intensity} lux - {label_light}")  # Print the light level category.
        time.sleep(READING_INTERVAL)  # Wait for the specified interval before the next reading.

# Entry point to the script; calls the main function if executed directly.
if __name__ == "__main__":
    main()