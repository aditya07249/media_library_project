from celery import shared_task
from .models import MediaFile
import os
from PIL import Image
import PyPDF2
import ffmpeg

@shared_task
def extract_metadata_task(file_id):
    media = MediaFile.objects.get(id=file_id)
    path = media.file.path
    metadata = {}

    try:
        if media.extension in ['.jpg', '.png']:
            with Image.open(path) as img:
                metadata['width'], metadata['height'] = img.size
        elif media.extension == '.pdf':
            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                metadata['pages'] = len(reader.pages)
        elif media.extension in ['.mp4', '.mp3']:
            probe = ffmpeg.probe(path)
            metadata['duration'] = float(probe['format']['duration'])
    except Exception as e:
        metadata['error'] = str(e)

    media.metadata = metadata
    media.save()
