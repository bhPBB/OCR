# OCR com Django e Google Cloud Vision

Este projeto é um site desenvolvido com Django que permite aos usuários fazer upload de imagens ou arquivos PDF para extração de texto, utilizando a API do Google Cloud Vision.
Eu o criei para usar no meu trabalho atual, em que, mensalmente, preciso passar o conteúdo de diversos documentos não estruturados escritos à mão para planilhas de Excel.
A aplicação está hospedada no **Google App Engine** e pode ser acessada diretamente através do link abaixo:

🔗 **[Acessar aplicação online](https://ocr-python-440813.rj.r.appspot.com/)**

---

## Tecnologias Utilizadas

- **[Django](https://www.djangoproject.com/)** – Framework web em Python.
- **[Google Cloud Vision API](https://cloud.google.com/vision)** – Serviço de OCR para detecção de texto em imagens e documentos.
- **[Google App Engine](https://cloud.google.com/appengine)** – Plataforma para hospedagem da aplicação.
- **[Bootstrap](https://getbootstrap.com/)** – Framework CSS para um design responsivo e moderno.

---

## Como Usar

1. Acesse o site:  
   👉 [https://ocr-python-440813.rj.r.appspot.com/](https://ocr-python-440813.rj.r.appspot.com/)

2. Faça upload de uma imagem ou PDF.

3. Clique em "Enviar" para que o sistema leia o conteúdo do arquivo.

4. Aguarde um momento, e o texto extraído será exibido na tela.

---

## Funcionalidades

- Upload de imagens e PDFs.
- Extração de texto com OCR via Google Cloud Vision.
- Interface web simples, funcional e responsiva.
- Serviço totalmente em nuvem, acessível via navegador.

---

## Desenvolvimento Local (opcional)

Caso deseje rodar o projeto localmente:

```bash
git clone https://github.com/bhPBB/OCR.git
cd OCR

# (opcional) criar ambiente virtual
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

pip install -r requirements.txt

# configurar variáveis de ambiente do Google Cloud
export GOOGLE_APPLICATION_CREDENTIALS="caminho/para/credenciais.json"

# executar servidor local
python manage.py migrate
python manage.py runserver
