from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.models import Note


User = get_user_model()

class TestContent(TestCase):
    LIST_URL = reverse('notes:list')
    CREATE_URL = reverse('notes:add')

    @classmethod
    def setUpTestData(cls):
        cls.main_user = User.objects.create(username='Main_user')
        cls.another_user = User.objects.create(username='Another_user')



    def test_user_sees_own_notes(self):
        another_user_note = Note.objects.create(
            title='Title', text='text', author=self.another_user
        )
        self.client.force_login(self.main_user)
        response = self.client.get(self.LIST_URL)
        notes = response.context['object_list']
        self.assertNotIn(another_user_note, notes)

    def test_notes_order(self):
        for index in range(2):
            Note.objects.create(
                title=f'Note {index}',
                text=f'{index}',
                author=self.main_user,
            )
        self.client.force_login(self.main_user)
        response = self.client.get(self.LIST_URL)
        notes = response.context['object_list']
        self.assertGreater(notes[1].id, notes[0].id)

    def test_authorized_user_has_form(self):
        self.client.force_login(self.main_user)
        response = self.client.get(self.CREATE_URL)
        self.assertIn('form', response.context)