import numpy

def genTestSet(state0=0, length=100):
    x = [float(state0)]
    for i in range(1, length):
        x.append( x[i-1] / 2.0 +\
                  25 * x[i-1] / (1 + x[i-1] ** 2) + \
                  8 * numpy.cos(1.2 * i) )
    return x

def genTestSetLinear(state0=None, length=100, noise=0):
    state = [numpy.matrix([0, 1]).T]
    update = numpy.matrix([[1, 0.1],[0, 0.9]])

    for t in range(length):
        state.append( update * state[t-1] + \
                      noise * numpy.random.normal(0,1,1)) 
    return state

if __name__ == "__main__":
    import pylab

    state0 = 0
    length = 100

    pylab.subplot(2, 1, 1)
    testset = genTestSet(state0, length)
    pylab.plot(testset)

    pylab.subplot(2, 1, 2)
    testset = genTestSetLinear(length, noise=0.01)
    pylab.plot([t[0,0] for t in testset])
    pylab.plot([t[1,0] for t in testset])
    pylab.show()
    
