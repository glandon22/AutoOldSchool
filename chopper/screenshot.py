import pyscreenshot as ImageGrab
#tree coords

#tree cords
#im = ImageGrab.grab([1250,475,1405,660])

#chat box coords
#im = ImageGrab.grab([2,1190,645,1350])

#inv coords
#im = ImageGrab.grab([2300,1040,2525,1335])

im = ImageGrab.grab([2,1190,645,1350])
# save image file
im.save(r'screens\\wc_level.png', 'png')