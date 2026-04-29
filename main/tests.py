from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.handlers.exception import response_for_exception
from django.test import TestCase

from .models import UploadImage


class TestApi(TestCase):
    def test_api_upload_image(self):
        file = SimpleUploadedFile(
            name='test.jpg',
            content=b'content',
            content_type='image/jpeg'
        )

        response = self.client.post('/api/images/', {'image': file})

        self.assertEqual(response.status_code, 201)

        data = response.json()

        self.assertIn('id', data)
        self.assertEqual(data['original_name'], 'test.jpg')
        self.assertEqual(UploadImage.objects.count(), 1)

        image_obj = UploadImage.objects.first()
        self.assertEqual(image_obj.original_name, 'test.jpg')

    def test_api_upload_no_file(self):

        response = self.client.post('/api/images/', {})

        self.assertEqual(response.status_code, 400)

        data = response.json()

        self.assertEqual(data['error'], 'Нет такого файла')
        self.assertEqual(UploadImage.objects.count(), 0)

    def test_api_upload_no_post(self):
        response = self.client.get('/api/images/')

        self.assertEqual(response.status_code, 405)

        data = response.json()
        self.assertEqual(data['error'], 'Метод не разрешен')

    def test_api_get_image(self):
        file = SimpleUploadedFile(
            name='file.jpg',
            content=b'content',
            content_type='image/jpeg'
        )

        image = UploadImage.objects.create(
            original_name= file.name,
            image=file
        )
        response = self.client.get(f'/api/images/{image.id}/')

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertIn('id', data)
        self.assertEqual(data['original_name'], 'file.jpg')
        self.assertIn('image_url', data)
        self.assertEqual(data['id'], image.id)

    def test_api_get_image_no_found(self):
        response = self.client.get('/api/images/99/')

        self.assertEqual(response.status_code, 404)

        data = response.json()

        self.assertEqual(data['error'], 'Картинки не существует')

    def test_api_no_get(self):
        response = self.client.post('/api/images/99/')

        self.assertEqual(response.status_code, 405)

        data = response.json()

        self.assertEqual(data['error'], 'Метод не разрешен')

    def test_api_delete_image(self):
        file = SimpleUploadedFile(
            name='file.jpg',
            content=b'content',
            content_type='image/jpeg'
        )
        image = UploadImage.objects.create(
            original_name= file.name,
            image=file
        )

        response = self.client.delete(f'/api/images/{image.id}/delete/')

        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(data['message'], 'Картинка удалена')
        self.assertEqual(data['original_name'], 'file.jpg')
        self.assertEqual(data['id'], image.id)
        self.assertEqual(UploadImage.objects.count(), 0)

    def test_api_delete_image_no_found(self):
        response = self.client.delete('/api/images/99/delete/')

        self.assertEqual(response.status_code, 404)

        data = response.json()

        self.assertEqual(data['error'], 'Картинка не найдена')

    def test_api_no_delete(self):
        response = self.client.get('/api/images/99/delete/')

        self.assertEqual(response.status_code, 405)

        data = response.json()

        self.assertEqual(data['error'], 'Метод не разрешен')
