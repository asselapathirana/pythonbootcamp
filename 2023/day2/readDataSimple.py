csv_file = './data/AHUH1.csv'
rf_mm_list = []

with open(csv_file, 'r') as file:
    next(file)  # Skip the header line
    for line in file:
        values = line.strip().split(',')
        rf_mm = float(values[1]) if values[1] != 'NA' else 0.0
        rf_mm_list.append(rf_mm)

print(rf_mm_list[:100])

resampled_list = []
sum_value = 0

for i, value in enumerate(rf_mm_list):
    sum_value += value
    if (i + 1) % 24 == 0:
        resampled_list.append(sum_value)
        sum_value = 0
print(max(resampled_list))