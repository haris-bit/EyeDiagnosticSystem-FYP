from django.shortcuts import render
from django.contrib import messages

# Import necessary libraries for image processing and classification
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from PIL import Image
from io import BytesIO

def home(request):
    return render(request, 'classifier/page1.html')

# views.py

from django.contrib import messages
from django.shortcuts import render, redirect

def upload_image(request):
    if request.method == 'POST':
        try:
            # Check if an image was uploaded
            if 'image' not in request.FILES:
                raise ValueError('No image selected')

            # Load the deep learning model
            model = load_model('hehe6401.h5')

            # Convert the uploaded image to a numpy array
            image = request.FILES['image']
            image = img_to_array(Image.open(image).resize((64, 64)).convert('RGB'))
            image = np.expand_dims(image, axis=0)

            # Classify the image
            probabilities = model.predict(image)

            # Check if the probability of all predicted classes is below 30%
            if np.all(np.amax(probabilities, axis=1) < 0.3):
                prediction = 'Unable to predict on this image'
            else:
                predictions = np.argmax(probabilities, axis=1)
                if predictions == 0:
                    prediction = 'Nothing, it\'s a Normal eye \U0001F642'
                elif predictions == 1:
                    prediction = 'Cataract'
                elif predictions == 2:
                    prediction = 'Glaucoma'
            

            # Store the prediction in the session
            request.session['prediction'] = prediction

            # Redirect to upload success page
            return redirect('upload_success')

        except:
            return redirect('upload_fail')

    # Render the upload template
    return render(request, 'classifier/page2.html')


def upload_success(request):
    # Check if prediction exists in session
    prediction = request.session.get('prediction')
    if prediction:
 
        # Render the success template with the prediction
        return render(request, 'classifier/page3.html')

    # If prediction doesn't exist, redirect to upload fail
    return redirect('upload_fail')

def upload_fail(request):
    # Render the fail template
    return render(request, 'classifier/page4.html')

def result(request):
    # Retrieve the prediction from the session
    prediction = request.session.get('prediction')

    # Render the result template with the prediction
    return render(request, 'classifier/page5.html', {'prediction': prediction})
