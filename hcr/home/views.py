from django.shortcuts import render,  redirect
from .forms import ImagesForm
from .models import UpImages
from django.http import HttpResponse
import sys
import numpy as np
import os
from subprocess import run, PIPE
import pandas as pd
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from keras.models import load_model
from . import segmentation, converting , delete, pathNorming

# def app_home(request):
#     # return HttpResponse("Hello Aswin")
#     return render(request,'index.html')

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

def OutputFiles(request,id):
    obj_id = UpImages.objects.get(id=id)
    img_db = obj_id.image
    print(img_db)
    new = obj_id.image.url
    print(new)
    norm_path = pathNorming.normPath(new)
    response = HttpResponse(content_type = 'text/plain')
    response['Content-Disposition'] = 'attachment; filename = output.txt'
    #Executing_segmentation
    print(norm_path)
    img = segmentation.openFirstImage(norm_path)
    lines_folder = "lines"
    os.makedirs(lines_folder, exist_ok=True)
    segmentation.lineSegment(img)
    num = segmentation.segment()
    print(num)
    #Generating_csvfile_for_prediction
    out2 = run([sys.executable,'pregen.py'],shell=False,stdout=PIPE)
    #loding_csvfile
    new_df = pd.read_csv('new.csv')
    # Preprocess the new data
    new_data = new_df.iloc[:, 1:].values.reshape(-1, 28, 28, 1).astype('float32') / 255.0
    model = load_model('modelml.h5')
    # Make predictions
    predictions = model.predict(new_data)
    # Get the predicted digit (class with the highest probability)
    predicted_labels = np.argmax(predictions, axis=1)
    print("Predicted Labels:", predicted_labels)
    #Convertin_labels_into_characters
    new_string = converting.convertingToCharacters(predicted_labels, num)
    delete.convertClearing()
    response.writelines(new_string)
    return response

def ClearAll(request,id):
    obj_id = UpImages.objects.get(id=id)
    img_db = obj_id.image
    print(img_db)
    new = obj_id.image.url
    print(new)
    obj_id.delete()
    norm_path = pathNorming.normPath(new)
    delete.clearing(norm_path)
    return redirect('/home/')