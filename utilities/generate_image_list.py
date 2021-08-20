import os 
import argparse
from pathlib import Path

def generate_path_list(dir_path, save_path, name)->None:
    
    f = open(Path(save_path)/Path(name),'w') 
    list_of_folders = os.listdir(dir_path)

    for folder in list_of_folders:
        list_of_files = os.listdir(Path(dir_path)/Path(folder))

        list_of_files.sort(key=lambda f: int(os.path.splitext(f)[0]))
        #number of files < 10
        if (len(list_of_files) < 10):
            print(folder, " has ", len(list_of_files), " frames ")
        for image in list_of_files:
            single_image_path = Path(folder)/Path(image) 
            f.write(str(single_image_path)+"\n")
    
    f.close()


if __name__== '__main__':
    parser = argparse.ArgumentParser(prog='Generate a list of image paths')
    
    parser.add_argument('-f', '--folder', type=str, required=True,
                        help='Folder to image files i.e. /images/train')

    parser.add_argument('-s', '--savepath', type=str, required=True,
                        help='path that saves the list')

    parser.add_argument('-n', '--name', type=str, required=True, help="name of the list")

    args = parser.parse_args()
    
    generate_path_list(args.folder, args.savepath, args.name)