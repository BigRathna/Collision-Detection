import pygame,sys,random,math

# Intialize the pygame
pygame.init()
clock=pygame.time.Clock()

# create the screen
height = 800
width = 700
screen = pygame.display.set_mode((height, width))

# colours
blue=(0,0,255)
green=(0,255,0)
red=(255,0,0)
black=(0,0,0)
white=(255,255,255)

# Waypoints
wayPoints=[[5,5],[130,200],[320,300],[500,430],[100,410],[270,560],[780,690]]
wayPoint_Index = -1

# Find distance between 2 points
def distance(p1,p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**.5

# To see if 2 circles overlap
def circleOverlapping(c1,c2):
    d=distance(c1[0:2],c2[0:2])
    if d>(c1[2]+c2[2]):
        return False
    else:
        return True

# Obstacles
obs1=[[40,60,20],[50,200,40],[200,280,70],[270,450,70],[800,450,90]]
obs=[]
obst = []
bObs=[]
# We get random points for circle and if the random circle doesnt overlap with other 
# circles we move forward

for i in range(len(obs1) ):
    x = obs1[i][0]
    y = obs1[i][1]
    z = obs1[i][2] + 10
    obs.append([x,y,z])
    obst.append([x,y,z])

    
# takes 2 points
def eqOfLine(p1,p2):
    m=(p1[1]-p2[1])/(p1[0]-p2[0])
    return [m,-m*p1[0]+p1[1]]
# return a list of form y=l[0]x+l[1]  

def quadraticFormula(a,b,c):
    d=b**2-4*a*c
    if d>=0:
        return (-b+d**.5)/(2*a),(-b-d**.5)/(2*a)
    else:
        return "No Tangent"

# checks if line is in circle
def lineInCircle(l,c):
    dist=(((l[0]*c[0]-c[1]+l[1])**2)/((l[0])**2+1))**.5
    if dist>=c[2]:
        return False
    return True

# returns angle between 2 lines
# takes slope of both lines
def angle(m1,m2):
    rad=math.atan((((m1-m2)/(1+m1*m2))**2)**.5)
    return math.degrees(rad)


# takes point and circle returns angle fow which
# x=r*cos(angle) and y=r*sin(angle)
# point needs to be on circle
def parametricAngle(p,c):
    angle=(math.acos((p[0]-c[0])/c[-1]),math.asin((p[1]-c[1])/c[-1]))
    if angle[0]<=math.pi/2 and angle[1]>=0:
        return angle[0]
    elif angle[0]<=math.pi/2 and angle[1]<0:
        return 2*math.pi+angle[1]
    elif angle[0]>math.pi/2 and angle[1]>0:
        return angle[0]
    else:
        return math.pi+angle[1]


# find points of intersection between 2 circles
def get_intersections(x0, y0, r0, x1, y1, r1):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d=math.sqrt((x1-x0)**2 + (y1-y0)**2)
    
    # non intersecting
    if d > r0 + r1 :
        return None
    # One circle within other
    if d < abs(r0-r1):
        return None
    # coincident circles
    if d == 0 and r0 == r1:
        return None
    else:
        a=(r0**2-r1**2+d**2)/(2*d)
        h=math.sqrt(r0**2-a**2)
        x2=x0+a*(x1-x0)/d   
        y2=y0+a*(y1-y0)/d   
        x3=x2+h*(y1-y0)/d     
        y3=y2-h*(x1-x0)/d 

        x4=x2-h*(y1-y0)/d
        y4=y2+h*(x1-x0)/d
        
        # we check the angles 
        l1=eqOfLine((x0,y0),(x3,y3))
        l1.append(angle(l[0],l1[0]))
        l2=eqOfLine((x0,y0),(x4,y4))
        l2.append(angle(l[0],l2[0]))

        if(l1[-1]<=l2[-1]):
            return [x3,y3,"c"]
        else:
            return [x4,y4,"c"]


# array to store all the arcs we have to draw
# 
arc=[]

# array that has all the points we visit
# each point is stored as a list [x,y,l/c]
# if it ends with l that means we have to draw line from point to next point
# if it ends with c that means we habe to draw arc
pointsToDraw=[]



# adding waypoints to pointsToDraw
for i in range(len(wayPoints)):
    pointsToDraw.append([wayPoints[i][0],wayPoints[i][1],"l"])

# initalising points as we have to visit them
curPt=pointsToDraw[0]
nextPt=pointsToDraw[1]
endPt=pointsToDraw[-1]


ptr=1

def circle_line_segment_intersection(circle_center, circle_radius, pt1, pt2, full_line=True, tangent_tol=1e-9):

    """ Find the points at which a circle intersects a line-segment.  This can happen at 0, 1, or 2 points.

    :param circle_center: The (x, y) location of the circle center
    :param circle_radius: The radius of the circle
    :param pt1: The (x, y) location of the first point of the segment
    :param pt2: The (x, y) location of the second point of the segment
    :param full_line: True to find intersections along full line - not just in the segment.  False will just return intersections within the segment.
    :param tangent_tol: Numerical tolerance at which we decide the intersections are close enough to consider it a tangent
    :return Sequence[Tuple[float, float]]: A list of length 0, 1, or 2, where each element is a point at which the circle intercepts a line segment.

    Note: We follow: http://mathworld.wolfram.com/Circle-LineIntersection.html
    """

    (p1x, p1y), (p2x, p2y), (cx, cy) = pt1, pt2, circle_center
    (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
    dx, dy = (x2 - x1), (y2 - y1)
    dr = (dx ** 2 + dy ** 2)**.5
    big_d = x1 * y2 - x2 * y1
    discriminant = circle_radius ** 2 * dr ** 2 - big_d ** 2

    if discriminant < 0:  # No intersection between circle and line
        return []
    else:  # There may be 0, 1, or 2 intersections with the segment
        intersections = [
            (cx + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * discriminant**.5) / dr ** 2,
             cy + (-big_d * dx + sign * abs(dy) * discriminant**.5) / dr ** 2)
            for sign in ((1, -1) if dy < 0 else (-1, 1))]  # This makes sure the order along the segment is correct
        if not full_line:  # If only considering the segment, filter out intersections that do not fall within the segment
            fraction_along_segment = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy for xi, yi in intersections]
            intersections = [pt for pt, frac in zip(intersections, fraction_along_segment) if 0 <= frac <= 1]
        if len(intersections) == 2 and abs(discriminant) <= tangent_tol:  # If line is tangent to circle, return just one point (as both intersections have same location)
            return [intersections[0]]
        else:
            return intersections


