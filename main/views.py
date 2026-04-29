from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
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

def api_upload_image(request):
    if request.method == "POST":
        image = request.FILES.get('image')

        if not image:
            logger.warning("API: файл не передан при загрузке")
            return JsonResponse({'error': 'Нет такого файла'}, status=400)


        obj = UploadImage.objects.create(original_name=image.name, image=image)

        logger.info("API: изображение загружено: id=%s, имя=%s", obj.id, obj.original_name)

        return JsonResponse({'id': obj.id, 'original_name': obj.original_name, 'image_url': obj.image.url}, status=201)

    logger.warning("API: неверный метод при загрузке: %s", request.method)

    return JsonResponse({'error': 'Метод не разрешен'}, status=405)

def api_get_image(request, image_id):
    if request.method == 'GET':
        image = UploadImage.objects.filter(id=image_id).first()

        if image:
            logger.info("API: запрос изображения: id=%s, имя=%s", image.id, image.original_name)

            return JsonResponse({'id': image.id, 'original_name': image.original_name, 'image_url': image.image.url}, status=200)
        else:
            return JsonResponse({'error': 'Картинки не существует'}, status=404)

    logger.warning("API: изображение не найдено: id=%s", image_id)

    return JsonResponse({'error': 'Метод не разрешен'}, status=405)

def api_delete_image(request, image_id):
    if request.method != 'DELETE':
        logger.warning("API: неверный метод удаления: %s", request.method)
        return JsonResponse({'error': 'Метод не разрешен'}, status=405)

    image = UploadImage.objects.filter(id=image_id).first()
    if not image:
        return JsonResponse({'error': 'Картинка не найдена'}, status=404)


    image_id = image.id
    original_name = image.original_name
    image.image.delete(save=False)
    image.delete()

    logger.info("API: изображение удалено: id=%s, имя=%s", image_id, original_name)

    return JsonResponse({'message': 'Картинка удалена', 'id': image_id, 'original_name': original_name})

