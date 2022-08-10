"""
Find the maximum 24h rainfall from a hourly record. 
Using just plain python (no fancy libraries!)
"""

with open('data/funabashi_rainfall.txt') as f:
    count = 0
    sum = 0
    maxv = 0
    
    while True:
        if count%24 == 0:
            #print(sum)
            if sum > maxv:
                maxv = sum
            sum = 0
        count += 1
            
        line = f.readline()
        if not line:
            break
        val = line.split()[-1]
        sum += int(val)
        # print(count, val)

    print("Maximum 24h rainfall value ", maxv)
