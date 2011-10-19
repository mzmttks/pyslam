import random

RANDOM = 0
class Robot:
    def __init__(self, mode, pos = (10, 10)):
        self.mode = mode
        self.pos = list(pos)
    def move(self, field):
        if self.mode == RANDOM:
            cand = [0]
            if 0 < self.pos[0] and \
                    field.data[self.pos[0]+1, self.pos[1]] == 0: 
                cand.append(1)
            if self.pos[0] < field.data.shape[0] and \
                    field.data[self.pos[0]-1, self.pos[1]] == 0: 
                cand.append(-1)
            self.pos[0] += random.choice(cand)
            
            cand = [0]
            if 0 < self.pos[1] and \
                    field.data[self.pos[0], self.pos[1]+1] == 0: 
                cand.append(1)
            if self.pos[1] < field.data.shape[1] and \
                    field.data[self.pos[0], self.pos[1]-1] == 0: 
                cand.append(-1)
            self.pos[1] += random.choice(cand)
