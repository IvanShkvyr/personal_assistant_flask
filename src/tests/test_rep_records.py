from datetime import datetime, timedelta

from src.models import AddressBook
from src.repository.records import get_record_user, create_record, update_record, delete_record, show_record, show_all_records, how_many_days_to_birthday
from src.tests.create_test_db import DbTestCase


class TestRepositoryRecords(DbTestCase):
    """
    Test the records collection database
    """
    def _create_addressbooks_record(self, first_name, user_id, last_name=None, phone=None, email=None, address=None, birthday=None, black_list=None):
        record = AddressBook(                        
                            first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            address=address,
                            birthday=birthday,
                            black_list=black_list,
                            user_id=user_id
                            )
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        query = self.session.query(AddressBook).filter(AddressBook.user_id == user_id).first()
        return query

    def test_get_record_user(self):
        record_1 = AddressBook(first_name="first_1", user_id=111)
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
        create_record(
                        first_name=first_name,
                        last_name="last_name",
                        phone="1234567890",
                        email="test@test.com",
                        address="Kyiv, street, building, flat",
                        birthday="1986-04-26",
                        black_list="True",
                        user_id=222,
                        session_=self.session
                        )
        query = self.session.query(AddressBook).filter(AddressBook.first_name == first_name).first()
        self.assertTrue(query, "не працює test_create_record")

    def test_update_record(self):
        birthday_str = "1986-04-26"
        birthday = datetime.strptime(birthday_str, '%Y-%m-%d')
        query = self._create_addressbooks_record(
                                                    first_name="first_3",
                                                    last_name="last_3",
                                                    phone="55555555555",
                                                    email="test3@test.com",
                                                    address="Kyiv, street, building, flat",
                                                    birthday=birthday,
                                                    black_list=True,
                                                    user_id=333
                                                )

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

    def test_delete_record_if_good_id(self):
        user_id = 444
        query = self._create_addressbooks_record(first_name="first_4", user_id=user_id)
        record_4_id = query.id
        test_delete = delete_record(record_4_id, user_id, self.session)
        self.assertTrue(test_delete, "не працює test_delete_record_if_good_id")

    def test_delete_record_if_bad_id(self):
        query = self._create_addressbooks_record(first_name="first_5", user_id=555)
        record_5_id = query.id
        test_delete = delete_record(record_5_id, 101, self.session)
        self.assertFalse(test_delete, "не працює test_delete_record_if_bad_id")

    def test_show_record_if_good_id(self):
        user_id = 66
        query = self._create_addressbooks_record(first_name="first_6", user_id=user_id)
        record_6_id = query.id
        test_show_record = show_record(record_6_id, user_id, self.session)
        self.assertTrue(test_show_record, "не працює test_show_record_if_good_id")

    def test_show_record_if_bad_id(self):
        query = self._create_addressbooks_record(first_name="first_7", user_id=777)
        record_7_id = query.id
        test_show_record = show_record(record_7_id, 102, self.session)
        self.assertFalse(test_show_record, "не працює test_show_record_if_bad_id")

    def test_show_all_records_if_good_id(self):
        user_id = 888
        query = self._create_addressbooks_record(first_name="first_8", user_id=user_id)
        test_show_record = show_all_records(user_id, self.session)
        self.assertTrue(test_show_record, "не працює test_show_all_records_if_good_id")

    def test_show_all_records_if_bad_id(self):
        query = self._create_addressbooks_record(first_name="first_8", user_id=999)
        test_show_record = show_all_records(103, self.session)
        self.assertFalse(test_show_record, "не працює test_show_all_records_if_bad_id")

    def test_how_many_days_to_birthday_if_good_id_is_date(self):
        birthday = datetime.now() + timedelta(days=10)
        user_id = 1010
        query = self._create_addressbooks_record(first_name="first_1010", birthday=birthday, user_id=user_id)
        record_10_id = query.id
        result_10 = how_many_days_to_birthday(record_10_id, user_id, self.session)
        self.assertEqual(result_10,
                        " There are 10 days left until first_1010's birthday",
                        "не працює test_how_many_days_to_birthday_if_good_id_is_date")

    def test_how_many_days_to_birthday_if_good_id_is_date_today(self):
        birthday = datetime.now()
        user_id = 1111
        query = self._create_addressbooks_record(first_name="first_1111", birthday=birthday, user_id=user_id)
        record_11_id = query.id
        result_11 = how_many_days_to_birthday(record_11_id, user_id, self.session)
        self.assertEqual(result_11,
                         "Today first_1111's birthday!!!",
                         "не працює test_how_many_days_to_birthday_if_good_id_is_date")

    def test_how_many_days_to_birthday_if_good_id_no_date(self):
        birthday = datetime.strptime("1900-01-01", '%Y-%m-%d')
        user_id = 1212
        query = self._create_addressbooks_record(first_name="first_1212", birthday=birthday, user_id=user_id)
        record_12_id = query.id
        result_12 = how_many_days_to_birthday(record_12_id, user_id, self.session)
        self.assertEqual(result_12,
                        "The user does not have such an entry in the address book",
                        "не працює test_how_many_days_to_birthday_if_good_id_is_date")

    def test_how_many_days_to_birthday_if_good_id_no_date(self):
        record_13_id = 1
        user_id = 1313
        result_13 = how_many_days_to_birthday(record_13_id, user_id, self.session)
        self.assertEqual(result_13,
                        "The user does not have such an entry in the address book",
                        "не працює test_how_many_days_to_birthday_if_good_id_is_date")
          

# py -m unittest discover src/tests
