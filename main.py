from turtle import *
from math import *
from time import sleep
from PIL import Image
setup()
up()
#speed('normal') #probably redundant at this stage if using delay(0)
#set to middle of the screen I think. I'm commenting a lot of this code more than a year after writing it / learning turtle&python
home()
 
tracer(0, 0) # make drawing faster. Comment this to see turtle drawings
hideturtle() #comment out to see turtle draw
 
#'Sky' color as the background
bgcolor('lightblue')
title("3D Cube by Sy Sophaneth")

#global position values for the cube
pos = [0.0,0.0,0.0]
rot = [0.0,0.0,0.0]
size = 20
Pos = pos
Rot = rot
#Let's set up original positions for all vertices
verts = [[1.0*size,1.0*size,1.0*size],[-1.0*size,1.0*size,1.0*size],
         [-1.0*size,-1.0*size,1.0*size],[1.0*size,-1.0*size,1.0*size],
         [1.0*size,1.0*size,-1.0*size],[-1.0*size,1.0*size,-1.0*size],
         [-1.0*size,-1.0*size,-1.0*size],[1.0*size,-1.0*size,-1.0*size]]
#as well we will set up a list of normals based on the vert array indices
#this was the only way I knew to do it similar to an .obj 3D file? I read about
#this somewhere and I'm pretty sure this is how Unity generates meshes as well
#[Citation needed]
faces = [[0,1,2,3],[5,4,7,6],[4,0,3,7],[1,5,6,2],[4,5,1,0],[3,2,6,7]]
 
#This was written using a lot of magic numbers because my 'camera' is set up
#as a static object and therefore there was a lot of errors in a few calculations.
#I basically changed random magic numbers on the go to try to get the best looking
#result.
def cull_faces(inverts = [],infaces = []):
    return_faces = []
    #perform leet maths for face culling
    for _ in range(len(infaces)):
        #coordinates (easier to use in maths)
        one = [verts[infaces[_][0]][0],verts[infaces[_][0]][1],verts[infaces[_][0]][2]]
        two = [verts[infaces[_][1]][0],verts[infaces[_][1]][1],verts[infaces[_][1]][2]]
        three = [verts[infaces[_][2]][0],verts[infaces[_][2]][1],verts[infaces[_][2]][2]]
        #calculate normals and normal lengths
        tempnorm = [(one[0]-two[0]),(one[1]-two[1]),(one[2]-two[2])]
        normlength = sqrt(((one[0]-two[0])**2.0)+((one[1]-two[1])**2.0)+((one[2]-two[2])**2.0))
        norm1 = [tempnorm[0]/normlength,tempnorm[1]/normlength,tempnorm[2]/normlength]
        tempnorm = [(three[0]-two[0]),(three[1]-two[1]),(three[2]-two[2])]
        normlength = sqrt(((three[0]-two[0])**2.0)+((three[1]-two[1])**2.0)+((three[2]-two[2])**2.0))
        norm2 = [tempnorm[0]/normlength,tempnorm[1]/normlength,tempnorm[2]/normlength]
        crossvec = [(norm1[1]*norm2[2])-(norm1[2]*norm2[1]),(norm1[2]*norm2[0])-(norm1[0]*norm2[2]),(norm1[0]*norm2[1])-(norm1[1]*norm2[0])]
        #probably the only important vectors in this code block for the faux camera's direction and the 'static directional light's normals
        #changing any of these will result in a different lighting angle or camera angle (camera isn't really relevant since there's no other references)
        cameravec = [0.0,0.0,1.0]
        lightvec = [0,-0.45,0.45]
        #End important magic vectors
        dot = (cameravec[0]*crossvec[0])+(cameravec[1]*crossvec[1])+(cameravec[2]*crossvec[2])
        if dot <-0.15:
            brightness = (lightvec[0]*crossvec[0])+(lightvec[1]*crossvec[1])+(lightvec[2]*crossvec[2])
            return_faces.append(infaces[_])
            return_faces.append(brightness)
    return return_faces
 
