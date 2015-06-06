import rhinoscriptsyntax as rs
import math
import System.Drawing as SD


obj = rs.GetObject("select mesh object",32)
bounding = rs.GetObject("select bounding box",32)

res = rs.GetReal("select resolution",1)

solid = rs.GetReal("solid or surface",0)

bb = rs.BoundingBox(bounding)

dimx = bb[6][0] - bb[0][0]
dimy = bb[6][1] - bb[0][1]
dimz = bb[6][2] - bb[0][2]

stepx = math.floor(dimx/res)
stepy = math.floor(dimy/res)
stepz = math.floor(dimz/res)
mvs = rs.MeshFaceVertices(obj)
ml = rs.MeshVertexColors(obj)


def getColor(check):
    closePoint = rs.MeshClosestPoint(obj,check)
    ind = closePoint[1]
    checkV = mvs[ind]   
    myCol =  ml[checkV[0]]
    return myCol
    

def voxStepper(ptList, x, z):
    count = 0
    while count < len(ptList):
        start = ptList[count][1] - bb[0][1]
        start = math.floor(start/res)
        start = start
        end = dimy 
        if count + 1 < len(ptList):
            end = ptList[count+1][1] - bb[0][1]
        end = math.floor(end/res)
        
        for n in range(int(start), int(end)):
            newY = n*res
            rs.AddPoint([x+bb[0][0],newY+bb[0][1],z+bb[0][2]])            
        count = count + 2


for i in range(int(stepx)):
    for j in range(int(stepz)):
        x = i*res
        z = j*res
        crv = rs.AddLine([x+bb[0][0],bb[0][1],z+bb[0][2]],[x+bb[0][0],dimy+bb[0][1],z+bb[0][2]])
        inters = rs.CurveMeshIntersection(crv,obj)
        rs.DeleteObject(crv)
        if inters:
            if solid == 1:
                voxStepper(inters, x,z)
            else:
                for k in range(len(inters)):
                    newY = (inters[k][1]-bb[0][1])/res
                    newY = math.floor(newY)
                    newY = newY*res +bb[0][1]
                    myPt = rs.AddPoint([x+bb[0][0] ,newY + res/2,z+bb[0][2]])
                    newCol = getColor(inters[k])
                    rs.ObjectColor(myPt, newCol)
        
