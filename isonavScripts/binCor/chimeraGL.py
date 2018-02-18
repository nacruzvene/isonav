import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image

from binCorComplement import *

from random import random
from math import *

from miscellaneous import *

colors = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (1,2),
    (1,5),
    (2,3),
    (2,6),
    (3,7),
    (4,5),
    (4,7),
    (5,6),
    (6,7)
    )

surfaces = (
    (0,1,2,3),
    (0,3,7,4),
    (0,1,5,4),

    (6,2,3,7),
    (6,7,4,5),
    (6,5,1,2),
    )

# theta_min_val=radians(163)
# theta_max_val=radians(176)

# delta_phi_val=radians(45)

# dDist=.45
detValDict={}

def getDetValues(detIdx,subIdx):
    mySimpleStr=str([detIdx,subIdx])
    if mySimpleStr not in detValDict:
        theta_min_val=radians(theta_min[detIdx])
        theta_max_val=radians(theta_max[detIdx])
        delta_phi_val=radians(delta_phi[detIdx])
        dDist=det_dist[detIdx]/50.0
        shift=delta_phi_val*subIdx
        detValDict[mySimpleStr]=theta_min_val,theta_max_val,delta_phi_val,dDist,shift
    return detValDict[mySimpleStr]

vertValDict={}

def getVerticies4Telescope(dDist,theta_min_val,theta_max_val,delta_phi_val,shift):
    myAwesomeStr=str([dDist,theta_min_val,theta_max_val,delta_phi_val,shift])
    if myAwesomeStr not in vertValDict:
        delta_r=0.1
        dDDist=dDist+delta_r
        verticies = (
            (dDist*sin(theta_max_val)*cos(delta_phi_val/2+shift),
             dDist*sin(theta_max_val)*sin(delta_phi_val/2+shift),
             dDist*cos(theta_max_val)),
            (dDist*sin(theta_max_val)*cos(-delta_phi_val/2+shift),
             dDist*sin(theta_max_val)*sin(-delta_phi_val/2+shift),
             dDist*cos(theta_max_val)),
            (dDist*sin(theta_min_val)*cos(-delta_phi_val/2+shift),
             dDist*sin(theta_min_val)*sin(-delta_phi_val/2+shift),
             dDist*cos(theta_min_val)),
            (dDist*sin(theta_min_val)*cos(delta_phi_val/2+shift),
             dDist*sin(theta_min_val)*sin(delta_phi_val/2+shift),
             dDist*cos(theta_min_val)),

            (dDDist*sin(theta_max_val)*cos(delta_phi_val/2+shift),
             dDDist*sin(theta_max_val)*sin(delta_phi_val/2+shift),
             dDDist*cos(theta_max_val)),
            (dDDist*sin(theta_max_val)*cos(-delta_phi_val/2+shift),
             dDDist*sin(theta_max_val)*sin(-delta_phi_val/2+shift),
             dDDist*cos(theta_max_val)),
            (dDDist*sin(theta_min_val)*cos(-delta_phi_val/2+shift),
             dDDist*sin(theta_min_val)*sin(-delta_phi_val/2+shift),
             dDDist*cos(theta_min_val)),
            (dDDist*sin(theta_min_val)*cos(delta_phi_val/2+shift),
             dDDist*sin(theta_min_val)*sin(delta_phi_val/2+shift),
             dDDist*cos(theta_min_val)),
        )
        vertValDict[myAwesomeStr]=verticies
    return vertValDict[myAwesomeStr]

def drawSurfaces(verticies,t=0.999):
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x+=1
            # glColor3fv(colors[x])
            # glColor3fv((1,0,0))
            # myColor=(cos(t*pi/2)**2,0,sin(t*pi/2)**2)
            # myColor=(random(),random(),random())
            if t=="white":
                myColor=(1,1,0)
            else:
                myColor=convert_to_rgb(0,1,t)
            # myColor=getRgb(0,1,t)
            # print("t = ", t )
            # cmap = cm.autumn
            # myColor=cmap(t)[:3]
            glColor3fv(myColor)
            glVertex3fv(verticies[vertex])
            glColor3fv((1,1,1))
    glEnd()

def drawSurfacesWColor(verticies,myColor=()):
    glBegin(GL_QUADS)
    for surface in surfaces:
        for vertex in surface:
            glColor3fv(myColor)
            glVertex3fv(verticies[vertex])
            glColor3fv((1,1,1))
    glEnd()


