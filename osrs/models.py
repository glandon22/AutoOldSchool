class tile:
    def __init__(self, x, y, z):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)

    @property
    def dict(self):
        return {'x': self.x, 'y': self.y, 'z': self.z}