def check_pt(fx,cx,fy,cy):
    if((fx*cx) > 0) and ((fy*cy)> 0):
        return True
    return False



def check_direction(curr,next,obs_check):
    check_ptr = []
    check_ptr = circle_line_segment_intersection(obs_check[0:2],obs_check[2],curr[0:2],next[0:2])
    if(check_ptr == []):
        return False

    flag_x = (curr[0] - next[0])
    flag_y = (curr[1] - next[1])
    check_x = (curr[0] - check_ptr[0][0])
    check_y = (curr[1] - check_ptr[0][1])

    if ((flag_x * check_x) > 0)  and ((flag_y * check_y) >0 ):
        return True
    return False

while curPt!=endPt:
    wayPoint_Index+=1
    # array which has all obstacles in our way it has [circle,dist of pt from circle]
    bObs=[]


    l=eqOfLine(curPt,nextPt)
    print("\n\ncurptr -> ",pointsToDraw.index(curPt),curPt)

    # check if our line goes thru any obstacles if so add it to bObs
    # 
    for i in obs:
        print(round(distance(i,curPt)), round(distance(curPt,nextPt)) )
        print(lineInCircle(l,i) , ( distance(i,curPt) < distance(curPt,nextPt) ) , check_direction(curPt,nextPt,i))
        
        if lineInCircle(l,i) and check_direction(curPt,nextPt,i) and ( distance(i,curPt) < distance(curPt,nextPt) ) :
            bObs.append([i,distance(i,curPt)])
            print("bobs",bObs)
    
    # incase no bObs are there then we move to next point
    if len(bObs)==0:    
        if nextPt[-1]=="c":
            curPt=pointsToDraw[ptr+1]
            nextPt=pointsToDraw[ptr+2]
            ptr+=2
        elif nextPt[-1]=="l":
            curPt=nextPt
            if ptr<len(pointsToDraw)-1:
                nextPt=pointsToDraw[ptr+1]
            ptr+=1
        
    # the error is most probably here instead of using waypoints array we should use pointsTDraw
    else:

        # Sort the points in order of distance and take closest circle
        bObs.sort(key=lambda x:x[-1])
        closestCirc=bObs[0][0]

        # Find the point of tangent

        #tangent is always taken from the first case

        d=(distance(closestCirc[0:2],wayPoints[wayPoint_Index])**2-(closestCirc[2])**2)**.5

        dToTpoint=(d**2-float(closestCirc[2])**2)**.5

        # Next point changes to point of tangent
        nextPt=get_intersections(float(wayPoints[wayPoint_Index][0]),float(wayPoints[wayPoint_Index][1]),float(dToTpoint),float(closestCirc[0]),float(closestCirc[1]),float(closestCirc[2]))

        #Getting points for boundary following

        # forgot what fuckery happens here ->>>
            #the current problem 1
        newL=eqOfLine(nextPt,wayPoints[-1])

        a=newL[0]**2+1
        b=(newL[1]*newL[0]-closestCirc[0]-closestCirc[1]*newL[0])*2
        c=closestCirc[0]**2+closestCirc[1]**2-closestCirc[2]**2+newL[1]**2-2*newL[1]*closestCirc[1]
        
        #prevCirc.append(closestCirc)
        x1,x2=quadraticFormula(a,b,c)
        y1=newL[0]*x1+newL[1]
        y2=newL[0]*x2+newL[1]

        # we get angles of the arc which we have to draw
        angles=[parametricAngle((x1,y1),closestCirc),parametricAngle((x2,y2),closestCirc)]
        rect=(closestCirc[0]-closestCirc[2],closestCirc[1]-closestCirc[2],closestCirc[2]*2,closestCirc[2]*2)
        arc.append([angles[0],angles[1],rect])
        
        # insert the points of boundary following into pointToDraw
        pointsToDraw.insert(ptr,[x2,y2,"c"])
        pointsToDraw.insert(ptr+1,[x1,y1,"l"])

        # Assigning the next points
        if nextPt[-1]=="c":
            curPt=pointsToDraw[ptr+1]
            nextPt=pointsToDraw[ptr+2]
            ptr+=2
        elif nextPt[-1]=="l":
            curPt=nextPt
            if ptr<len(pointsToDraw)-1:
                nextPt=pointsToDraw[ptr+1]
            ptr+=1

