"""
Основные классы предметной области
"""

from datetime import datetime
from typing import List, Dict
from exceptions import *


class Book:
    """Класс для представления книги"""

    def __init__(self, book_id: int, title: str, author: str, genre: str,
                 price: float, quantity: int, year: int):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.price = price
        self.quantity = quantity
        self.year = year

        self._validate_data()

    def _validate_data(self):
        """Валидация данных книги"""
        if self.book_id < 0:
            raise ValueError("ID книги не может быть отрицательным")
        if not self.title:
            raise ValueError("Название книги не может быть пустым")
        if not self.author:
            raise ValueError("Автор не может быть пустым")
        if not self.genre:
            raise ValueError("Жанр не может быть пустым")
        if self.price <= 0:
            raise InvalidPriceError("Цена должна быть положительной")
        if self.quantity < 0:
            raise ValueError("Количество не может быть отрицательным")
        if self.year < 1000 or self.year > datetime.now().year:
            raise ValueError("Неверный год издания")

    def to_dict(self) -> Dict:
        """Преобразование книги в словарь"""
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'price': self.price,
            'quantity': self.quantity,
            'year': self.year
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Book':
        """Создание книги из словаря"""
        return cls(
            book_id=data['book_id'],
            title=data['title'],
            author=data['author'],
            genre=data['genre'],
            price=data['price'],
            quantity=data['quantity'],
            year=data['year']
        )

    def __str__(self):
        return f"ID: {self.book_id} | '{self.title}' - {self.author} | Жанр: {self.genre} | {self.price} руб. | В наличии: {self.quantity} | Год: {self.year}"


class Employee:
    """Класс для представления сотрудника"""

    def __init__(self, emp_id: int, name: str, position: str, salary: float):
        self.emp_id = emp_id
        self.name = name
        self.position = position
        self.salary = salary

        self._validate_data()

    def _validate_data(self):
        """Валидация данных сотрудника"""
        if self.emp_id < 0:
            raise ValueError("ID сотрудника не может быть отрицательным")
        if not self.name:
            raise ValueError("Имя сотрудника не может быть пустым")
        if not self.position:
            raise ValueError("Должность не может быть пустой")
        if self.salary < 0:
            raise ValueError("Зарплата не может быть отрицательной")

    def to_dict(self) -> Dict:
        """Преобразование сотрудника в словарь"""
        return {
            'emp_id': self.emp_id,
            'name': self.name,
            'position': self.position,
            'salary': self.salary
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Employee':
        """Создание сотрудника из словаря"""
        return cls(
            emp_id=data['emp_id'],
            name=data['name'],
            position=data['position'],
            salary=data['salary']
        )

    def __str__(self):
        return f"ID: {self.emp_id} | {self.name} - {self.position} | Зарплата: {self.salary} руб."


class Customer:
    """Класс для представления клиента"""

    def __init__(self, cust_id: int, name: str, email: str, phone: str):
        self.cust_id = cust_id
        self.name = name
        self.email = email
        self.phone = phone

        self._validate_data()

    def _validate_data(self):
        """Валидация данных клиента"""
        if self.cust_id < 0:
            raise ValueError("ID клиента не может быть отрицательным")
        if not self.name:
            raise ValueError("Имя клиента не может быть пустым")
        if '@' not in self.email:
            raise ValueError("Неверный формат email")
        if not self.phone:
            raise ValueError("Телефон не может быть пустым")

    def to_dict(self) -> Dict:
        """Преобразование клиента в словарь"""
        return {
            'cust_id': self.cust_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Customer':
        """Создание клиента из словаря"""
        return cls(
            cust_id=data['cust_id'],
            name=data['name'],
            email=data['email'],
            phone=data['phone']
        )

    def __str__(self):
        return f"ID: {self.cust_id} | {self.name} | {self.email} | {self.phone}"


class Sale:
    """Класс для представления продажи"""

    def __init__(self, sale_id: int, book_id: int, customer_id: int,
                 employee_id: int, quantity: int, total_price: float,
                 sale_date: datetime = None):
        self.sale_id = sale_id
        self.book_id = book_id
        self.customer_id = customer_id
        self.employee_id = employee_id
        self.quantity = quantity
        self.total_price = total_price
        self.sale_date = sale_date or datetime.now()

        self._validate_data()

    def _validate_data(self):
        """Валидация данных продажи"""
        if self.sale_id <= 0:
            raise ValueError("ID продажи должен быть положительным")
        if self.book_id <= 0:
            raise ValueError("ID книги должен быть положительным")
        if self.customer_id <= 0:
            raise ValueError("ID клиента должен быть положительным")
        if self.employee_id <= 0:
            raise ValueError("ID сотрудника должен быть положительным")
        if self.quantity <= 0:
            raise ValueError("Количество должно быть положительным")
        if self.total_price <= 0:
            raise ValueError("Общая цена должна быть положительной")

    def to_dict(self) -> Dict:
        """Преобразование продажи в словарь"""
        return {
            'sale_id': self.sale_id,
            'book_id': self.book_id,
            'customer_id': self.customer_id,
            'employee_id': self.employee_id,
            'quantity': self.quantity,
            'total_price': self.total_price,
            'sale_date': self.sale_date.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Sale':
        """Создание продажи из словаря"""
        return cls(
            sale_id=data['sale_id'],
            book_id=data['book_id'],
            customer_id=data['customer_id'],
            employee_id=data['employee_id'],
            quantity=data['quantity'],
            total_price=data['total_price'],
            sale_date=datetime.fromisoformat(data['sale_date'])
        )

    def __str__(self):
        return (f"ID продажи: {self.sale_id} | Книга ID: {self.book_id} | "
                f"Клиент ID: {self.customer_id} | Сотрудник ID: {self.employee_id} | "
                f"{self.quantity} шт. | {self.total_price} руб. | "
                f"{self.sale_date.strftime('%d.%m.%Y %H:%M')}")
