import time
class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.motion=ALProxy("ALMotion")
        self.posture=ALProxy("ALRobotPosture")
        self.touch=ALProxy("ALTouch")
        self.memory=ALProxy("ALMemory")

    def onLoad(self):
        self.isRunning=False
        self.events = ['FrontTactilTouched', 'MiddleTactilTouched', 'RearTactilTouched']

        for event in self.events:
            self.memory.subscribeToEvent(event, self.getName(), 'Process')

    def onUnload(self):
        self.isRunning=False

        for event in self.events:
            self.memory.unsubscribeToEvent(event, self.getName())

    def onInput_onStart(self):
        if not self.isRunning:
            self.isRunning=True
            self.motion.wakeUp()
            self.posture.goToPosture("StandInit",0.8)
            self.motion.setStiffnesses("LArm",0)

            while self.isRunning:
                angles=self.motion.getAngles(["LShoulderRoll","LShoulderPitch"],True)
                self.logger.info("angles "+str(angles))
                if angles[1]<0.5:
                    # walk
                    if angles[0]>1:
                        angles[0] = 1

                    self.motion.moveToward(1,0,angles[0])
                else:
                    self.motion.moveToward(0,0,0)
                time.sleep(0.1)

            self.motion.moveToward(0,0,0)

            self.onStopped()

    def Process(self, var, val, msg):
        if val == 1:
            self.isRunning=False

    def onInput_onStop(self):
        self.isRunning=False