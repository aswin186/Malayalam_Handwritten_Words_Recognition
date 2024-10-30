import os
from hcr.settings import BASE_DIR
import glob

def clearing(image_name):
    img_name = image_name
    os.remove(img_name)


def convert_clearing():
    
    lines_folder = "lines"
    for filename in os.listdir(lines_folder):
        if filename.endswith(".png"):
            img_path = os.path.join(lines_folder, filename)
            os.remove(img_path)

    
    for label in range(100):
        # dirList = glob.glob("pre/"+str(label)+"/*.jpg")
        dirList = glob.glob("characters/"+str(label)+"/*.png") 
        for char_path in dirList:
            os.remove(char_path)

    csv_path = os.path.join(BASE_DIR,'new.csv')
    os.remove(csv_path)