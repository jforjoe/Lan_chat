from machine import Pin, SoftI2C
import time
import _thread
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

    # Initializing pages
        self.current_page = 0
        self.pages = []


    def update_display(self):
        self.display.fill(0)
        start_line = max(0, len(self.message_buffer) - self.max_lines)

        for i, msg in enumerate(self.message_buffer[start_line:], start=0):
            self.display.text(msg, 0, i * 10, 1)

        self.display.show()

        # Handle line wrapping and reset if needed
        if len(self.message_buffer[-1]) > 12:  # Adjust based on your display character width
            wrapped_lines = self.wrap_text(self.message_buffer[-1], 12)  # Replace 12 with your character width
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

        #self.update_display(message)  # when pages are not dealt with uncomment this ....
        self.update_pages()
        self.show_current_page()

        # Start the update loop in a new thread
        _thread.start_new_thread(self.update_display_loop, ())


######################################################################################################
######################################################################################################
##      _________________HANDLING PAGES OF MESSAGES________________________ 

    def update_pages(self):
        self.pages = []
        current_page = []
        for message in self.message_buffer:
            current_page.append(message)
            if len(current_page) == self.max_lines:
                self.pages.append(current_page)
                current_page = []
        if current_page:
            self.pages.append(current_page)



    def show_current_page(self):
        self.display.fill(0)
        # Check if there are any pages
        if not self.pages:
            self.display.text("No messages yet!", 0, 0, 1)
            self.display.show()
            return

        # Handle empty pages within the current page range
        while not self.pages[self.current_page]:
            self.current_page += 1  # Move to next page (if not empty)
            if self.current_page >= len(self.pages):
                self.current_page = len(self.pages) - 1  # Clamp to last page
                break  # Exit loop if all pages are empty

        # Display messages from the current page
        for i, message in enumerate(self.pages[self.current_page]):
            self.display.text(message[:16], 0, i * 10, 1)  # Truncate to 16 characters
        self.display.show()



    def update_display_loop(self):
        while True:
            self.update_display()
            time.sleep(0.5)  # Adjust the sleep time as needed


    def next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.show_current_page()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_current_page()



if __name__=="__main__":
    # using default address 0x3C
    i2c = SoftI2C(sda=Pin(21), scl=Pin(22))
    display = ssd1306.SSD1306_I2C(128, 32, i2c)
    display.text('Hello, World!', 0, 0, 1)
    display.show()