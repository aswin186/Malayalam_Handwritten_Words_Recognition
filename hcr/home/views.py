from django.shortcuts import render,redirect
from .forms import ImagesForm
from .models import UpImages
from django.http import HttpResponse

import cv2
import sys
import numpy as np
from scipy import ndimage
import os
import glob

import sys
from subprocess import run,PIPE

from hcr.settings import BASE_DIR

import pandas as pd
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
from keras.models import load_model

# Create your views here.

# def app_home(request):
#     # return HttpResponse("Hello Aswin")
#     return render(request,'index.html')


####################################################################################################################################################################################################
####################################                            ####################################################################################################################################
####################################     segmentaion code       ####################################################################################################################################
####################################                            ####################################################################################################################################
####################################################################################################################################################################################################
def openFirstImage(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    ret, img = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY)
    return img

def showImage(img1):
    cv2.imshow('image', img1)
    cv2.waitKey()
    cv2.destroyAllWindows()

def saveImage(img, line_id, folder_path):
    filename = os.path.join(folder_path, f"line_{line_id}.png")
    cv2.imwrite(filename, img)

def lineSegment(img):
    height, width = img.shape
    # print(height, width)
    lines = []
    i = j = 0
    p = False
    start = 0
    line_id = 1

    for i in range(height):
        f = True
        for j in range(width):
            if img[i, j] == 0:  # foreground pixel
                f = False
                p = True
                break
        if f:
            if p:
                img1 = img[start:i, 0:width]
                lines.append(img1)

                saveImage(img1, line_id, "lines")  # Save to the "lines" folder
                line_id += 1

                start = i
                p = False

    for i in range(len(lines)):
        showImage(lines[i])

    return lines

def openImage(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return img

def showImage(img1):
    cv2.imshow('image', img1)
    cv2.waitKey()
    cv2.destroyAllWindows()

def find_connected(img, label, id, i, j, threshold, xmin, ymin, xmax, ymax):
    h, w = img.shape
    
    if img[i, j] < threshold or i >= h-1 or j >= w-1:
        return label, xmin, ymin, xmax, ymax
    else:
        if label[i, j] == 0:
            if j < xmin:
                xmin = j
            if j > xmax:
                xmax = j
            if i < ymin:
                ymin = i
            if i > ymax:
                ymax = i

            label[i, j] = id

            label, xmin, ymin, xmax, ymax = find_connected(img, label, id, i+1, j, threshold, xmin, ymin, xmax, ymax)
            label, xmin, ymin, xmax, ymax = find_connected(img, label, id, i+1, j+1, threshold, xmin, ymin, xmax, ymax)
            label, xmin, ymin, xmax, ymax = find_connected(img, label, id, i, j+1, threshold, xmin, ymin, xmax, ymax)
            label, xmin, ymin, xmax, ymax = find_connected(img, label, id, i-1, j+1, threshold, xmin, ymin, xmax, ymax)
            label, xmin, ymin, xmax, ymax = find_connected(img, label, id, i-1, j, threshold, xmin, ymin, xmax, ymax)
            label, xmin, ymin, xmax, ymax = find_connected(img, label, id, i-1, j-1, threshold, xmin, ymin, xmax, ymax)
            label, xmin, ymin, xmax, ymax = find_connected(img, label, id, i, j-1, threshold, xmin, ymin, xmax, ymax)
            label, xmin, ymin, xmax, ymax = find_connected(img, label, id, i+1, j-1, threshold, xmin, ymin, xmax, ymax)
    return label, xmin, ymin, xmax, ymax

def _main(img, id, line_folder):
    try:
        height, width = img.shape
    except:
        print('Exception occurred in segmentation.py')
        return None

    threshold = 127
    # id = 0
    label = np.zeros((height, width))
    result = []

    for j in range(width):
        for i in range(height):
            if img[i, j] >= threshold and label[i, j] == 0:
                id = id + 1
                label, xmin, ymin, xmax, ymax = find_connected(img, label, id, i, j, threshold, width, height, -1, -1)
                crop_img = img[ymin:ymax, xmin:xmax]

                # Save the cropped image
                save_img(id, img, ymin, ymax, xmin, xmax, line_folder)
                # cv2.imwrite(f'label_{id}.png', crop_img)

                result.append(crop_img)

                img[ymin-2:ymin-1, xmin-1:xmax+1] = 100
                img[ymax+1:ymax+2, xmin-1:xmax+1] = 100
                img[ymin-1:ymax+1, xmin-2:xmin-1] = 100
                img[ymin-1:ymax+1, xmax+1:xmax+2] = 100
    
    return result


def save_img(id, img, ymin, ymax, xmin, xmax, line_folder):
    crop_img = img[ymin:ymax, xmin:xmax]

    characters_folder = os.path.join("characters", line_folder)
    os.makedirs(characters_folder, exist_ok=True)

    # Save each individual image separately with a unique filename
    filename = os.path.join(characters_folder, f'label_{id}.png')
    cv2.imwrite(filename, crop_img)


def segment():
    sys.setrecursionlimit(100000000)
    lines_folder = "lines"
    id = 0
    line_counter = 0  # Initialize line counter
    numchar = []

    # Iterate through images in the "lines" folder
    for filename in os.listdir(lines_folder):
    
        if filename.endswith(".png"):
            img_path = os.path.join(lines_folder, filename)
            img = openImage(img_path)
            # print(f'--> Processing Image: {filename}')
            
            ret, img = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY_INV)
            img = ndimage.median_filter(img, 5)

            line_folder = str(line_counter)  # Use line counter as part of folder name
            # Extract individual lists for each image
            result = _main(img, id, line_folder)

            # Do something with the result for each image (e.g., print the number of components)
            # print(f'Number of components in {filename}: {len(result)}')

            numchar.append(len(result))

            # print('--> Finished Processing Image\n')

            # print(numchar)
        
        # Increment line counter after processing each image
        line_counter += 1

        # Update id with the total number of components processed
        id += len(result)

    return numchar
