import pymunk
import members


class Walker:
    def __init__(self, space) -> None:
        self.arm1 = members.ArmRight(space, 600,600,100,10,5)
        self.arm2 = members.ArmRight(space, 300,600,100,10,5)
    
        self.body = pymunk.Body()
        self.body.position = (500,600)
        self.shape = pymunk.Circle(self.body,50)
        self.shape.mass =50

        self.joint1 = pymunk.PivotJoint(self.arm1.bone1.get_body(),self.body,(550,600))
        self.joint2 = pymunk.PivotJoint(self.arm2.bone2.get_body(),self.body,(450,600))

    def create(self, space):
        space.add(self.joint1)
        space.add(self.joint2)
        space.add(self.body,self.shape)
        return self.shape