import pylab
pylab.ion()
pylab.hold(False)

def inrange(v, maxv, minv):
    if v > maxv: return maxv
    if v < minv: return minv
    return v

def visualize(pos, feature, landmarks, kalman, field):
    fld = pylab.array(field.data)
    fld[inrange(int(pos[0]), fld.shape[0]-1, 0), 
        inrange(int(pos[1]), fld.shape[1]-1, 0)] = 128
    pylab.imshow(fld, interpolation="nearest")
    pylab.draw()
    
def mainloop():
    pylab.show()
