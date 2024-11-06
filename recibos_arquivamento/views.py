# views.py
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.http import JsonResponse
from google.cloud import vision
from .forms import ImageUploadForm
from django.core.files.storage import default_storage
from django.conf import settings

class OCRUploadView(FormView):
    template_name = 'upload.html'
    form_class = ImageUploadForm
    success_url = reverse_lazy('upload')

    def form_valid(self, form):
        # Get the uploaded image file
        uploaded_file = form.cleaned_data['imagem']
        
        # Save to Google Cloud Storage
        file_path = default_storage.save(uploaded_file.name, uploaded_file)

        # Initialize Google Cloud Vision API client
        client = vision.ImageAnnotatorClient()

        # Generate GCS file URI
        gcs_uri = f'gs://{settings.BUCKET}/media/{file_path}'

        # Use the GCS file URI directly in Vision API
        imagem = vision.Image(source=vision.ImageSource(gcs_image_uri=gcs_uri))
        response = client.text_detection(image=imagem)
        texts = response.text_annotations

        # Extract detected text
        detected_text = texts[0].description if texts else "No text detected"
        
        # Return JSON response
        return JsonResponse({'detected_text': detected_text})

    def form_invalid(self, form):
        return JsonResponse({'error': 'Invalid form'}, status=400)
