from django.shortcuts import render, redirect
from .models import UploadImage
import logging

logger = logging.getLogger(__name__)


def index(request):
    return render(request, 'main/index.html')


def upload(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            obj = UploadImage.objects.create(
                original_name=image.name,
                image=image
            )
            logger.info("Изображение загружено через форму: id=%s, имя=%s", obj.id, obj.original_name)
            return redirect('upload')
        else:
            logger.warning("Ошибка загрузки через форму: файл не передан")
    return render(request, 'main/upload.html')


def image_detail(request):
    image = None
    error = None
    if request.method == 'POST':
        query = request.POST.get('query')
        try:
            image = UploadImage.objects.filter(id=int(query)).first()
        except ValueError:
            image = UploadImage.objects.filter(original_name=query).first()

        if image is None:
            error = 'Картинка не найдена'
            logger.warning("Изображение не найдено (форма): запрос=%s", query)
        else:
            logger.info("Изображение найдено (форма): id=%s, имя=%s", image.id, image.original_name)


    return render(request, 'main/image_detail.html', {'image': image, 'error': error})

def delete(request):
    message = None
    error = None
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            image = UploadImage.objects.filter(id=query).first()

            if image:
                image_id = image.id
                original_name = image.original_name
                image.image.delete(save=False)
                image.delete()
                message = 'Картинка удалена'
                logger.info("Изображение удалено (форма): id=%s, имя=%s", image_id, original_name)
            else:
                error = 'Картинка не найдена'
                logger.warning("Ошибка удаления (форма): изображение не найдено, запрос=%s", query)

    return render(request, 'main/delete.html', {'error': error, 'message': message})




