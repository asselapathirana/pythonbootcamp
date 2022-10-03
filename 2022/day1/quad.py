# first ask the user to enter three numbers a,b,c
# user input is taken as string(text) in python
# so we need to convert them to decimal number using float
a = float(input('Insert a value for variable a'))
b = float(input('Insert a value for variable b'))
c = float(input('Insert a value for variable c'))

# now print the values, just to check
print(a, b, c) 

# calculate b^2-4ac as d
d = b**2 - 4 * a * c 

if d > 0 : # if d is positive
    x1 = (-b + d**0.5)/ (2*a)
    x2 = (-b - d**0.5)/ (2*a)
    print('You have two real and distincts root')
    print(x1, x2)

elif d == 0 : # if d is zero
    x1 = (-b / (2*a))
    
    print('You have one real root')
    print(x1) 

else : # d is niether positive or zeoro, that means negative. 
    print('No real root can be defined')