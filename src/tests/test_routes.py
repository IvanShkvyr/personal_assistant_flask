
from src.tests.create_test_db import DbTestCase


class TestRouters(DbTestCase):

    def test_check(self):
        response = self.client.get("/check")
        self.assertIn("I am working", response.get_data(as_text=True))
        self.assertEqual(200, response.status_code)


    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)


    def test_registration(self):
        # тест що ми бачимо сторінку регістрації
        response = self.client.get("/registration")
        self.assertEqual(200, response.status_code)

        # тест аутентифікації
        # response = self.client.post("/registration", data={"login": "user", "phone": "1111111111", "password": "123456"})
        # self.assertEqual(200, response.status_code)

    def test_login(self):
        # тест що ми бачимо сторінку login
        response = self.client.get("/login")
        self.assertEqual(200, response.status_code)

    
    def test_logout(self):
        # тест що ми не можемо розлогінитися якщо ми не автентифіковані
        response = self.client.get("/logout")
        self.assertEqual(302, response.status_code)


    def test_create(self):
        # тест що ми не можемо зайти на сторінку без авторизації
        response = self.client.get("/create")
        self.assertEqual(302, response.status_code)

    
    def test_update(self):
        # тест що ми не можемо зайти на сторінку без авторизації
        response = self.client.get("/update")
        self.assertEqual(302, response.status_code)


    def test_remove(self):
        # тест що ми не можемо зайти на сторінку без авторизації
        response = self.client.get("/remove")
        self.assertEqual(302, response.status_code)


    def test_show_record(self):
        # тест що ми не можемо зайти на сторінку без авторизації
        response = self.client.get("/show_record")
        self.assertEqual(302, response.status_code)


    def test_show_all(self):
        # тест що ми не можемо зайти на сторінку без авторизації
        response = self.client.get("/show_all")
        self.assertEqual(302, response.status_code)


    def test_days_to_birthday(self):
        # тест що ми не можемо зайти на сторінку без авторизації
        response = self.client.get("/days_to_birthday")
        self.assertEqual(302, response.status_code)
