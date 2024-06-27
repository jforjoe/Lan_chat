from machine import Pin, SoftI2C
import ssd1306

# using default address 0x3C
i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

display.text('Hello, World!', 0, 0, 1)
display.show()
