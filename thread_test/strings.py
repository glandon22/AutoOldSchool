import matplotlib.pyplot as plt
import numpy as np

# Given dictionary
data = {'11886,1836,3': True, '11887,1836,3': True, '11888,1836,3': True, '11889,1836,3': True, '11890,1837,3': True, '11890,1838,3': True, '11890,1839,3': True, '11890,1840,3': True, '11889,1841,3': True, '11888,1841,3': True, '11887,1841,3': True, '11886,1841,3': True, '11885,1840,3': True, '11885,1839,3': True, '11885,1838,3': True, '11885,1837,3': True}

# Extracting x and y values from the keys
x_values = []
y_values = []

for key in data.keys():
    x, y, z = map(int, key.split(','))
    x_values.append(x)
    y_values.append(y)

# Creating the plot
plt.figure(figsize=(10, 6))
plt.scatter(x_values, y_values, color='blue')
plt.title('Pnm perim')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.grid(True)
plt.xticks(range(min(x_values) - 1, max(x_values) + 1))
plt.yticks(range(min(y_values) - 1, max(y_values) + 1))

# Adding labels for each point
for x, y in zip(x_values, y_values):
    plt.text(x, y, f'({x}, {y})')

# Show the plot
'''plt.xlim(min(x_values) - 5, max(x_values) + 5)
plt.ylim(min(y_values) - 5, max(y_values) + 5)'''
plt.show()