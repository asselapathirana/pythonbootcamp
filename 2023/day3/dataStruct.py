for value in [1, 2, 3, 4, 5]:
    print(value)
    
i=0
for value in ['apple', 'pears', 'bananas']:
    print(i, value)
    i+=1
    
for i, value in enumerate(['apple', 'pears', 'bananas']):
    print(i, value)

for value in range(10):
    print(value)
print ("-------------------")
for value in range(5, 10):
    print(value)

print ("-------------------")

for value in range(20, 0, -2):
    print(value)

print ("-------------------")
[print(value) for value in range(10)]
   
   
print ("-------------------")

# tuples
values=(1, 2, 3, 4, 5)

students ={"John": "A", "Mary": "B", "Mike": "C"}
print(students["John"])
print(list(students.keys()))
print(list(students.values()))

for key, value in students.items():
    print(key, value)
print("-------------------")
students ={"John": [80,90, 85], "Mary": [25, 95, 100], "Mike": [75, 45, 80]}
print(students["John"])

students2={ key: value[0]/10. for key, value in students.items()}
print(students2)
    