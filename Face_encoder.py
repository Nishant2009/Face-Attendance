from  face_recognition import load_image_file, face_encodings
from os import listdir , path
from json import loads, dumps
from tkinter import messagebox

# CREATING EMPTY DICTIONARIES AND LISTS REQUIRED
new_data = {}
final_dict = {}
new_names = []
old_names = []

# Generating new data
for file in listdir("./BTech/known_faces/"):
    image = load_image_file("./BTech/known_faces/"+file)
    face_encoding = face_encodings(image)[0]
    final_encoding = str(face_encoding).replace("\n","").split()
    new_data[f"{path.splitext(file)[0]}"] = (",").join(final_encoding)

# Converting loaded data to single string
a = str(new_data).replace("'",'"')
b = a.replace(': "[',': [')
c = b.replace(']"',']\n')
new_data = loads(c)

# New data's keys list
list_for_new_names = list(new_data.keys())
for key in list_for_new_names:
    new_names.append(key)

# Reading old data
with open("JSONNAMES.json", "r") as re:
    old_data = re.read()
    json_old = loads(old_data)
    list_for_old_names = list(json_old.keys())
    for key in list_for_old_names:
        old_names.append(key)

# Update or not old data
with open("known_names.json", "r") as knwn_names:
    knwn_names = knwn_names.read()
    known_names = loads(knwn_names)
for old_name in old_names:
    if old_name in list(new_data.keys()) :
        val = messagebox.askyesno("QUERY", f"ROLL NO. {old_name} Name : {known_names[old_name]}\nALREADY EXISTS IN DATABASE, \n\nDO YOU WANT TO UPDATE IT ?")
        if val == True:
            final_dict[old_name] = new_data[old_name]
    else :
        final_dict[old_name] = json_old[old_name]


# Updating New Data in json
for new_name in new_names :
    final_dict[new_name] = new_data[new_name]

# The Final Combined data
final_data_0 = dumps(final_dict)
final_data_1 = final_data_0.replace('{"','{\n\t"')
final_data_2 = final_data_1.replace(', "', ',\n\t"')
final_data = final_data_2.replace("]}","]\n}")

# Writing in temporary file, So that if program closes unexpectedly old data will be safe
with open("JSONNAMES_temp.json", "w") as w:
    w.write(final_data)

# Now writing to final file, As we also have a copy in temperory file
with open("JSONNAMES.json", "w") as w:
    w.write(final_data)