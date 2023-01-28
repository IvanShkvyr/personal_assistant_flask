import bcrypt

from sqlalchemy import and_

from config.config import BASE_DIR
from src.repository.users import inc, create_user
from src.tests.create_test_db import DbTestCase
from src.models import Users, AddressBook


# # py -m unittest discover src/tests

class TestRepositoryUsers(DbTestCase):
    """
    Test the user collection database
    """

    def test_inc(self):
        self.assertEqual(inc(1), 2)

    def test_create_user(self):
        self.session.query(Users).delete()

        self.session.commit()

        login_test = "user_test"
        phone_test = "1111111111"
        pasword_test = "password"
        hash_test = bcrypt.hashpw(pasword_test.encode("utf-8"), bcrypt.gensalt(rounds=10))
        user_test = create_user(login_test, phone_test, pasword_test)
        self.session.add(user_test)
        self.session.commit()
        query = self.session.query(Users).filter(and_(Users.login == login_test, Users.phone == phone_test, Users.hash == hash_test))

        self.assertEqual(1, len(query))



# # py -m unittest discover src/tests