####################################################################################################################################################################################################
####################################                            ####################################################################################################################################
####################################     segmentaion code       ####################################################################################################################################
####################################                            ####################################################################################################################################
####################################################################################################################################################################################################


def upload_images(request):
    if request.POST:
        form = ImagesForm(request.POST,request.FILES)
        if form.is_valid:
            form.save()
            obj = form.instance
            # return render(request,"index.html",{"obj":obj})
            img = UpImages.objects.all()
            return render(request, 'index.html', {'img': img, "form":form})

    else:
        form = ImagesForm()
    img = UpImages.objects.all()
    return render(request, 'index.html', {'img': img, "form":form})


def OutputFiles(request):
    response = HttpResponse(content_type = 'text/plain')
    response['Content-Disposition'] = 'attachment; filename = output.txt'

    # lines = ["അ ല ൻ\n","സ ര പ \n","സ ന ത \n","ഫ സ ദ"]

#####################################################################################################################################################################
#################################                                 ###################################################################################################
#################################      executing segmentation     ###################################################################################################
#################################                                 ###################################################################################################
#####################################################################################################################################################################
 
    path = os.path.join(BASE_DIR,'media/images/test.jpg')
    # path = "image.jpg"

    print(path)

    # path = input('image path: ')
    img = openFirstImage(path)

    # Create the "lines" folder if it doesn't exist
    lines_folder = "lines"
    os.makedirs(lines_folder, exist_ok=True)

    lineSegment(img)

    num = segment()

    print(num)

#####################################################################################################################################################################
#################################                                 ###################################################################################################
#################################      executing segmentation     ###################################################################################################
#################################                                 ###################################################################################################
#####################################################################################################################################################################



    # out1 = run([sys.executable,'segmentation.py'],shell=False,stdout=PIPE)
    # numchars = out1.stdout
    # print(numchars)

#####################################################################################################################################################################
#################################                                    ################################################################################################
#################################   Generating testing csv file      ################################################################################################
#################################                                    ################################################################################################
#####################################################################################################################################################################

    out2 = run([sys.executable,'pregen.py'],shell=False,stdout=PIPE)
    # out4 = run([sys.executable,'predi.py'],shell=False,stdout=PIPE)

#########################################################################################################################################################
#################################                     ###################################################################################################
#################################      prediction     ###################################################################################################
#################################                     ###################################################################################################
#########################################################################################################################################################


    # Assuming you have a new image in 'new_image.csv'
    new_df = pd.read_csv('new.csv')

    # Preprocess the new data
    new_data = new_df.iloc[:, 1:].values.reshape(-1, 28, 28, 1).astype('float32') / 255.0
    model = load_model('modeldigit.h5')

    # Make predictions
    predictions = model.predict(new_data)

    # Get the predicted digit (class with the highest probability)
    predicted_labels = np.argmax(predictions, axis=1)

    print("Predicted Labels:", predicted_labels)

#########################################################################################################################################################
#################################                                         ###############################################################################
#################################      convertin labels in to classes     ###############################################################################
#################################                                         ###############################################################################
#########################################################################################################################################################    

    chars = predicted_labels
    charsnum = num

    classes = {
        "0": "അ",
        "1": "ആ",
        "2": "ഉ",
        "3": "മ",
        "4": "ഇ",
        "5": "എ",
        "6": "വ",
        "7": "ല",
        "8": "ര",
        "9": "യ",
        "10": "റ",
        "11": "പ",
        "12": 'ാ',
        "13": "ശ",
        "14":  "ന",
        "15": "ി",
        "16": 'ൗ',
        "17": "ഞ",
        "18": "ൽ",
        "19": " ",
}
  

    characters = [classes[str(c)] for c in chars]

    print(characters)

    new_list = []

    # Index for tracking the current position in the 'lines' list
    lines_index = 0

    for c in characters:
        new_list.append(c)
        charsnum[lines_index] -= 1  # Decrease the count for the current line

        if charsnum[lines_index] == 0:  # Check if the count for the current line has reached 0
            new_list.append('\n')  # Add newline character
            lines_index += 1  # Move to the next line count from the 'lines' list
            if lines_index >= len(charsnum):  # Check if all line counts have been processed
                break

    new_list = [str(item) for item in new_list]

    char_string = ', '.join([str(item) for item in new_list])

    symbol_to_remove = ","

    new_string = ""
    for char in char_string:
        if char != symbol_to_remove:
            new_string += char


    # out = run([sys.executable,'test.py',"aswin"],shell=False,stdout=PIPE)

    # print(out)
    # lines = out.stdout
    #to write to file

    response.writelines(new_string)

    return response



def ClearAll(request,id):
    obj_id = UpImages.objects.get(id=id)
    obj_id.delete()

    lines_folder = "lines"
    for filename in os.listdir(lines_folder):
        if filename.endswith(".png"):
            img_path = os.path.join(lines_folder, filename)
            os.remove(img_path)

    image_path = os.path.join(BASE_DIR,'media/images/test.jpg')
    os.remove(image_path)

    for label in range(100):
#       dirList = glob.glob("pre/"+str(label)+"/*.jpg")
        dirList = glob.glob("characters/"+str(label)+"/*.png") 
        for char_path in dirList:
            os.remove(char_path)

    csv_path = os.path.join(BASE_DIR,'new.csv')
    os.remove(csv_path)
    
    return redirect('/home/')