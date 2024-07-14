from machine import Pin, SoftI2C
import ssd1306

class Display():
    def __init__(self):

    #Initializing the display
        self.i2c = SoftI2C(sda=Pin(21),scl=Pin(22))
        self.display = ssd1306.SSD1306_I2C(128,32, self.i2c)
        self.display.show()
        self.line = 0

    # Message buffer and display settings
        self.message_buffer = []
        self.max_lines = 3  # Number of lines that can fit on the display
        self.line = 0  # Current line for displaying messages



    def update_display(self, message):
        self.display.fill(0)
        start_line = max(0, len(self.message_buffer) - self.max_lines)

        for i, msg in enumerate(self.message_buffer[start_line:], start=0):
            self.display.text(msg, 0, i * 10, 1)

        self.display.show()

        # Handle line wrapping and reset if needed
        if len(message) > 12:  # Adjust based on your display character width
            wrapped_lines = self.wrap_text(message, 12)  # Replace 12 with your character width
            for line in wrapped_lines:
                self.display.text(line, 0, self.line, 1)
                self.line += 10
                if self.line >= 32:
                    self.line = 0
        else:
            self.line += 10
            if self.line >= 32:
                self.line = 0



    def wrap_text(self, text, char_width):
        """Wraps text to fit within the specified character width."""
        lines = []
        current_line = ""
        for word in text.split():
            if len(current_line + word) <= char_width:
                current_line += word + ' '
            else:
                lines.append(current_line[:-1])  # Remove trailing space
                current_line = word + ' '
        lines.append(current_line[:-1])  # Remove trailing space from last line
        return lines


    def add_message(self, message):
        self.message_buffer.append(message)

        # Handle buffer overflow (optional)
        if len(self.message_buffer) > 100:
            self.message_buffer.pop(0)  # Remove oldest message

        self.update_display(message)





if __name__=="__main__":
    # using default address 0x3C
    i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
    display = ssd1306.SSD1306_I2C(128, 32, i2c)
    display.text('Hello, World!', 0, 0, 1)
    display.show()