for i in pointsToDraw:
    print(i)

while True:
    pygame.time.delay(100)

    screen.fill(white)
    for event in pygame.event.get():
        # Allowing program to quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # drawing the obstacles
    for i in obs:
        pygame.draw.circle(screen,green,i[0:2],i[2])
    for i in obs1:
        pygame.draw.circle(screen,blue,i[0:2],i[2])
    # drawing the obstacles
    for i in wayPoints:
        pygame.draw.circle(screen,green,i,10)
    # drawing the points to draw and also the lines we will follow
    for i in range(len(pointsToDraw)-1):
        if pointsToDraw[i][2]=="l":
            pygame.draw.line(screen,red,pointsToDraw[i][0:2],pointsToDraw[i+1][0:2])
        pygame.draw.circle(screen,black,pointsToDraw[i][0:2],3)
    # drawing the straight line from start to end
    pygame.draw.line(screen,red,wayPoints[0],wayPoints[-1])
    # drawing the arcs we will follow
    for i in range(len(arc)):
        if(arc[i][1]>math.pi):
            pygame.draw.arc(screen,black,arc[i][2],2*math.pi-arc[i][0],2*math.pi-arc[i][1],2)
        else:
            pygame.draw.arc(screen,black,arc[i][2],2*math.pi-arc[i][1],-arc[i][0],2)
    pygame.display.update()
    clock.tick(1)