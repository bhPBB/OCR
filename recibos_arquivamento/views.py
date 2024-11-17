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
        
        # salva arquivo no cloud storage
        file_path = default_storage.save(uploaded_file.name, uploaded_file)
        
        # checa se o arquivo é um pdf
        if uploaded_file.name.endswith('.pdf'):
            response = self.process_pdf(file_path)
        else:
            response = self.process_image(file_path)
        
        # Apaga o arquivo original do bucket
        storage_client = storage.Client()
        bucket = storage_client.bucket(settings.BUCKET)
        blob = bucket.blob(f'media/{file_path}')
        blob.delete()

        return response

    def process_pdf(self, file_path):
        # Inicializa o cliente do cloud vision e do cloud storage 
        client = vision.ImageAnnotatorClient()
        storage_client = storage.Client()

        # inicializa o bucket
        gcs_source_uri = f'gs://{settings.BUCKET}/media/{file_path}'
        output_prefix = 'ocr_results/'

        # Forma a url para enviar o arquivo pdf e receber o arquivo json
        gcs_destination_uri = f'gs://{settings.BUCKET}/{output_prefix}'
        mime_type = 'application/pdf'
        
        input_config = vision.InputConfig(
            gcs_source=vision.GcsSource(uri=gcs_source_uri), mime_type=mime_type
        )
        output_config = vision.OutputConfig(
            gcs_destination=vision.GcsDestination(uri=gcs_destination_uri)
        )

        # Envia o request
        operation = client.async_batch_annotate_files(
            requests=[{
                'input_config': input_config,
                'features': [{'type_': vision.Feature.Type.DOCUMENT_TEXT_DETECTION}],
                'output_config': output_config
            }]
        )

        # Aguarda a operação ser concluída
        operation.result(timeout=300)

        # Recupera o resultado do arquivo json
        bucket = storage_client.bucket(settings.BUCKET)
        blob_list = list(bucket.list_blobs(prefix=output_prefix))

        detected_text = ""

        for blob in blob_list:
            result_data = blob.download_as_text()
            response = vision.AnnotateFileResponse.from_json(result_data)

        for page in response.responses[0].full_text_annotation.pages:
            for block in page.blocks:
                block_text = "" 
                for paragraph in block.paragraphs:
                    paragraph_text = " ".join([
                        "".join([symbol.text for symbol in word.symbols])
                        for word in paragraph.words
                    ])
                    
                    block_text += paragraph_text + "\n"  # Quebra de linha após cada linha
                detected_text += block_text + "\n\n"  # Dupla quebra de linha após cada bloco
                
        # Apaga os resultados
        for blob in blob_list:
            blob.delete()

        # Retorna resposta para o template
        return JsonResponse({'detected_text': detected_text})

    def process_image(self, file_path):
        # Inicializa o cliente do cloud vision
        client = vision.ImageAnnotatorClient()

        # Gera a url do arquivo
        gcs_uri = f'gs://{settings.BUCKET}/media/{file_path}'

        # Processa o arquivo
        imagem = vision.Image(source=vision.ImageSource(gcs_image_uri=gcs_uri))
        response = client.document_text_detection(image=imagem)
        texts = response.full_text_annotation.text

        # Salva o texto em uma variável
        detected_text = texts if texts else "Nenhum texto detectado."
        
        # Retorna o texto para o template
        return JsonResponse({'detected_text': detected_text})

    def form_invalid(self):
        return JsonResponse({'error': 'Invalid form'}, status=400)
    