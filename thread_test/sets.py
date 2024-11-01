import matplotlib.pyplot as plt

# Given set of coordinates
data_set = {
    '12089,5099', '12074,5104', '12088,5097', '12074,5103',
    '12077,5095', '12085,5094', '12088,5107', '12072,5105',
    '12085,5108', '12081,5108', '12076,5097', '12081,5095',
    '12072,5097', '12073,5103', '12076,5105', '12086,5101',
    '12083,5101', '12072,5106', '12079,5111', '12082,5095',
    '12087,5103', '12074,5110', '12079,5104', '12078,5106',
    '12074,5112', '12084,5106', '12076,5103', '12079,5101',
    '12086,5096', '12073,5104', '12072,5104', '12086,5111',
    '12076,5104', '12081,5096', '12082,5096', '12074,5094',
    '12075,5105'
}

# Extracting x and y values from the set
x_values = []
y_values = []

for item in data_set:
    x, y = map(int, item.split(','))
    x_values.append(x)
    y_values.append(y)

# Creating the plot
plt.figure(figsize=(10, 6))
plt.scatter(x_values, y_values, color='blue')
plt.title('Plot of Coordinates (x, y)')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.grid(True)
plt.xticks(range(min(x_values) - 1, max(x_values) + 1))
plt.yticks(range(min(y_values) - 1, max(y_values) + 1))

# Adding labels for each point
for x, y in zip(x_values, y_values):
    plt.text(x, y, f'({x}, {y})')

# Show the plot
plt.show()
