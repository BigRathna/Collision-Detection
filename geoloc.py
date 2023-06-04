import math
import pyproj
from pyproj import Transformer


transformer = Transformer.from_crs("EPSG:4326", "epsg:3857")
transformer2 = Transformer.from_crs("epsg:3857","EPSG:4326")

#inserting the coordinates of the location of teh drone
CamX, CamY = transformer.transform(62,-20)

#converting coordinates to a flat terrain format
# transformer = Transformer.from_crs("epsg:3857","EPSG:4326")

A = 170 # relative altitude
pitch = -42.6/180*3.14159 
dir = -163.2/180*3.14159 

# change the values to match the image resolution of the received image.
ImgResX = 40000
ImgResY = 30000

# Change the values to the coordinates of the Object found in the image 
ObjOnImgX = 20000
ObjOnImgY = 15000



RatioX = ObjOnImgX
RatioX2 = (ImgResX-ObjOnImgX)
RatioY = ObjOnImgY
RatioY2 = (ImgResY-ObjOnImgY)

Cf = 4.49 
SX = 6.3 
aspect = 0.75 
Sd = SX * math.sqrt(1+aspect**2) 


ratXh = SX/Cf/2 
ratYh = aspect * ratXh 
ccf = math.sqrt(1+ratYh**2) 
phiXh,phiYh = math.atan(ratXh),math.atan(ratYh) 

Kc = A/math.tan(-pitch*phiYh) 
Kf = A/math.tan(-pitch+1*phiYh)
Kb = A/math.tan(-pitch+(-1*phiYh))


Rc = math.sqrt(A**2+Kc**2) 
Rf = math.sqrt(A**2+Kf**2)
Rb = math.sqrt(A**2+Kb**2)
Wch = Rc * ratXh /1 
Wfh = Rf * ratXh / ccf
Wbh = Rb * ratXh / ccf

Centre_W,Centre_K = 0,Kc
BR_K = Kf
BL_K = BR_K
TR_K = Kb
TL_K = TR_K
BL_W = Wfh
BR_W = -BL_W
TL_W = Wbh 
TR_W = -TL_W


def section(x1, x2, y1, y2, m, n):
 
    # Applying section formula
    x = (float)((n * x1)+(m * x2))/(m + n)
    y = (float)((n * y1)+(m * y2))/(m + n)
    return x,y

def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       raise Exception('lines do not intersect')

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

#find height 

Centre_x = CamX + (Centre_W) * math.cos(dir) + (Centre_K) * math.sin(dir)
BR_x = CamX + (BR_W) * math.cos(dir) + (BR_K) * math.sin(dir)
BL_x = CamX + (BL_W) * math.cos(dir) + (BL_K) * math.sin(dir)
TR_x = CamX + (TR_W) * math.cos(dir) + (TR_K) * math.sin(dir)
TL_x = CamX + (TL_W) * math.cos(dir) + (TL_K) * math.sin(dir)
Centre_y = CamY - (Centre_W) * math.sin(dir) + (Centre_K) * math.cos(dir)
BR_y = CamY - (BR_W) * math.sin(dir) + (BR_K) * math.cos(dir)
BL_y = CamY - (BL_W) * math.sin(dir) + (BL_K) * math.cos(dir)
TR_y = CamY - (TR_W) * math.sin(dir) + (TR_K) * math.cos(dir)
TL_y = CamY - (TL_W) * math.sin(dir) + (TL_K) * math.cos(dir)

P1_x,P1_y = section(BL_x,BR_x,BL_y,BR_y,RatioX,RatioX2)
P2_x,P2_y = section(TL_x,TR_x,TL_y,TR_y,RatioX,RatioX2)
P3_x,P3_y = section(BL_x,TL_x,BL_y,TL_y,RatioY,RatioY2)
P4_x,P4_y = section(BR_x,TR_x,BR_y,TR_y,RatioY,RatioY2)

P1 = (P1_x,P1_y)
P2 = (P2_x,P2_y)
P3 = (P3_x,P3_y)
P4 = (P4_x,P4_y)
FinalX, FinalY = line_intersection((P1,P2),(P3,P4))

print(Centre_x, Centre_y)
Centre_x,Centre_y = transformer2.transform(Centre_x,Centre_y)
print("->>>",Centre_x, Centre_y)
print(transformer2.transform(BR_x, BR_y))
print(transformer2.transform(BL_x, BL_y))
print(transformer2.transform(TR_x, TR_y))
print(transformer2.transform(TL_x, TL_y))

Latitude,Longitude = transformer2.transform(FinalX,FinalY)
print(Latitude,Longitude)

