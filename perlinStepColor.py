import rhinoscriptsyntax as rs
import math
import perlin

pts = rs.GetObjects("select pts", 1)
comp = rs.GetObject("select module",32)
res = rs.GetReal("set resolution", 1)
pScale = rs.GetReal("set noiseScale", .01)
taper = rs.GetReal("set taper",.7)
gens = rs.GetReal("set generations", 5)
sn = perlin.SimplexNoise()


def applyColor(inMesh, col):
    colors = []
    for i in range(rs.MeshVertexCount(inMesh)): colors.append(col)
    rs.MeshVertexColors(inMesh, colors)


def constrainVector(inVec):
    if abs(inVec[0]) > abs(inVec[1]) and abs(inVec[0]) > abs(inVec[2]):
        inVec[1] = 0
        inVec[2] = 0
    if abs(inVec[1]) > abs(inVec[0]) and abs(inVec[1]) > abs(inVec[2]):
        inVec[0] = 0
        inVec[2] = 0
    if abs(inVec[2]) > abs(inVec[0]) and abs(inVec[2]) > abs(inVec[1]):
        inVec[0] = 0
        inVec[1] = 0
    outVec = rs.VectorUnitize(inVec)
    return outVec
        

def voxStep(loc, g, inCol):
    val = sn.noise3(loc[0]*pScale, loc[1]*pScale, loc[2]*pScale)
    alt = val*180
    azm = val*360
    vec = [0,0,1]
    vec = rs.VectorRotate(vec,alt, [0,1,0])
    vec = rs.VectorUnitize(vec)
    vec = rs.VectorRotate(vec, azm, [0,0,1])
    vec = rs.VectorUnitize(vec)
    vec = constrainVector(vec)    
    scal = (taper**g)*res
    vec = rs.VectorScale(vec, scal)
    newLoc = rs.VectorAdd(vec, loc)
    newBox = rs.ScaleObject(comp, [0,0,0], [scal*1.1,scal*1.1,scal*1.1], copy = True)
    rs.MoveObject(newBox, newLoc)
    #rs.ObjectColor(newBox,inCol)
    applyColor(newBox,col)
    if g < gens:
        voxStep(newLoc, g+1, inCol)

for pt in pts:
    tempLoc = rs.PointCoordinates(pt)
    newBox = rs.ScaleObject(comp, [0,0,0], [res,res,res], copy = True)
    rs.MoveObject(newBox, tempLoc)
    col = rs.ObjectColor(pt)
    applyColor(newBox,col)
    #rs.ObjectColor(newBox,col)
    voxStep(tempLoc,0,col)


