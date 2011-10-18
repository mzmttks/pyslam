import robot.simu2Dlocomotion as robot
import device.simuRLF as device
import features.allpass as features
import landmarks.allpass as landmarks
import kalman.ExtendedKalmanFilter as kalman

import field.visualizer as visualizer
import field.simField as field

fieldObj = field.Field("field/test01.fld")

robotObj = robot.Robot(robot.RANDOM)
deviceObj = device.Device(fieldObj, robotObj)
kf = kalman.Kalman()

while 1:
    pos = robotObj.move(fieldObj)
    raw = deviceObj.getRawData()
    f = features.getFeatures(raw)
    l = landmarks.getLandmarks(f)
    kf.addLandmark(l, pos)
    kf.update()
    
    visualizer.visualize(pos, f, l, kf, fieldObj)

    print pos
