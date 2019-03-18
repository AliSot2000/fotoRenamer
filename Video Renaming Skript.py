import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS




#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Version of the Skript
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


print("Skript zur Änderung der Nomenklatur der Fotos")
print("Version 1.0")
print("Date of creation = 23.12.2018")
print("Autor = AliSot2000")
print("This script requires the exiftool from Phil Harvey")
print("You can find the install for this tool at: \nhttp://owl.phy.queensu.ca/~phil/exiftool/")
print("This script is tested on Mac and may need some adjustment for Windows or Linux")
print("Do not hesitate to ad additional instances of Date and Time")
print("ALL FOLDER NAMES MUST NOT INCLUDE SPACES, OTHERWISE THE SCRIPT WILL FAIL")
print("\n \n \n \n")
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Input of User
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


#File path: all files at this location are going to be renamed.
filepath = None
while not filepath:
    filepath = input("please enter the filepath \n")

#File path under which the renamed files are going to be stored:
new_filepath = input("Enter the filepath of the new safelocation \n")
if not new_filepath:
    new_filepath = filepath

#Separator between the time and the date. Exemple: 2018:12:23_13:45:00;
# separator would be _
separator_datetime = input("this will separate the date and time \n")
if not separator_datetime:
    separator_datetime = "_"

#Separator between the values of time and date, Exemple: 2018:12:23_13:45:00;
# separator would be :
separator_value = input("this will sparate the values \n")
if not separator_value:
    separator_value = ":"

#Prints all files in this location.
content = os.listdir(path=filepath)
print("The content is:")
for q in range(len(content)):
    print(content[q])


#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#Main algorithm
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


#Initialising some variables for later
metadata_list = []
metadata_dict = {}
translate_list = []
error_list = []
number_of_files = len(content)
new_filenames_list = []

#Iterating over files in folder
for i in range(len(content)):
    print("Processing File " + str(i + 1) + " of " + str(number_of_files))
    filename = content[i]

    #the phil harvey script doesn't work with spaces, so the spaces are replaced for the processing
    if " " in filename:
        print("space found in Filename")
        modify_filename = filename.replace(" ", "_")
        os.rename(fullpath, filepath +"/"+ modify_filename)
        fullpath = filepath + "/" + modify_filename
    else:
        fullpath = filepath + "/" + filename
    #Separating the Filename and Fileextention
    f_name, f_type = os.path.splitext(fullpath)

    #Excepting System file .DS_Store
    if (filename !=".DS_Store"):
        #entering the command into the terminal
        metadata = os.popen("exiftool " + fullpath).read()
        #splitting the output of the terminal at every line break
        metadata_list = metadata.split("\n")

        #Iterating over the Elements of the Metadata to creat a dictionairy
        for b in range(len(metadata_list)):
            current_entry = metadata_list[b]
            #splitting singel list entrys into two elements
            translate_list = current_entry.split(": ", 1)

            if len(translate_list) == 2:
                key = translate_list[0]
                key = key.replace(" ", "_", 1)
                key = key.replace(" ", "")
                metadata_dict[key] = translate_list[1]
            elif len(translate_list) < 2:
                metadata_dict[translate_list[0]] = None
                print(translate_list[0] + "No Value for Element " + translate_list[0] + "; Current Filename = "+ filename)


#Trying to get the date from the metadata
        try:

#Searching the right dataset inside the metadata_dict
            try:
                creation_date_time = metadata_dict.get("Create_Date")
                print("Create_Date found, Value = " + creation_date_time)
            except:
                print("Metadata has no Element: Create_Date")


            date, time = creation_date_time.split(" ")
            print(date, time)
    #Removing eventual milliseconds values in time

            try:
                a, b = time.split(".")
                time_list = []
                time_list = a.split(":")
            except ValueError:
                time_list = time.split(":")

            date_list = date.split(":")
            print(date_list, time_list)
    #Defining the new Filename
            new_filename = (date_list[0] + separator_value + date_list[1] + separator_value +
                            date_list[2] + separator_datetime + time_list[0] + separator_value +
                            time_list[1] + separator_value + time_list[2])
            not_new_filename = True
            while not_new_filename:
                not_new_filename = True
                if new_filename in new_filenames_list:
                    print("Duplicate found" + new_filename)
                    new_filename = new_filename + "|"
                else:
                    not_new_filename = False
                    print("No Duplicat found")


            new_filenames_list.append(new_filename)
            print(new_filename)
            new_fullpath = new_filepath + "/" + new_filename + f_type

            os.rename(fullpath, new_fullpath)
            print("File " + fullpath + " successfully renamed to " + new_fullpath + "\n")





        except:
            print("No Matching Metadata found " + filename)
            error_list.append(fullpath)



if len(error_list) > 0:
    print(" \n \nSome errors occured with the following files: \n \n")
    for i in range(len((error_list))):
        print(error_list[i])

print("\n \nDone")
#6328
