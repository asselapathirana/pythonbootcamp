
# below is my 'abosolute path' 
"E:\\teaching\\python_course\\2022\\pythonbootcamp\\2022\\day1\\data\\AHUH1.csv"
# but we'll use relative path
filepath="data/AHUH1.csv"
with open(filepath,"r") as fin:
    text=fin.read()