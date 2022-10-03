
# below is my 'abosolute path' 
"E:\\teaching\\python_course\\2022\\pythonbootcamp\\2022\\day1\\data\\AHUH1.csv"
# but we'll use relative path
filepath="data/AHUH1.csv"
with open(filepath,"r") as fin:
    text=fin.read()
lines=text.split('\n')

#remove the first line
lines=lines[1:]
# lets loop through each element in the list lines
rain=[]
for val in lines:
    out=val.split(",")
    if len(out) >=2:
        # missing data, marked with 'NA' will be treated as zero - simpliciy
        if out[1]=="NA":
            out[1]=0
        v=float(out[1])
    rain.append(v)
# by here, I have a array (list) of numbers
# I need to sum each consecutive 24 numbers 
#how many 24 blocks do I have?
nb=int(len(rain)/24)
print(nb)
dailyblocks=list(zip(*[iter(rain)]*24))
dailyrain=[sum(x) for x in dailyblocks]
maxdr=max(dailyrain)
print(maxdr)
    
