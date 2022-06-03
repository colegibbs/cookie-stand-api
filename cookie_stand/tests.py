from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CookieStand


class CookieStandTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        testuser1 = get_user_model().objects.create_user(
            username="testuser1", password="pass"
        )
        testuser1.save()

        test_cookie_stand = CookieStand.objects.create(
            location="Seattle",
            owner=testuser1,
            description="Tasty Cookies",
            hourly_sales=["Money"],
            minimum_customers_per_hour=1,
            maximum_customers_per_hour=2,
            average_cookies_per_sale=4.0,
        )
        test_cookie_stand.save()

    def setUp(self):
        self.client.login(username="testuser1", password="pass")

    def test_cookie_stand_model(self):
        cookie_stand = CookieStand.objects.get(id=1)
        actual_owner = str(cookie_stand.owner)
        actual_location = str(cookie_stand.location)
        actual_hourly_sales = cookie_stand.hourly_sales
        actual_description = str(cookie_stand.description)
        actual_minimum_customers_per_hour = str(cookie_stand.minimum_customers_per_hour)
        actual_maximum_customers_per_hour = str(cookie_stand.maximum_customers_per_hour)
        actual_cookies_per_sale = str(cookie_stand.average_cookies_per_sale)
        self.assertEqual(actual_owner, "testuser1")
        self.assertEqual(actual_location, "Seattle")
        self.assertEqual(actual_hourly_sales, ["Money"])
        self.assertEqual(
            actual_description, "Tasty Cookies"
        )
        self.assertEqual(actual_minimum_customers_per_hour, "1")
        self.assertEqual(actual_maximum_customers_per_hour, "2")
        self.assertEqual(actual_cookies_per_sale, "4.0")

    def test_get_thing_list(self):
        url = reverse("cookie_stand_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cookie_stand = response.data
        self.assertEqual(len(cookie_stand), 1)
        self.assertEqual(cookie_stand[0]["location"], "Seattle")

    def test_get_thing_by_id(self):
        url = reverse("cookie_stand_detail", args=(1,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cookie_stand = response.data
        self.assertEqual(cookie_stand["location"], "Seattle")

    def test_create_thing(self):
        url = reverse("cookie_stand_list")
        data = {
            "location": "Portland",
            "owner": 1,
            "description": "homey",
            "hourly_sales": ["Moneyness"],
            "minimum_customers_per_hour": 2,
            "maximum_customers_per_hour": 4,
            "average_cookies_per_sale": 4.0,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        cookie_stand = cookie_stand.objects.all()
        self.assertEqual(len(cookie_stand), 2)
        self.assertEqual(cookie_stand.objects.get(id=2).location, "Portland")

    def test_update_thing(self):
        url = reverse("cookie_stand_detail", args=(1,))
        data = {
            "location": "Portland",
            "owner": 1,
            "description": "my cookie is made of dirt. ",
            "hourly_sales": ["Moneyness"],
            "minimum_customers_per_hour": 2,
            "maximum_customers_per_hour": 4,
            "average_cookies_per_sale": 4.0,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cookie_stand = CookieStand.objects.get(id=1)
        self.assertEqual(cookie_stand.owner, data["owner"])
        self.assertEqual(cookie_stand.location, data["location"])
        self.assertEqual(cookie_stand.hourly_sales, data["hourly_sales"])
        self.assertEqual(
            cookie_stand.description, data["my cookie is made of dirt. "]
        )
        self.assertEqual(cookie_stand.minimum_customers_per_hour, data["minimum_customers_per_hour"])
        self.assertEqual(cookie_stand.maximum_customers_per_hour, data["maximum_customers_per_hour"])
        self.assertEqual(cookie_stand.cookies_per_sale, data["average_cookies_per_sale"])


    def test_delete_thing(self):
        url = reverse("cookie_stand_detail", args=(1,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        cookie_stand = CookieStand.objects.all()
        self.assertEqual(len(cookie_stand), 0)

    def test_authentication_required(self):
        self.client.logout()
        url = reverse("cookie_stand_detail", args=(1,))
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
