import os
from hcr.settings import BASE_DIR

def normPath(path):
    new = path
    old_name = os.path.normpath(new)
    image_url = str(os.path.join(BASE_DIR) + str(old_name)).replace('\\','/')
    print(image_url)
    norm_path = os.path.normpath(image_url)
    print(norm_path)
    return norm_path