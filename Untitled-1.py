def canBeSumofConsec(n) :
  
    # We basically return true if n is a
    # power of two
    return ((n&(n-1)) and n)
  
  
# Driver code
n = 30
if(canBeSumofConsec(n)) :
    print("true")
else :
    print("false")