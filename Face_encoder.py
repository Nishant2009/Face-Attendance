from face_recognition import load_image_file, face_encodings
from os import listdir, path
from json import loads, dumps
from tkinter import messagebox
from dotenv import dotenv_values
import csv

# Initialize locations of the new_faces and face_data directories from the .env file
env_vars = dotenv_values(".env")

new_faces = env_vars.get("NEW_FACES_LOCATION")
face_data = env_vars.get("FACE_DATA_LOCATION")

# Initialize empty dictionaries and lists
new_data = {}
final_dict = {}
new_names = []
old_names = []

# Generate new face encoding data from images in the new_faces directory and if no file is present in the directory, give a message box and exit
if len(listdir(new_faces)) == 0:
    messagebox.showerror("ERROR", "NO IMAGE FILE FOUND IN KNOWN FACES DIRECTORY")
    exit()
for file in listdir(new_faces):
    print(new_faces, file)
    image_path = path.join(new_faces, file)
    image = load_image_file(image_path)
    face_encoding = face_encodings(image)[0]
    final_encoding = str(face_encoding).replace("\n", "").split()
    new_data[f"{path.splitext(file)[0]}"] = (",").join(final_encoding)

# Convert the new data dictionary to a JSON-compatible string
a = str(new_data).replace("'", '"')
b = a.replace(': "[', ': [')
c = b.replace(']"', ']')
new_data = loads(c)

# Create a list of new names from the new data keys
list_for_new_names = list(new_data.keys())
for key in list_for_new_names:
    new_names.append(key)

# Read old data from the Face_Data.json file
try:
    with open(face_data, "r") as re:
        old_data = re.read()
        json_old = loads(old_data)
        list_for_old_names = list(json_old.keys())
        for key in list_for_old_names:
            old_names.append(key)
except:
    json_old = {}

# Read known names from the attendance.csv file
known_names = {}
with open("./Class_Name/attendance.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row if there is one
    for row in reader:
        registration_no, name = row[0], row[1]
        known_names[registration_no] = name

# Update old data based on user input
for old_name in old_names:
    if old_name in list(new_data.keys()):
        val = messagebox.askyesno("QUERY", f"ROLL NO. {old_name} Name : {known_names[old_name]}\nALREADY EXISTS IN DATABASE, \n\nDO YOU WANT TO UPDATE IT ?")
        if val:
            final_dict[old_name] = new_data[old_name]
    else:
        final_dict[old_name] = json_old[old_name]

# Add new data to the final dictionary
for new_name in new_names:
    final_dict[new_name] = new_data[new_name]

# Convert the final dictionary to a formatted JSON string
final_data_0 = dumps(final_dict)
final_data_1 = final_data_0.replace('{"', '{\n\t"')
final_data_2 = final_data_1.replace(', "', ',\n\t"')
final_data = final_data_2.replace("]}", "]\n}")

# Write the final data to the Face_Data.json file
with open(face_data, "w") as w:
    w.write(final_data)