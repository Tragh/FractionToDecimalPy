# Author: Michael M
# Author site: https://github.com/Tragh
# License: MIT
# Date: 2018-02-20


import sys
import math

#Factors n, returning the result as a dict of prime,power pairs
#this is far from the most efficient algorithm but it's okay
def Factor(n):
    rvalue=dict()
    start=2
    while n>1:
        sqrtn=int(math.sqrt(n))
        for d in range(start,sqrtn+1): #check up to root n
            if n%d==0: #then we have prime factor
                p=0 #find highest power of d dividing n
                ppow=d
                while (n%ppow)==0:
                    p+=1;
                    ppow*=d;
                rvalue[d]=p #add to dict
                ppow//=d #highest power dividing
                n//=ppow #new n
                start=d+1 #new start
                break;
        else: #so n is prime
            rvalue[n]=1
            break;
    return rvalue

#Finds the highest power of factor that divides num
def HighestFactor(num,factor):
    if num==0: return -1
    pow=factor
    rvalue=0
    while (num % pow) == 0:
        pow*=factor
        rvalue+=1
    return rvalue

#Finds (somewhat efficiently) the least n such that d divides 10**n - 1 by factoring Euler's totient of d
def F(d):
    if d==0: return 0
    def MergeFactor(dictionary, key, value):
        if key in dictionary:
            dictionary[key]+=value
        else:
            dictionary[key]=value
    #First to calculate the totient of d one factors d
    totient=1
    totientFactors=dict()
    fact=Factor(d)
    #This next loop is cheeky (efficient) and doing two jobs
    #first calculating the totient using its multiplicative property
    #and factoring the totient (since in calculating it we learn of its factors)
    for prime, power in fact.items():
        MergeFactor(totientFactors,prime,power-1)
        f=Factor(prime-1)
        for prime2,power2 in f.items():
            MergeFactor(totientFactors,prime2,power2)
        totient*=(prime-1)*prime**(power-1)
    #At this point we know the totient of d, and the factors of the totient.
    #the lowest n such that d divides 10**n - 1 is a factor of the totient
    #this will destructively iterate over the factors of the totient
    #the totient variable is re-purposed to find n
    while len(totientFactors)!=0:
        prime,power=totientFactors.popitem()
        while (10**(totient//prime)-1)%d == 0 and power!=0:
            totient//=prime
            power-=1

    return totient


# Code entry point #######################################################################################################
if len(sys.argv)<2:
    print("The first argument must be a fraction e.g. 23/26")
    quit()
try:
    p,q=sys.argv[1].split("/")
    p=int(p)
    q=int(q)
except ValueError:
    print("Invalid Fraction")
    quit()
if q==0:
    print("div/0")
    quit()


#p/q is the fraction we're working width

#A is the part before the decimal point
A=p//q
p=p%q

#Here we make the denominator co-prime to 10 and end up with a factor of 1/10**c
a=HighestFactor(q,2)
b=HighestFactor(q,5)
c=max(a,b)
p=p*2**(c-a)*5**(c-b)
q=q//2**a//5**b

#B is the non-repeating part
B=p//q
p=p%q

#use F to find the length of the repeating part
n=F(q)
#calculate the repeating part, we know q divides (10**n-1)
C=((10**n-1) // q)*p

#print the result
print(A, end='')
if C!=0 or B!=0: print(".", end='')
if c!=0 and (C!=0 or B!=0): print('{0:0{width}}'.format(B, width=c), end='')
if n!=0 and C!=0: print("["+'{0:0{width}}'.format(C, width=n)+"]", end='')
print("")

print("Fixed part has length: {}".format(c))
print("Repeating part has period: {}".format(n))
