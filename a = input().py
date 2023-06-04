import math
n =int(input())

check =0 
temp = 1

while(True):
    number = (2*temp)+1+n
    if (math.sqrt(1+(8*number)) % 1 != 0):
        temp+=1
        continue
    else:
        break

print(temp,temp+1)
