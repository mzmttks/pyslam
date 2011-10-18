import numpy
import numpy.linalg
import ut
import copy


class UnscentedKalman:

    def __init__(self, f, fn, h, hn, x0, P0, kappa=2):
        self.f = f
        self.fn = fn
        self.h = h
        self.hn = hn
        self.sDim = fn.shape[0]
        self.mDim = hn.shape[0]

        self.x = numpy.matrix(numpy.concatenate(
            (x0, #state
             numpy.zeros((self.sDim, 1)),#state noise
             numpy.zeros((self.mDim, 1)))))#measurement noise

        self.kappa = kappa

        self.P = numpy.matrix(
            numpy.zeros((P0.shape[0] + fn.shape[0] + hn.shape[0],
                         P0.shape[1] + fn.shape[1] + hn.shape[1])))
        self.P[0:P0.shape[0], 0:P0.shape[1]] = P0
        self.P[P0.shape[0]:P0.shape[0] + fn.shape[0],
               P0.shape[1]:P0.shape[0] + fn.shape[1]] = fn

        self.P[- hn.shape[0]:, - hn.shape[1]:] = hn

        self.ut = ut.UnscentedTransform(kappa)

    def update(self, data):

        # state
        xminus, pminus = self.ut.transform(self.f, self.x, self.P)
        pminus += numpy.matrix(numpy.eye(self.ut.mean.shape[0]) * 10 ** -5)

        stateSigma = copy.copy(self.ut.aftsigma)

        self.ut.convert(self.h)

        zminus = self.ut.estimateMean()
        S = self.ut.estimateCov()
        measureSigma = copy.copy(self.ut.aftsigma)

        Pxy = numpy.matrix(numpy.zeros((xminus.shape[0], zminus.shape[0])))
        for sigx, sigz, w in zip(stateSigma,
                                 measureSigma,
                                 self.ut.w):
            Pxy += w * (sigx - xminus) * (sigz - zminus).T

        if numpy.linalg.det(S) > 0:
            K = Pxy * S.I
        else:
            print "det(S) is zero"
            K = Pxy# * S.I

        self.x[0:self.sDim, 0:self.sDim] \
            = self.x[0:self.sDim, 0:self.sDim] + K * (data - zminus)
        self.P[0:self.sDim, 0:self.sDim] = pminus - K * S * K.T

        self.innovation = (data - zminus)
        self.zminus = zminus
        self.data = data

        self.hist()

    def hist(self):
        import copy
        try:
            self.xhist.append(copy.copy(self.x))
        except:
            self.xhist = [self.x]

        try:
            self.phist.append(self.P)
        except:
            self.phist = [self.P]

        try:
            self.ihist.append(float(self.innovation.trace()))
        except:
            self.ihist = [float(self.innovation.trace())]

def __test__():
    pass


if __name__ == "__main__":
    import pylab
    import testset
    import numpy

    def plot(isDraw=True):
        #return
        pylab.subplot(3, 1, 1)
        pylab.title("State")

        pylab.plot([x[0, 0] for x in kal.xhist],
                   "k-", label="Estimated state")
        pylab.hold(True)
        pylab.plot([t[0, 0] for t in states[1:]],
                   "r-", label="True state")
        #pylab.legend(loc="lower right")

        pylab.hold(False)
        pylab.subplot(3, 1, 2)
        pylab.plot([t[0, 0] for t in measures],
                   label="Measurement")
        pylab.hold(False)
        pylab.legend()

        pylab.hold(False)
        pylab.subplot(3, 1, 3)
        pylab.plot([tmpx[0, 0] - t[0, 0]
                    for tmpx, t in zip(kal.xhist, states[1:])],
                   label="Estimation error")
        pylab.hold(False)
        pylab.legend()

        if isDraw:
            pylab.draw()
        else:
            pylab.show()
    sDim = 1
    mDim = 1
    pylab.ion()
    dt = 0.01

    def f(prev, noise=numpy.matrix(numpy.zeros(sDim)).T):
        #return prev[:sDim] + noise
        return prev[:sDim] - dt * numpy.matrix([
                numpy.sin(10 * i * numpy.pi / 180.0)]) + noise
        #return prev[:sDim] + numpy.matrix([
        #        -prev[1, 0] + noise[0, 0],
        #         prev[1, 0]**2 * prev[2, 0] + noise[1, 0],
        #         noise[2, 0]]).T
    fn = 0.1 * numpy.matrix(numpy.eye(sDim))

    def h(state, noise=numpy.matrix(numpy.zeros(mDim)).T):
        #return numpy.matrix([numpy.sin(state[0, 0]),
        #                     numpy.cos(state[0, 0])]).T + noise
        return numpy.matrix([(state[0, 0])**3 + noise[0, 0]])
        #return numpy.matrix(numpy.sqrt(1 + (state[1, 0] - 10)**2)) + noise

    def hfault(state):
        return numpy.matrix([state[0, 0]**2 + state[0, 0]])

    hn = 0.1 * numpy.matrix(numpy.eye(mDim))

    P0 = numpy.matrix(numpy.diag([1.0]))
    x0 = numpy.matrix([1.0]).T

    kal = UnscentedKalman(f, fn, h, hn, x0, P0)
    step = 300

    states = [x0]
    measures = [h(x0)]
    for i in range(step - 1):
        print "iteration", i

        fnoise = numpy.random.multivariate_normal(numpy.zeros(sDim), fn)
        hnoise = numpy.random.multivariate_normal(numpy.zeros(mDim), hn)

        fnoise = numpy.matrix(fnoise).T
        hnoise = numpy.matrix(hnoise).T

        states.append(f(states[-1], fnoise))
        measures.append(h(states[-1], hnoise))

        kal.update(measures[-1])
        #kal.update(hfault(states[-1]))

        #if i > 5:
        #    plot()
    plot(False)
