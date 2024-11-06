# views.py
from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from google.cloud import vision
from google.cloud import storage
from django.core.files.storage import default_storage
from django.conf import settings
from .forms import ImageUploadForm

class OCRUploadView(FormView):
    template_name = 'upload.html'
    form_class = ImageUploadForm
    success_url = reverse_lazy('upload')

    def form_valid(self, form):
        uploaded_file = form.cleaned_data['imagem']
        
        # Save to Google Cloud Storage
        file_path = default_storage.save(uploaded_file.name, uploaded_file)
        
        # Check if the uploaded file is a PDF or image then extract text to variable
        if uploaded_file.name.endswith('.pdf'):
            return self.process_pdf(file_path)
        else:
            return self.process_image(file_path)
        
    def process_pdf(self, file_path):
        # Initialize Vision and Storage clients
        client = vision.ImageAnnotatorClient()
        storage_client = storage.Client()

        # Define GCS URIs
        gcs_source_uri = f'gs://{settings.BUCKET}/media/{file_path}'
        settings.BUCKET
        output_prefix = 'ocr_results/'

        # Setup request for async batch processing of PDF
        gcs_destination_uri = f'gs://{settings.BUCKET}/{output_prefix}'
        mime_type = 'application/pdf'
        
        input_config = vision.InputConfig(
            gcs_source=vision.GcsSource(uri=gcs_source_uri), mime_type=mime_type
        )
        output_config = vision.OutputConfig(
            gcs_destination=vision.GcsDestination(uri=gcs_destination_uri)
        )

        # Send async request
        operation = client.async_batch_annotate_files(
            requests=[{
                'input_config': input_config,
                'features': [{'type_': vision.Feature.Type.DOCUMENT_TEXT_DETECTION}],
                'output_config': output_config
            }]
        )

        # Wait for the operation to complete
        operation.result(timeout=300)

        # Retrieve the JSON result file from GCS
        bucket = storage_client.bucket(settings.BUCKET)
        blob_list = list(bucket.list_blobs(prefix=output_prefix))

        detected_text = ""
        
        for blob in blob_list:
            # Download each JSON result and parse it
            result_data = blob.download_as_text()
            response = vision.AnnotateFileResponse.from_json(result_data)
        
        # Extract structured text from each page in the response
        for page in response.responses[0].full_text_annotation.pages:
            for block in page.blocks:
                block_text = ""  # Gather all text from this block
                for paragraph in block.paragraphs:
                    paragraph_text = " ".join([
                        "".join([symbol.text for symbol in word.symbols])  # Full word
                        for word in paragraph.words
                    ])
                    block_text += paragraph_text + "\n"  # Add paragraph with line break
                detected_text += block_text + "\n\n"  # Double line break between blocks

        # Clean up GCS results
        for blob in blob_list:
            blob.delete()

        # Return JSON response with detected text
        return JsonResponse({'detected_text': detected_text})

    def process_image(self, file_path):
        # Initialize Google Cloud Vision API client
        client = vision.ImageAnnotatorClient()

        # Generate GCS file URI
        gcs_uri = f'gs://{settings.BUCKET}/media/{file_path}'

        # Use the GCS file URI directly in Vision API for image
        imagem = vision.Image(source=vision.ImageSource(gcs_image_uri=gcs_uri))
        response = client.document_text_detection(image=imagem)
        texts = response.full_text_annotation.text

        # Extract detected text
        detected_text = texts if texts else "Nenhum texto detectado."
        
        # Return JSON response
        return JsonResponse({'detected_text': detected_text})

    def form_invalid(self, form):
        return JsonResponse({'error': 'Invalid form'}, status=400)
    