
import cv2
import sys
import numpy as np
from scipy import ndimage
import os

def open_first_image(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    ret, img = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY)
    return img

def show_image(img1):
    cv2.imshow('image', img1)
    cv2.waitKey()
    cv2.destroyAllWindows()

def save_image(img, line_id, folder_path):
    filename = os.path.join(folder_path, f"line_{line_id}.png")
    cv2.imwrite(filename, img)

def line_segment(img):
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

                save_image(img1, line_id, "lines")  # Save to the "lines" folder
                line_id += 1

                start = i
                p = False
    # for i in range(len(lines)):
    #     showImage(lines[i])
    return lines

def open_image(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    return img

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
    id = 0
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

    filename = os.path.join(characters_folder, f'label_{id}.png')
    cv2.imwrite(filename, crop_img)


def segment():
    sys.setrecursionlimit(100000000)
    lines_folder = "lines"
    id = 0
    line_counter = 0  
    numchar = []

    for filename in os.listdir(lines_folder):
    
        if filename.endswith(".png"):
            img_path = os.path.join(lines_folder, filename)
            img = open_image(img_path)
            # print(f'--> Processing Image: {filename}')
            
            ret, img = cv2.threshold(img, 130, 255, cv2.THRESH_BINARY_INV)
            img = ndimage.median_filter(img, 5)

            line_folder = str(line_counter)  
            # Extract individual characters for each image
            result = _main(img, id, line_folder)

            # print(f'Number of components in {filename}: {len(result)}')
            numchar.append(len(result))

            # print('--> Finished Processing Image\n')
            # print(numchar)

        line_counter += 1
        id += len(result)

    return numchar