from datetime import datetime

from sqlalchemy import and_

from src import db
from src import models


def get_record_user(record_id, user_id):
    return db.session.query(models.AddressBook).filter(
        and_(models.AddressBook.user_id == user_id, models.AddressBook.id == record_id)).first()


def create_record(first_name, phone, user_id, last_name, email, address, black_list, birthday):

    if not birthday:
        birthday = "1900-01-01"
    birthday = datetime.strptime(birthday, '%Y-%m-%d')
    if black_list == "True":
        black_list = True
    else:
        black_list = False

    record = models.AddressBook(first_name=first_name, last_name=last_name, phone=phone, email=email, address=address, birthday=birthday, black_list=black_list, user_id=user_id)
    db.session.add(record)
    db.session.commit()


def update_record(record_id, first_name, phone, user_id, last_name, email, address, black_list, birthday):
    record = get_record_user(record_id, user_id)

    if black_list == "True":
        black_list = True
    else:
        black_list = False

    if first_name:
        record.first_name = first_name
    if last_name:
        record.last_name = last_name
    if phone:
        record.phone = phone
    if email:
        record.email = email
    if address:
        record.address = address
    if birthday:
        birthday = datetime.strptime(birthday, '%Y-%m-%d')
        record.birthday = birthday
    record.black_list = black_list

    db.session.commit()


def delete_record(record_id, user_id):
    criterion = db.session.query(models.AddressBook).filter(
        and_(models.AddressBook.user_id == user_id, models.AddressBook.id == record_id)).first()

    if not criterion:
        return False

    db.session.query(models.AddressBook).filter(
        and_(models.AddressBook.user_id == user_id, models.AddressBook.id == record_id)).delete()
    db.session.commit()

    return True


def show_record(record_id, user_id):
    criterion = db.session.query(models.AddressBook).filter(
        and_(models.AddressBook.user_id == user_id, models.AddressBook.id == record_id)).first()

    if not criterion:
        return False
    
    return criterion


def show_all_records(user_id):
    criterion = db.session.query(models.AddressBook).filter(
        and_(models.AddressBook.user_id == user_id)).all()

    if not criterion:
        return False
    
    return criterion


def how_many_days_to_birthday(record_id, user_id):
    person = db.session.query(models.AddressBook).filter(
        and_(models.AddressBook.user_id == user_id, models.AddressBook.id == record_id)).first()

    if not person:
        return "The user does not have such an entry in the address book"

    current_date, current_year, next_year = _current_date_and_year()

    if person.birthday.strftime('%Y-%m-%d') == "1900-01-01":
        return "The user does not have such an entry in the address book"

    birthday = person.birthday
    birthday = birthday.replace(year=current_year)

    if birthday < current_date:
        result = (birthday.replace(year=next_year) - current_date).days
    elif birthday > current_date:
        result = (birthday - current_date).days
    else:
        return f"Today {person.first_name}'s birthday!!!"
    return f" There are {result} days left until {person.first_name}'s birthday"


def _current_date_and_year():
    """Returns the current date, the current year, and the next year"""
    current_date = datetime.now().date()
    current_year = current_date.year
    next_year = current_year + 1
    return current_date, current_year, next_year