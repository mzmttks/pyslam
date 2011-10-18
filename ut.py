import numpy
import copy

class UnscentedTransform:
    def __init__(self, kappa):
        self.kappa = float(kappa)
        
    def getSigmaPoints(self, mean, cov, isOrig = True):
        self.L = mean.shape[0]
                
        if isOrig:
            self.w = [self.kappa / (self.L + self.kappa)]
            cov = self.sqrt((self.L + self.kappa) * cov)
        else:
            self.w = [1.0 / 3]
            cov = self.sqrt((self.L)/(1 - self.w[0]) * cov)

        self.sigma = [copy.copy(mean)]
        
        for i in range(self.L):
            self.sigma.append(mean + cov[i, :].T)
            self.sigma.append(mean - cov[i, :].T)
            if isOrig:
                self.w.extend([1.0 / (2 * (self.L + self.kappa))] * 2 )
            else:
                self.w.extend([(1.0 - self.w[0]) / (2 * self.L)] * 2)
        
    def sqrt(self, A):
        """ A = P * P.T"""
        #print "eig:", numpy.linalg.eig(A)[0]
        try:
            sqrta = numpy.linalg.cholesky(A)
            return sqrta
        except:
            return numpy.eye(A.shape[0])

    def estimateMean(self):
        self.mean = numpy.matrix(numpy.zeros(self.aftsigma[0].shape))
        for w, sigma in zip(self.w, self.aftsigma):
            self.mean += w * sigma
        return self.mean

    def estimateCov(self):
        self.cov = numpy.matrix(numpy.zeros((self.aftsigma[0].shape[0],
                                           self.aftsigma[0].shape[0])))
        for w, sigma in zip(self.w, self.aftsigma):
            self.cov += w * (sigma - self.mean) * (sigma - self.mean).T
        return self.cov
        
    def convert(self, func):
        self.aftsigma = [numpy.matrix(func(d)) for d in self.sigma]
    
    def transform(self, func, mean, cov, isOrig=True, flag=False):
        self.getSigmaPoints(mean, cov, isOrig)
        self.convert(func)

        return self.estimateMean(), self.estimateCov()


if __name__ == "__main__":
    import pylab
    import scipy
    import copy

    def func(x):
        return numpy.matrix( (x[0, 0] * numpy.cos(x[1, 0]),
                              x[0, 0] * numpy.sin(x[1, 0]))).T
    kappa = 2
    
    befmean = numpy.matrix([1, 90.0 * (numpy.pi / 180)]).T
    befcov = numpy.matrix(numpy.diag([0.01, 20.0 / 180 * numpy.pi])).T

    
    x, y = scipy.random.multivariate_normal(befmean.T.tolist()[0], 
                                            befcov, 5000).T
    
    ut = UnscentedTransform(kappa)
    aftmean, aftcov = ut.transform(func, befmean, befcov)
    aftmean2, aftconv2 = ut.transform(func, befmean, befcov)

    after = map(lambda t: func(numpy.matrix((t[0], t[1])).T), zip(x,y))

    
    print "--- Before ---"
    print "mean: ", befmean.T.tolist()[0]
    print "cov : ", befcov.flatten()

    print "--- Unscented ---"
    print "mean: ", aftmean.T.tolist()[0]
    print "cov : ", aftcov.flatten()
    
    print "--- Monte Calro ---"
    aftx = [a[0, 0] for a in after]
    afty = [a[1, 0] for a in after]
    print "mean: ", [numpy.mean(aftx), numpy.mean(afty)]
    print "cov : ", numpy.cov(aftx, afty).flatten()


    pylab.subplot(2, 1, 1)
    pylab.plot(x, y, "k.")
    pylab.plot([s[0, 0] for s in ut.sigma],
               [s[1, 0] for s in ut.sigma],
               "ro",
               markersize=20)
    pylab.legend()

    pylab.subplot(2, 1, 2)
    pylab.plot([t[0, 0] for t in after],
               [t[1, 0] for t in after],
               "k.")
    pylab.plot([s[0, 0] for s in ut.aftsigma],
               [s[1, 0] for s in ut.aftsigma],
               "ro",
               markersize=15)
    #pylab.plot(aftmean[0, 0],
    #           aftmean[1, 0],
    #           "ro",
    #           label="Unscented")
    pylab.plot(aftmean2[0, 0],
               aftmean2[1, 0],
               "go",
               label="Unscented",
               markersize=15)
    pylab.plot(numpy.mean(aftx), numpy.mean(afty), "rD", label="Monte Carlo")
    pylab.legend()
    pylab.show()
  
