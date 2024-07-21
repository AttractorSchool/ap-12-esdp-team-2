from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from clubs.models import Club, ClubCategory, City

class ClubsTestCase(TestCase):
    def setUp(self):
        phone_number = '+77478392004'
        password = 'Admin123!'

        user, created = User.objects.get_or_create(phone=phone_number)
        if created:
            user.is_superuser = True
            user.is_active = True
            user.first_name = 'TestFirstName'
            user.last_name = 'TestLastName'
            user.set_password(password)
            user.save()
        self.author = user

        self.assertIsNotNone(user, "User was not created")
        self.assertTrue(user.check_password(password), "Password was not set correctly")

        login_successful = self.client.login(phone=phone_number, password=password)

        self.assertTrue(login_successful, "Login failed in setUp method")

        category = ClubCategory.objects.create(name='Test Category')
        if created:
            category.save()
        city = City.objects.create(name='Test City')
        if created:
            city.iata_code = 'TST'
            city.save()

    def test_club_create(self):
        descriptionText = 'Test Club Description ' * 10
        print(descriptionText)
        category = ClubCategory.objects.filter(is_active=True).first()
        city = City.objects.first()
        print(self.author)
        data = {
            'name': 'Test Club',
            'category': category.id,
            'description': descriptionText,
            'email': 'test@gmail.com',
            'phone': '+77478392004',
            'city': city.id,
        }
        response = self.client.post('/clubs/create/', data=data)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Club.objects.count(), 1)