def getVert4TelesSimple(detIdx,subIdx):
    theta_min_val,theta_max_val,delta_phi_val,dDist,shift=getDetValues(detIdx,subIdx)
    verticies=getVerticies4Telescope(dDist,theta_min_val,theta_max_val,delta_phi_val,shift)
    return verticies

def drawChimTelesGL(detIdx,subIdx,surfStat=False,t=0):
    verticies=getVert4TelesSimple(detIdx,subIdx)
    if surfStat:
        drawSurfaces(verticies,t)
    #     pass

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def specialDrawChimTelesGL(detIdx,subIdx,myColor=(1,1,0)):
    verticies=getVert4TelesSimple(detIdx,subIdx)
    drawSurfacesWColor(verticies,myColor)
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()


def drawFromGLists(gVerts,gEdges,gSurf=[]):
    myColor=convert_to_rgb(0,1,1)
    glBegin(GL_QUADS)
    for surface in gSurf:
        for vertex in surface:
            glColor3fv(myColor)
            glVertex3fv(gVerts[vertex])
            glColor3fv((1,1,1))
    glEnd()

    glBegin(GL_LINES)
    for edge in gEdges:
        for vertex in edge:
            glVertex3fv(gVerts[vertex])
    glEnd()


def drawChimTelesGL2(detIdx,subIdx,surfStat=False):
    theta_min_val,theta_max_val,delta_phi_val,dDist,shift=getDetValues(detIdx,subIdx)
    verticies=getVerticies4Telescope(dDist,theta_min_val,theta_max_val,delta_phi_val,shift)
    if surfStat:
        drawSurfaces(verticies,random())

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def drawRing(detIdx,subTDict):
    telesN=teles_num[detIdx]
    for subIdx in range(telesN):
        tVal=subTDict[subIdx]
        drawChimTelesGL(detIdx,subIdx,True,tVal)

def specialDrawRing(detIdx,myColor=(0,0,1)):
    telesN=teles_num[detIdx]
    for subIdx in range(telesN):
        specialDrawChimTelesGL(detIdx,subIdx,myColor)


def getOptVertStuff4Ring(rNum):
    telesN=teles_num[rNum]
    gVertL=[]
    for j in range(telesN):
        #Get the vertices for all the telescopes in the ring
        telesV=getVert4TelesSimple(rNum,j)
        gVertL.append(telesV)
    gOptVerts,gOptEdges,gOptSurfaces=getOptimizedRelList(gVertL)
    return gOptVerts,gOptEdges

def getVertStuff4Ring(rNum):
    telesN=teles_num[rNum]
    gVertL=[]
    for j in range(telesN):
        #Get the vertices for all the telescopes in the ring
        telesV=getVert4TelesSimple(rNum,j)
        gVertL.append(telesV)
    return gVertL

def getOptVertStuff4Rings(rNumL=[]):
    gVertL=[]
    if rNumL==[]: #All of Chimera
        rNumL=range(34)

    for i in rNumL:
        rVertL=getVertStuff4Ring(i)
        gVertL+=rVertL
    gOptVerts,gOptEdges,gOptSurfaces=getOptimizedRelList(gVertL)
    return gOptVerts,gOptEdges,gOptSurfaces

def drawAllChimera(tDict):
    # for i in range(34):
    # glBegin(GL_LINES)
    for i in range(34):
        ringT=ring_tags[i]
        subTDict=tDict[ringT]
        drawRing(i,subTDict)
    # glEnd()


def specialDrawAllChimera(colorL):
    # glBegin(GL_LINES)
    for i in range(34):
        ringT=ring_tags[i]
        myColor=colorL[i]
        specialDrawRing(i,myColor)
    # glEnd()

def getTDict(rStr,sTel):
    aDict=getRelAngleDict(rStr,sTel)
    tDict={}
    for ringStr in aDict:
        tDict[ringStr]=[]
        for subTel in aDict[ringStr]:
            tVal=subTel/180
            tDict[ringStr].append(tVal)
    return tDict

def myRelAdd(i,myIntList):
    return tuple([e+i for e in myIntList])

def getRotation(thing, x):
    return thing[-x:] + thing[:-x]

def getAllRotList(thing):
    allRotL=[]
    for i in range(len(thing)):
        rThing=getRotation(thing,i)
        allRotL.append(rThing)
    return allRotL

