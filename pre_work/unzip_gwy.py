import csv
import os
import zipfile

base_direc = './gwy'
directory = os.listdir('./gwy')

print(directory)
# Iterate over the files in the directory
skipping = []
for file_name in directory:
    file_path = os.path.join(base_direc, file_name)
    if file_name.endswith(".zip"):
        try:
            # Extract the zip file
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # Determine the desired name for the extracted file
                extracted_file_name = os.path.splitext(file_name)[0]
                extracted_file_name = extracted_file_name+".csv"
                # Extract the file and rename it
                zip_ref.extractall(base_direc)
                extracted_files = zip_ref.namelist()
                for extracted_file in extracted_files:
                    if extracted_file.endswith(".csv"):
                        extracted_file_path = os.path.join(base_direc, extracted_file)
                        new_file_path = os.path.join(base_direc, extracted_file_name)
                        os.rename(extracted_file_path, new_file_path)
                print("Unzipped {"+file_name+"} and renamed the csv file to {"+extracted_file_name+"}")
        except:
            print("Skipping {"+file_name+"} - Not a valid zip file")
            skipping.append(file_name)

print(skipping)
print(len(skipping))

for file_name in skipping:
    csv_filename = './gwy/'+os.path.splitext(file_name)[0] + '.csv'

    # Create and write data to the CSV file
    with open(csv_filename, 'w') as csvfile:
        writer = csv.writer(csvfile)

    print("Created CSV file for skipped file: {"+csv_filename+"}")


#
# import csv
# import os
# import zipfile
#
# base_direc = './gwy'
# directory = os.listdir('./gwy')
#
# print(directory)
# # Iterate over the files in the directory
# skipping = []
# for file_name in directory:
#     file_path = os.path.join(base_direc, file_name)
#     if file_name.endswith(".zip"):
#         try:
#             # Extract the zip file
#             with zipfile.ZipFile(file_path, 'r') as zip_ref:
#                 # Determine the desired name for the extracted file
#                 extracted_file_name = os.path.splitext(file_name)[0]
#                 extracted_file_name = extracted_file_name + ".csv"
#                 # Extract the file and rename it
#                 zip_ref.extractall(base_direc)
#                 extracted_files = zip_ref.namelist()
#                 for extracted_file in extracted_files:
#                     if extracted_file.endswith(".csv"):
#                         extracted_file_path = os.path.join(base_direc, extracted_file)
#                         new_file_path = os.path.join(base_direc, extracted_file_name)
#                         os.rename(extracted_file_path, new_file_path)
#                 print(f"Unzipped {file_name} and renamed the csv file to {extracted_file_name}")
#         except zipfile.BadZipFile:
#             print(f"Skipping {file_name} - Not a valid zip file")
#             skipping.append(file_name)
#
# print(skipping)
# print(len(skipping))
#
# for file_name in skipping:
#     csv_filename = './gwy/' + os.path.splitext(file_name)[0] + '.csv'
#
#     # Create and write data to the CSV file
#     with open(csv_filename, 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#
#     print(f"Created CSV file for skipped file: {csv_filename}")