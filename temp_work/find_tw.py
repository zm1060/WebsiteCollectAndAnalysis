input_file_path = "dailyupdate-detailed.txt"
output_file_path = "output_taiwan.txt"

with open(input_file_path, "r") as input_file, open(output_file_path, "w") as output_file:
    for line in input_file:
        fields = line.strip().split(";")

        # 如果任何列包含 "Taiwan" 或 "taiwan"，则写入新文件
        if any("taiwan" in field.strip().lower() for field in fields):
            output_file.write(line)

print("Filtering completed. Check the output file:", output_file_path)
