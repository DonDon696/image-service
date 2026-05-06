import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import UploadImage
from pytest import fixture
from django.urls import reverse

@fixture(scope="session")
def file_image():
    file = SimpleUploadedFile(
        name='test.jpg',
        content=b'hello',
        content_type='image/jpeg'
    )
    return file

def test_index(client):
    response = client.get(reverse('index'))

    assert response.status_code == 200


@pytest.mark.django_db
def test_upload_positive(client, file_image):
    response = client.post('/upload/', {'image': file_image})
    assert response.status_code == 200

    assert UploadImage.objects.count() == 1

    obj = UploadImage.objects.first()
    assert obj.original_name == file_image.name

@pytest.mark.django_db
def test_upload_negative(client):
    response = client.post('/upload/', {})

    assert response.status_code == 200
    assert UploadImage.objects.count() == 0

@pytest.mark.django_db
def test_upload_not_post(client, file_image):
    response = client.get('/upload/', {'image': file_image})
    assert response.status_code == 200
    assert UploadImage.objects.count() == 0


@pytest.mark.django_db
def test_image_detail_positive(client, file_image):
    obj = UploadImage.objects.create(original_name= file_image.name, image= file_image)

    response = client.post('/image_detail/', {'query': str(obj.id)})

    assert response.status_code == 200
    assert response.context['image'] == obj
    assert response.context['error'] is None

@pytest.mark.django_db
def test_image_detail_positive_name(client, file_image):
    obj = UploadImage.objects.create(original_name= file_image.name, image= file_image)

    response = client.post('/image_detail/', {'query': obj.original_name})

    assert response.status_code == 200
    assert response.context['image'] == obj
    assert response.context['error'] is None

@pytest.mark.django_db
def test_image_detail_negative(client):
    response = client.post('/image_detail/', {'query': '999'})
    assert response.status_code == 200
    assert response.context['image'] is None
    assert response.context['error'] is not None

@pytest.mark.django_db
def test_image_detail_negative_name(client):
    response = client.post('/image_detail/', {'query': 'none.jpg'})
    assert response.status_code == 200
    assert response.context['image'] is None
    assert response.context['error'] is not None

def test_image_detail_not_post(client):
    response = client.get('/image_detail/')

    assert response.status_code == 200
    assert response.context['image'] is None
    assert response.context['error'] is None


@pytest.mark.django_db
def test_delete_positive(client, file_image):
    obj = UploadImage.objects.create(original_name=file_image.name, image=file_image)

    response = client.post('/delete/', {'query': str(obj.id)})

    assert UploadImage.objects.count() == 0
    assert response.status_code == 200
    assert response.context['message'] == 'Картинка удалена'
    assert response.context['error'] is None

@pytest.mark.django_db
def test_delete_negative(client, file_image):
    obj = UploadImage.objects.create(original_name=file_image.name, image=file_image)

    assert UploadImage.objects.count() == 1

    response = client.post('/delete/', {'query': '999'})

    assert UploadImage.objects.count() == 1
    assert UploadImage.objects.first().id == obj.id
    assert response.status_code == 200
    assert response.context['error'] == 'Картинка не найдена'
@pytest.mark.django_db
def test_delete_not_post(client, file_image):
    obj = UploadImage.objects.create(original_name=file_image.name, image=file_image)
    assert UploadImage.objects.count() == 1

    response = client.get('/delete/')

    assert response.status_code == 200
    assert UploadImage.objects.count() == 1
    assert response.context['message'] is None
    assert response.context['error'] is None
    assert UploadImage.objects.first().id == obj.id
