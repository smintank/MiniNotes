from http import HTTPStatus

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.models import Note
from notes.forms import WARNING


User = get_user_model()


class TestLogic(TestCase):
    NOTE_TEXT = 'text1'
    NEW_NOTE_TEXT = 'text2'


    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='User1')
        cls.another_user = User.objects.create(username='User2')
        cls.auth_client_1 = Client()
        cls.auth_client_1.force_login(cls.user)
        cls.auth_client_2 = Client()
        cls.auth_client_2.force_login(cls.another_user)
        cls.note = Note.objects.create(
            title='title', text=cls.NOTE_TEXT, author=cls.user, slug='slug'
        )
        note_slug = cls.note.slug
        cls.create_url = reverse('notes:add')
        cls.edit_url = reverse('notes:edit', args=(note_slug,))
        cls.delete_url = reverse('notes:delete', args=(note_slug,))
        cls.success_url = reverse('notes:success')

    def test_user_cant_edit_comment_of_another_user(self):
        response = self.auth_client_2.post(self.edit_url, data={
            'title': 'title', 'text': self.NEW_NOTE_TEXT
        })
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NOTE_TEXT)

    def test_user_can_edit_note(self):
        response = self.auth_client_1.post(self.edit_url, data={
            'title': 'title', 'text': self.NEW_NOTE_TEXT
        })
        self.assertRedirects(response, self.success_url)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, self.NEW_NOTE_TEXT)

    def test_another_user_cant_delete_comment_of_user(self):
        response = self.auth_client_2.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

    def test_user_can_delete_note(self):
        response = self.auth_client_1.delete(self.delete_url)
        self.assertRedirects(response, self.success_url)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 0)

    # def test_unique_slug_warning(self):
    #     response = self.auth_client.post(self.create_url, data={
    #         'title': 'title2', 'text': 'text2', 'slug': 'slug', 'author': self.user.id
    #     })
    #     print(response.context)
    #     self.assertFormError(
    #         response,
    #         form='form',
    #         field='slug',
    #         errors=WARNING
    #     )
    #     notes_count = Note.objects.count()
    #     self.assertEqual(notes_count, 1)

    def test_user_can_create_note(self):
        response = self.auth_client_1.post(self.create_url, data={
            'title': 'title', 'text': self.NEW_NOTE_TEXT
        })
        self.assertRedirects(response, self.success_url)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 2)
        note = Note.objects.last()
        self.assertEqual(note.text, self.NEW_NOTE_TEXT)
        self.assertEqual(note.title, 'title')
        self.assertEqual(note.author, self.user)

    def test_anonymous_user_cant_create_note(self):
        self.client.post(self.create_url, data={
            'title': 'title', 'text': self.NEW_NOTE_TEXT
        })
        notes_count = Note.objects.count()
        self.assertEqual(notes_count, 1)

