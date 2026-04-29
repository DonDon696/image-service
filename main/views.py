from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import UploadImage



def index(request):
    return render(request, 'main/index.html')


def upload(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            UploadImage.objects.create(
                original_name=image.name,
                image=image
            )
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


    return render(request, 'main/image_detail.html', {'image': image, 'error': error})

def delete(request):
    massage = None
    error = None
    if request.method == 'POST':
        query = request.POST.get('query')
        if query:
            image = UploadImage.objects.filter(id=query).first()

            if image:
                image.image.delete(save=False)
                image.delete()
                massage = 'Картинка удалена'
            else:
                error = 'Картинка не найдена'

    return render(request, 'main/delete.html', {'error': error, 'massage': massage})

def api_upload_image(request):
    if request.method == "POST":
        image = request.FILES.get('image')

        if not image:
            return JsonResponse({'error': 'Нет такого файла'}, status=400)


        obj = UploadImage.objects.create(original_name=image.name, image=image)

        return JsonResponse({'id': obj.id, 'original_name': obj.original_name, 'image_url': obj.image.url}, status=201)
    return JsonResponse({'error': 'Метод не разрешен'}, status=405)

def api_get_image(request, image_id):
    if request.method == 'GET':
        image = UploadImage.objects.filter(id=image_id).first()

        if image:
            return JsonResponse({'id': image.id, 'original_name': image.original_name, 'image_url': image.image.url}, status=200)
        else:
            return JsonResponse({'error': 'Картинки не существует'}, status=404)

    return JsonResponse({'error': 'Метод не разрешен'}, status=405)

def api_delete_image(request, image_id):
    if request.method != 'DELETE':
        return JsonResponse({'error': 'Метод не разрешен'}, status=405)

    image = UploadImage.objects.filter(id=image_id).first()
    if not image:
        return JsonResponse({'error': 'Картинка не найдена'}, status=404)


    image_id = image.id
    original_name = image.original_name
    image.image.delete(save=False)
    image.delete()
    return JsonResponse({'message': 'Картинка удалена', 'id': image_id, 'original_name': original_name})

