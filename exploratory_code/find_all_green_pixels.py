#!/usr/local/bin/python3
import numpy as np
from PIL import Image
# Open image and make RGB and HSV versions
RGBim = Image.open("..\\screens\\loot_box.png").convert('RGB')
HSVim = RGBim.convert('HSV')

# Make numpy versions
RGBna = np.array(RGBim)
HSVna = np.array(HSVim)

# Extract Hue
H = HSVna[:,:,0]

# Find all not purple pixels,
lo,hi = 0,280
# Rescale to 0-255, rather than 0-360 because we are using uint8
lo = int((lo * 255) / 360)
hi = int((hi * 255) / 360)
not_green = np.where((H>lo) & (H<hi))

# Make all green pixels black in original image
RGBna[not_green] = [0,0,0]

# Find all not purple pixels,
lo,hi = 281,360
# Rescale to 0-255, rather than 0-360 because we are using uint8
lo = int((lo * 255) / 360)
hi = int((hi * 255) / 360)
not_green = np.where((H>lo) & (H<hi))

# Make all green pixels black in original image
RGBna[not_green] = [0,0,0]
Image.fromarray(RGBna).save('result.png')