def checkThingOnList(thing,list2Check):
    rotThingL=getAllRotList(thing)

    for rThing in rotThingL:
        if rThing in list2Check:
            return False

    #Now inverting the thing
    invThing=thing[::-1]
    rotIThingL=getAllRotList(invThing)
    for rIThing in rotIThingL:
        if rIThing in list2Check:
            return False

    #If it made it all the way, then it made it to the list.
    return True

def getGRelList(telesCoordLists,boolSurf=False):
    gTelVertList=[]
    gEdgeList=[]
    gSurfList=[]

    tCoordLen=8 #Number of verticies on a single telescope
    myShift=0
    for tCoordPL in telesCoordLists:
        gTelVertList+=tCoordPL

        subRel=[myRelAdd(myShift,myEdgeRel) for myEdgeRel in edges]
        gEdgeList+=subRel

        subSurfRel=[myRelAdd(myShift,mySurf) for mySurf in surfaces]
        gSurfList+=subSurfRel

        myShift+=tCoordLen

    return gTelVertList,gEdgeList,gSurfList

def getOptimizedRelList(telesCoordLists):
    gTelVertList,gEdgeList,gSurfList=getGRelList(telesCoordLists)

    #Converting the edge relationship to point relationship and
    #avoiding repeated edges (including reciprocal ones).
    gVertEdgeL=[]

    edgeR=range(2)
    for edge in gEdgeList:
        edgeVert=tuple([gTelVertList[edge[i]] for i in edgeR])

        if checkThingOnList(edgeVert,gVertEdgeL):
            gVertEdgeL.append(edgeVert)


    #Doing the same with the surfaces
    gVertSurfL=[]

    surfR=range(4)
    #This might be trickier than it looks
    for surf in gSurfList:
        surfVert=tuple([gTelVertList[surf[i]] for i in surfR])

        if checkThingOnList(edgeVert,gVertSurfL):
            gVertSurfL.append(surfVert)

    #Now reducing the points that are on gTelVertList since there are
    #many repeated.
    gReduVertL = list(set(gTelVertList))

    #Converting back the points into index relationships using the
    #gReduVertL list.
    gReduEdgeList=[]
    for gVEdge in gVertEdgeL:
        gReduEdgeList.append((gReduVertL.index(gVEdge[0]),\
                              gReduVertL.index(gVEdge[1])))

    #Now for the surface points.
    gReduSurfList=[]
    for gVSurf in gVertSurfL:
        gReduSurfList.append((gReduVertL.index(gVSurf[0]),\
                              gReduVertL.index(gVSurf[1])))

    return gReduVertL,gReduEdgeList,gReduSurfList

def main():
    rStr="8i"
    sTel=3
    tDict=getTDict(rStr,sTel)
    colorL=[(0,0,1) for i in range(34)]
    colorL[ring_tags.index(rStr)]=(1,0,0.5)
    colorL[ring_tags.index("S16")]=(0,1,0.5)

    pygame.init()
    # width, height=(1900,600)
    width, height=(705,303)
    display = (width,height)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -5)
    # glRotatef(120, 0, 1, 0)
    glRotatef(120, 0, 1, 0)
    # glClearColor(190, 190, 190, 1.0) #4 changing the background

    # gVerts,gEdges,gSurf=getOptVertStuff4Rings(range(30))
    # gVerts,gEdges,gSurf=getOptVertStuff4Rings()
    # print(len(gSurf))

    myCount=0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # glRotatef(1, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        drawAllChimera(tDict)
        specialDrawChimTelesGL(ring_tags.index(rStr),sTel)

        # specialDrawAllChimera(colorL)
        # specialDrawRing(ring_tags.index(rStr))
        # drawFromGLists(gVerts,gEdges,gSurf)

        # drawChimTelesGL(25,5,True)
        # drawChimTelesGL2(32,20,True)
        # drawRing(15)
        pygame.display.flip()
        pygame.time.wait(10)

        if myCount==1:
            print("Inside the if")
            glPixelStorei(GL_PACK_ALIGNMENT, 1)
            data = glReadPixels(0, 0, width, height, GL_RGBA, GL_UNSIGNED_BYTE)
            image = Image.frombytes("RGBA", (width, height), data)
            image.save('output.png', 'PNG')

        myCount+=1

main()
