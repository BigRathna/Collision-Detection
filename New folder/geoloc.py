import math

CamX,CamY = 300828, 4956483 
A = 95.1 
pitch = -42.6/180*3.14159 
dir = -163.2/180*3.14159 


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


print(Centre_x, Centre_y)
print(BR_x, BR_y)
print(BL_x, BL_y)
print(TR_x, TR_y)
print(TL_x, TL_y)
