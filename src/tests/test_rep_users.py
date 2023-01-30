import bcrypt

from sqlalchemy import and_

from src.models import Users
from src.repository.users import create_user, find_by_login, login
from src.tests.create_test_db import DbTestCase


class TestRepositoryUsers(DbTestCase):
    """
    Test the user collection database
    """

    def _create_userss_record(self, login, phone, raw_pasword):
        hash_test = bcrypt.hashpw(raw_pasword.encode("utf-8"), bcrypt.gensalt(rounds=10))
        record = Users(login=login, phone=phone, hash=hash_test)                   
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        query = self.session.query(Users).filter(Users.login == login).first()
        return query

    def test_create_user(self):
        login_test = "user_1"
        phone_test = "1111111111"
        pasword_test = "password"
        user_test = create_user(login_test, phone_test, pasword_test, self.session)
        self.session.refresh(user_test)
        query = self.session.query(Users).filter(and_(Users.login == login_test, Users.phone == phone_test)).first()
        self.assertTrue(bcrypt.checkpw(pasword_test.encode("utf-8"), query.hash))
        self.assertTrue(query)

    def test_find_by_login(self):
        query = self._create_userss_record(login="user_2", phone="2222222222", raw_pasword="password")
        login_user_2 = query.login
        find_user = find_by_login(login_user_2, self.session)
        self.assertTrue(find_user)

    def test_login(self):
        query = self._create_userss_record(login="user_3", phone="3333333333", raw_pasword="password")
        login_user_3 = query.login
        login_user = login(login_user_3, "password", self.session)
        self.assertTrue(login_user)
        
# py -m unittest discover src/tests
