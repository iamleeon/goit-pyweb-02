from collections import UserDict
from datetime import datetime, date, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if not self.phone_validation(value):
            raise ValueError("Invalid phone format")

    def phone_validation(self, phone):
        try:
            if len(phone) == 10 and int(phone):
                return phone
        except ValueError:
            return None


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y").date()
            if birthday > datetime.today().date():
                raise Exception("Invalid date. Date can't be in future.")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        phone = Phone(phone)
        self.phones.append(phone)

    def remove_phone(self, phone_to_remove):
        self.phones = [phone for phone in self.phones if phone.value != phone_to_remove]

    def edit_phone(self, old_phone, new_phone):
        new_phone = Phone(new_phone)
        self.phones = [new_phone if phone.value == old_phone else phone for phone in self.phones]

    def find_phone(self, phone):
        for p in self.phones:
            if phone == str(p):
                return p

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return (f"Contact name: {self.name.value}. Phones: {'; '.join(p.value for p in self.phones)}. "
                f"Birthday: {self.birthday}.")


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name):
        del self.data[name]

    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = ""
        today = date.today()
        try:
            for user in self.data.values():
                if user.birthday is None:
                    continue
                else:
                    birthday_this_year = datetime.strptime(str(user.birthday), "%d.%m.%Y").replace(year=today.year).date()
                    days_counter = (birthday_this_year - today).days
                    if 0 <= days_counter <= days:
                        if birthday_this_year.weekday() >= 5:
                            days_ahead = 0 - birthday_this_year.weekday()
                            days_ahead += 7
                            birthday_this_year = birthday_this_year + timedelta(days=days_ahead)
                        birthday_this_year = datetime.strftime(birthday_this_year, "%d.%m.%Y")
                        upcoming_birthdays += (f"Contact name: {user.name}. "
                                               f"Birthday: {user.birthday}. "
                                               f"Congratulation date: {birthday_this_year}.\n")
            return upcoming_birthdays
        except ValueError:
            return None
