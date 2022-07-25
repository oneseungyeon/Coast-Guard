import shutil
import glob
import os

file_path = './frame_1/'
copy_path = './frame_image/'
folder_list = list(glob.glob(os.path.join(file_path, '*')))
# print(folder_list)
i =0
for folder in folder_list:
    # print(folder)
    file_list = list(glob.glob(os.path.join(folder, '*')))
    for file in file_list:
        print(file)
        shutil.copy(file, copy_path + file.split('\\')[-1])
        print("done")
    print("Really DONE!")

print("Really Really DONE!!")