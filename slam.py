import robot.toySimulator as robot
import features.simuRLF as features
import landmarks.allpass as landmarks
import kalman.ExtendedKalmanFilter as kalman

kf = kalman.UnscentedKalmanFilter()

while 1:
    m = robot.move()
    f = features.getFeature()
    l = landmarks.getLandmarks(f)
    kf.addLandmark(l, m)
    kf.update()
    