def draw(infaces):
    print(infaces, len(infaces)/2)
    for _ in range(int(len(infaces)/2)):
        #This color value can be changed to get a desired face colour in RGB (changing the magic numbers as a 'base lighting' value)
        color((0,0.6+(infaces[_*2+1])*0.6,0))
        up()
        #important magic numbers here also
        goto(verts[infaces[_*2][0]][0]*(5+verts[infaces[_*2][0]][2]/20.0),
             verts[infaces[_*2][0]][1]*(5+verts[infaces[_*2][0]][2]/20.0))
        begin_fill()
        down()
        goto(verts[infaces[_*2][1]][0]*(5+verts[infaces[_*2][1]][2]/20.0),
             verts[infaces[_*2][1]][1]*(5+verts[infaces[_*2][1]][2]/20.0))
        goto(verts[infaces[_*2][2]][0]*(5+verts[infaces[_*2][2]][2]/20.0),
             verts[infaces[_*2][2]][1]*(5+verts[infaces[_*2][2]][2]/20.0))
        goto(verts[infaces[_*2][3]][0]*(5+verts[infaces[_*2][3]][2]/20.0),
             verts[infaces[_*2][3]][1]*(5+verts[infaces[_*2][3]][2]/20.0))
        goto(verts[infaces[_*2][0]][0]*(5+verts[infaces[_*2][0]][2]/20.0),
             verts[infaces[_*2][0]][1]*(5+verts[infaces[_*2][0]][2]/20.0))
        end_fill()
        up()
        
    update()
 
def rotate(xAxis = 59,yAxis = 21,zAxis = 12):
    #calculate for every angle
    thetaX = radians(xAxis)
    thetaY = radians(yAxis)
    thetaZ = radians(zAxis)
    csX = cos(thetaX)
    snX = sin(thetaX)
    csY = cos(thetaY)
    snY = sin(thetaY)
    csZ = cos(thetaZ)
    snZ = sin(thetaZ)
    for vert in range(len(verts)):
        #calculate changes to Y axis
        yx = float(verts[vert][0] * csY - verts[vert][2] * snY)
        yz = float(verts[vert][0] * snY + verts[vert][2] * csY)
        #rotate around Y axis
        verts[vert][0] = yx
        verts[vert][2] = yz
        #calculate changes to X axis
        xy = float(verts[vert][1] * csX - verts[vert][2] * snX)
        xz = float(verts[vert][1] * snX + verts[vert][2] * csX)
        verts[vert][1] = xy
        verts[vert][2] = xz
        #calculate changes to Z axis
        zx = float(verts[vert][0] * csZ - verts[vert][1] * snZ)
        zy = float(verts[vert][0] * snZ + verts[vert][1] * csZ)
        #rotate around Z axis
        verts[vert][0] = zx
        verts[vert][1] = zy
# Control functions for Left Right Down and Up
def L():
    clear()
    rotate(0,5,0)
    draw(cull_faces(verts,faces))
def R():
    clear()
    rotate(0,-5,0)
    draw(cull_faces(verts,faces))
def U():
    clear()
    rotate(-5,0,0)
    draw(cull_faces(verts,faces))
def D():
    clear()
    rotate(5,0,0)
    draw(cull_faces(verts,faces))

flag = True
# Calliing these functions to smoothen the animation
def Up():
    i = 5
    for i in range(5):
        U()
def Down():
    i = 5
    for i in range(5):
        D()
def Right():
    i = 5
    for i in range(5):
        R()
def Left():
    i = 5
    for i in range(5):
        L()

def autoLeft():
    global flag
    for i in range(5000):
        if flag:
            L()
        else:
            break
# Automatic mode 
def autoRight():
    global flag
    for i in range(5000):
        if flag:
            R()
        else:
            break

def autoUp():
    global flag
    for i in range(5000):
        if flag:
            U()
        else:
            break

def autoDown():
    global flag
    for i in range(5000):
        if flag:
            D()
        else:
            break
# Start and Stop toggle
# Flag variable is global and that's why we can call it without being "undefined"
def stop():
    global flag
    flag = False
def start():
    global flag
    flag = True

onkey(Left,"a")
onkey(Right, "d")
onkey(Up, "w")
onkey(Down, "s")

onkey(autoLeft,"Left")
onkey(autoRight,"Right")
onkey(autoUp,"Up")
onkey(autoDown,"Down")

onkey(stop,"n")
onkey(start,"y")

listen()
rotate(0,20,20)
width(2)


draw(cull_faces(verts,faces))


done()