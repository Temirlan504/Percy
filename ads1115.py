from smbus import SMBus
import time

ADS1115_I2C_ADDRESS = 0x48
CONVERSION_REGISTER = 0x00
CONFIG_REGISTER = 0x01

# Define I2C bus on channel 1
# bus = SMBus(1)

class TemperatureSensor:
    def __init__(self, bus, channel=0):
        self.bus = bus
        self.channel = channel
        self.config = 0x8583  # 0b1000010100000011
        self.config |= (self.channel << 12)
        self.config |= (0x0000 << 9)  # 128 SPS
        self.config |= (0x0000 << 5)  # Continuous mode
        self.config |= (0x0000 << 4)  # Single shot mode
        self.config |= (0x0000 << 3)  # Disable comparator
        self.config |= (0x0000 << 2)  # Disable comparator
        self.config |= (0x0000 << 1)  # Disable comparator
        self.config |= (0x0000 << 0)  # Disable comparator
        bus.write_i2c_block_data(ADS1115_I2C_ADDRESS, CONFIG_REGISTER, [(self.config >> 8) & 0xFF, self.config & 0xFF])

    def read(self, bus):
        # Write configuration to start a single-shot conversion
        bus.write_i2c_block_data(ADS1115_I2C_ADDRESS, CONFIG_REGISTER, [(self.config >> 8) & 0xFF, self.config & 0xFF])
        time.sleep(0.1)  # Wait for conversion to complete (adjust delay as needed)

        # Read the conversion register to get 2 bytes of A0 output
        data = bus.read_i2c_block_data(ADS1115_I2C_ADDRESS, CONVERSION_REGISTER, 2)

        # Convert returned data array of decimals to an array of 2 bytes
        binary_values = [bin(value)[2:].zfill(8) for value in data]

        # Join first part of the binary number with the second part
        binary_number = ''.join(binary_values)
        
        return binary_number

    def close(self, bus):
        bus.close()

# Create an instance of the TemperatureSensor class
# temp_sensor = TemperatureSensor()

# Read temperature from the sensor
# while True:
#     try:
#         adc_out_binary = temp_sensor.read()
#         adc_out_decimal = int(adc_out_binary, 2)

#         # Convert the ADC output to temperature
#         temperatureC = 0.015107 * adc_out_decimal + 11.5564

#         print(f'Temperature: {round(temperatureC, 2)}°C')

#         time.sleep(1)

#     except KeyboardInterrupt:
#         # Close the I2C bus
#         temp_sensor.close()
