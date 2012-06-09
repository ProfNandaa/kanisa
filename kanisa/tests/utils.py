from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class KanisaViewTestCase(TestCase):
    def setUp(self):
        bob = User.objects.create_user('bob', '', 'secret')
        bob.is_staff = False
        bob.save()

        fred = User.objects.create_user('fred', '', 'secret')
        fred.is_staff = True
        fred.save()

    def check_staff_only(self, view_name):
        # Not logged in
        url = reverse(view_name)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'admin/login.html')

        # Logged in as non-staff member
        self.client.login(username='bob', password='secret')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'admin/login.html')
        self.client.logout()
