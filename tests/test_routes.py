from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()

class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='User')
        cls.note = Note.objects.create(title='title', text='text', author=cls.user)

    def test_page_availability(self):
        urls = (
            ('users:login', None),
            ('users:logout', None),
            ('users:signup', None),
            ('notes:home', None),
        )
        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEquals(response.status_code, HTTPStatus.OK)

    def test_redirect_for_anonymous_client(self):
        login_url = reverse('users:login')
        for name in ('notes:add', 'notes:edit', 'notes:delete'):
            with self.subTest(name=name):
                args = (self.note.slug,)
                if name == 'notes:add':
                    args = None
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)


    def test_availability_for_note_edit_and_delete(self):
        self.client.force_login(self.user)
        for name in ('notes:edit', 'notes:delete'):
            with self.subTest(user=self.user, name=name):
                url = reverse(name, args=(self.note.slug,))
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
