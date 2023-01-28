import bcrypt
from datetime import datetime
import unittest

from sqlalchemy import and_

from config.config import BASE_DIR
from src.repository.users import create_user, find_by_login, login
from src.repository.records import get_record_user, create_record, update_record
from src.tests.create_test_db import DbTestCase
from src.models import Users, AddressBook

# # py -m unittest discover src/tests

class TestRepositoryUsers(DbTestCase):
    """
    Test the user collection database
    """

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
        login_test = "user_2"
        phone_test = "2222222222"
        pasword_test = "password"
        hash_test = bcrypt.hashpw(pasword_test.encode("utf-8"), bcrypt.gensalt(rounds=10))
        user_2 = Users(login=login_test, phone=phone_test, hash=hash_test)
        self.session.add(user_2)
        self.session.commit()
        self.session.refresh(user_2)
        find_user = find_by_login(login_test, self.session)

        self.assertEqual(user_2, find_user)

    def test_login(self):
        login_test = "user_3"
        phone_test = "3333333333"
        pasword_test = "password"
        hash_test = bcrypt.hashpw(pasword_test.encode("utf-8"), bcrypt.gensalt(rounds=10))
        user_3 = Users(login=login_test, phone=phone_test, hash=hash_test)
        self.session.add(user_3)
        self.session.commit()
        self.session.refresh(user_3)
        login_user = login(login_test, pasword_test, self.session)

        self.assertTrue(login_user)
        
        
class TestRepositoryRecords(DbTestCase):
    """
    Test the records collection database
    """

    def test_get_record_user(self):
        
        record_1 = AddressBook(user_id=111)
        self.session.add(record_1)
        self.session.commit()
        self.session.refresh(record_1)

        query = self.session.query(AddressBook).filter(AddressBook.user_id == 111).first()

        record_id = query.id
        user_id = 111
        result = get_record_user(record_id, user_id, self.session)

        self.assertEqual(record_1, result, "не працює test_get_record_user //1")

        record_id = query.id
        user_id = 2
        result_2 = get_record_user(record_id, user_id, self.session)

        self.assertIsNone(result_2, "не працює test_get_record_user //2")
        
        record_id = 111
        user_id = 111
        result_3 = get_record_user(record_id, user_id, self.session)

        self.assertIsNone(result_3, "не працює test_get_record_user //3")

    def test_create_record(self):

        first_name = "first_name"
        last_name = "last_name"
        phone = "1234567890"
        email = "test@test.com"
        address = "Kyiv, street, building, flat"
        birthday = "1986-04-26"
        black_list = "True"
        user_id = 222

        create_record(
                        first_name=first_name,
                        phone=phone,
                        user_id=user_id,
                        last_name=last_name,
                        email=email,
                        address=address,
                        black_list=black_list,
                        birthday=birthday,
                        session_=self.session
                        )
        
        query = self.session.query(AddressBook).filter(AddressBook.first_name == first_name).first()

        self.assertTrue(query, "не працює test_create_record")

    #@unittest.skip(" ")
    def test_update_record(self):
        first_name = "first_3"
        last_name = "last_3"
        phone = "55555555555"
        email = "test3@test.com"
        address = "Kyiv, street, building, flat"
        birthday_str = "1986-04-26"
        birthday = datetime.strptime(birthday_str, '%Y-%m-%d')
        black_list = True
        user_id = 333

        record_3 = AddressBook(                        
                        first_name=first_name,
                        last_name=last_name,
                        phone=phone,
                        email=email,
                        address=address,
                        birthday=birthday,
                        black_list=black_list,
                        user_id=user_id
                        )

        self.session.add(record_3)
        self.session.commit()
        self.session.refresh(record_3)

        query = self.session.query(AddressBook).filter(AddressBook.user_id == 333).first()
        record_id = query.id

        update_record(
                        record_id= record_id ,first_name="test", last_name="test", phone="5555555555", email="test5@test.com",
                        address="test", birthday="1999-12-31", black_list="False", user_id=333, session_=self.session
                    )
        query = self.session.query(AddressBook).filter(AddressBook.first_name == "test").first()

        self.assertEqual(query.first_name, "test", "не працює test_update_record неправильний атрибут first_name")
        self.assertEqual(query.last_name, "test", "не працює test_update_record неправильний атрибут last_name")
        self.assertEqual(query.phone, "5555555555", "не працює test_update_record неправильний атрибут phone")
        self.assertEqual(query.email, "test5@test.com", "не працює test_update_record неправильний атрибут email")
        self.assertEqual(query.address, "test", "не працює test_update_record неправильний атрибут address")
        birthday_test = datetime.strptime("1999-12-31", '%Y-%m-%d').date()
        self.assertEqual(query.birthday, birthday_test, "не працює test_update_record неправильний атрибут birthday")
        self.assertEqual(query.black_list, False, "не працює test_update_record неправильний атрибут black_list")



  
# py -m unittest discover src/tests
