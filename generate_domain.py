import os

all_file = []
count = 0
for filename in os.listdir('./domain_txt'):
    if filename.endswith('.txt'):
        all_file.append(filename.split('.txt')[0])
        count += 1
print(all_file)
print(count)