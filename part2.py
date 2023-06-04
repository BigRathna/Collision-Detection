import pygame,sys,random,math,re

#Bounds of the screen
max_x = 800
max_y = 700


#initializing display
pygame.init()
clock=pygame.time.Clock()

screen = pygame.display.set_mode((max_x,max_y))

# colours
blue=(0,0,255)
green=(0,255,0)
red=(255,0,0)
black=(0,0,0)
white=(255,255,255)

#currrent coordinates of the drone
current_cord = []
obstacle_cords = []
relative_cords = []

def distance(p1,p2):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2)**.5

def circleOverlapping(c1,c2):
    d=distance(c1[0:3],c2[0:3])
    if d>(c1[3]+c2[3]):
        return False
    else:
        return True

def draw_circle(x,y,r,cl):
    pygame.draw.circle(screen,cl,(x,y),r)

def calculate_relative( cords ):
    for i in cords:
        rel = (i[0]- current_cord[0][0] ,i[1]- current_cord[0][1]  ,i[2]-current_cord[0][2],i[3])
        relative_cords.append(rel)



while True:
    
    
    screen.fill(white)

    for event in pygame.event.get():
        # Allowing program to quit
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    
    
    pygame.draw.circle(screen,black,[400,350],150,1)
    current_cord.clear()
    obstacle_cords.clear()
    file = open("cords","r")
    p = file.readline()
    curr = tuple(int(x.strip()) for x in p.split(','))
    current_cord.append(curr)
    pygame.draw.circle(screen,green,[400,350],current_cord[0][3])

    #current cord: [0] = x, [1] = y, [2] = z,[3] = r

    
    n=int(file.readline())   
    for i in range(0,n):
        p=file.readline()
        inp=tuple(int(x.strip()) for x in p.split(','))
        obstacle_cords.append(inp)
        #draw_circle(obstacle_cords[i][0],obstacle_cords[i][1],obstacle_cords[i][3],black)

    # MAKING COORDIINATES RELATIVE
    relative_cords.clear()
    calculate_relative(obstacle_cords)

    limit_lower_z = 10
    limit_upper_z = 1000

    for i in relative_cords:
        if(circleOverlapping(i,(0,0,0,150))):
            if(i[2] >= 0  and current_cord[0][2] < limit_upper_z):
                draw_circle(i[0] + (max_x/2),i[1] + (max_y/2),i[3],blue)
                print("move down")
            else:
                if(i[2] < 0 and current_cord[0][2] > limit_lower_z):
                    print("move up")
                    draw_circle(i[0] + (max_x/2),i[1] + (max_y/2),i[3],red)
        else:
            draw_circle(i[0]  + (max_x/2) ,i[1]+ (max_y/2) ,i[3],black)

    


    pygame.display.update()
    screen.fill(white)
    
    clock.tick(1)

