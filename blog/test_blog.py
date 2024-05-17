from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Project.forms import ContactForm
from .models import BlogPost
from django.contrib.auth import get_user_model


class BlogPostDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = BlogPost.objects.create(title='Test Post', content='Lorem ipsum', slug='test-post', user=self.user)

    def test_blog_post_detail_view(self):
        client = Client()
        url = reverse('post_detail', kwargs={'slug': self.post.slug})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'detail.html')
        self.assertEqual(response.context['object'], self.post)

    def test_blog_post_detail_view_invalid_slug(self):
        client = Client()
        url = reverse('post_detail', kwargs={'slug': 'invalid-slug'})
        response = client.get(url)
        self.assertEqual(response.status_code, 404)


class RegisterNewUserViewTest(TestCase):

    def test_register_view(self):
        url = reverse('register')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')
        self.assertContains(response, 'id="id_username"')
        self.assertContains(response, 'id="id_email"')
        self.assertContains(response, 'id="id_password1"')
        self.assertContains(response, 'id="id_password2"')

    def test_register_submission(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username='testuser').exists())


class ContactPageTestCase(TestCase):
    def test_contact_page_GET(self):

        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertIsInstance(response.context['form'], ContactForm)

    def test_contact_page_POST_invalid_data(self):

        data = {}
        response = self.client.post(reverse('contact'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'form.html')
        self.assertIsInstance(response.context['form'], ContactForm)


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_login_view_GET(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_view_POST(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302)  # Oczekujemy przekierowania po zalogowaniu
        self.assertRedirects(response, reverse('home'))
