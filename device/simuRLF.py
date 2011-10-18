import numpy
import itertools

class Device:
    def __init__(self, field, robot):
        self.field = field
        self.robot = robot

    def getRawData(self):
        x = self.robot.pos[0]
        y = self.robot.pos[1]
        return [self.field.data[i, j] for i, j 
                in itertools.product(
                [x-1, x, x+1], [y-1, y, y+1])]
    
if __name__ == "__main__":
    pass
