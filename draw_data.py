import board
import busio
import adafruit_character_lcd.character_lcd_i2c as character_lcd


i2c = busio.I2C(board.SCL, board.SDA)
lcd = character_lcd.Character_LCD_I2C(i2c, 16, 2, 0x21)


def draw_data(data):
    lcd.backlight = True
    lcd.message = "Hum: " + str(data['humidity']) + '%\n' + "Temp: " + str(data['temperature']) + chr(223) + "C"