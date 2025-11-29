"""
Основной класс книжного магазина
"""

from typing import List, Dict
from models import Book, Employee, Customer, Sale
from exceptions import *
from file_operations import FileOperations


class Bookstore:
    """Основной класс книжного магазина"""

    def __init__(self, name: str):
        self.name = name
        self.books: Dict[int, Book] = {}
        self.employees: Dict[int, Employee] = {}
        self.customers: Dict[int, Customer] = {}
        self.sales: Dict[int, Sale] = {}
        self._next_book_id = 1
        self._next_emp_id = 1
        self._next_cust_id = 1
        self._next_sale_id = 1
        self.file_ops = FileOperations()

    def _get_next_book_id(self) -> int:
        """Получить следующий доступный ID для книги"""
        if self.books:
            max_id = max(self.books.keys())
            return max_id + 1
        return 1

    def _get_next_emp_id(self) -> int:
        """Получить следующий доступный ID для сотрудника"""
        if self.employees:
            max_id = max(self.employees.keys())
            return max_id + 1
        return 1

    def _get_next_cust_id(self) -> int:
        """Получить следующий доступный ID для клиента"""
        if self.customers:
            max_id = max(self.customers.keys())
            return max_id + 1
        return 1

    def add_book(self, book: Book) -> None:
        """Добавление книги в магазин"""
        try:
            if book.book_id <= 0:
                book.book_id = self._get_next_book_id()

            if book.book_id in self.books:
                self.books[book.book_id].quantity += book.quantity
                print(
                    f"Количество книги '{book.title}' увеличено. Теперь в наличии: {self.books[book.book_id].quantity}")
            else:
                self.books[book.book_id] = book
                if book.book_id >= self._next_book_id:
                    self._next_book_id = book.book_id + 1
                print(f"Книга '{book.title}' успешно добавлена с ID: {book.book_id}")
        except Exception as e:
            raise BookstoreError(f"Ошибка при добавлении книги: {e}")

    def remove_book(self, book_id: int, quantity: int = 1) -> None:
        """Удаление книги из магазина"""
        try:
            if book_id not in self.books:
                raise BookNotFoundError(f"Книга с ID {book_id} не найдена")

            book = self.books[book_id]
            if book.quantity < quantity:
                raise InsufficientQuantityError(
                    f"Недостаточно книг. В наличии: {book.quantity}, запрошено: {quantity}"
                )

            book.quantity -= quantity
            if book.quantity == 0:
                del self.books[book_id]
                print(f"Книга '{book.title}' полностью удалена из магазина")
            else:
                print(f"Удалено {quantity} экз. книги '{book.title}'. Осталось: {book.quantity}")

        except (BookNotFoundError, InsufficientQuantityError):
            raise
        except Exception as e:
            raise BookstoreError(f"Ошибка при удалении книги: {e}")

    def sell_book(self, book_id: int, quantity: int, customer_id: int, employee_id: int) -> Sale:
        """Продажа книги клиенту"""
        try:
            if book_id not in self.books:
                raise BookNotFoundError(f"Книга с ID {book_id} не найдена")

            if customer_id not in self.customers:
                raise CustomerNotFoundError(f"Клиент с ID {customer_id} не найден")

            if employee_id not in self.employees:
                raise EmployeeNotFoundError(f"Сотрудник с ID {employee_id} не найден")

            book = self.books[book_id]
            if book.quantity < quantity:
                raise InsufficientQuantityError(
                    f"Недостаточно книг для продажи. В наличии: {book.quantity}"
                )

            total_price = book.price * quantity
            book.quantity -= quantity

            sale = Sale(
                sale_id=self._next_sale_id,
                book_id=book_id,
                customer_id=customer_id,
                employee_id=employee_id,
                quantity=quantity,
                total_price=total_price
            )

            self.sales[self._next_sale_id] = sale
            self._next_sale_id += 1

            customer = self.customers[customer_id]
            employee = self.employees[employee_id]

            print(f"Продажа успешно завершена: {quantity} экз. '{book.title}' "
                  f"клиенту {customer.name} за {total_price} руб. "
                  f"(Продавец: {employee.name})")

            return sale

        except (BookNotFoundError, CustomerNotFoundError, EmployeeNotFoundError, InsufficientQuantityError):
            raise
        except Exception as e:
            raise BookstoreError(f"Ошибка при продаже книги: {e}")

    def add_employee(self, employee: Employee) -> None:
        """Добавление сотрудника"""
        try:
            if employee.emp_id <= 0:
                employee.emp_id = self._get_next_emp_id()

            if employee.emp_id in self.employees:
                print(f"Сотрудник с ID {employee.emp_id} уже существует")
                return

            self.employees[employee.emp_id] = employee
            if employee.emp_id >= self._next_emp_id:
                self._next_emp_id = employee.emp_id + 1
            print(f"Сотрудник {employee.name} успешно добавлен с ID: {employee.emp_id}")

        except Exception as e:
            raise BookstoreError(f"Ошибка при добавлении сотрудника: {e}")

    def add_customer(self, customer: Customer) -> None:
        """Добавление клиента"""
        try:
            if customer.cust_id <= 0:
                customer.cust_id = self._get_next_cust_id()

            if customer.cust_id in self.customers:
                print(f"Клиент с ID {customer.cust_id} уже существует")
                return

            self.customers[customer.cust_id] = customer
            if customer.cust_id >= self._next_cust_id:
                self._next_cust_id = customer.cust_id + 1
            print(f"Клиент {customer.name} успешно добавлен с ID: {customer.cust_id}")

        except Exception as e:
            raise BookstoreError(f"Ошибка при добавлении клиента: {e}")

    def search_books(self, **kwargs) -> List[Book]:
        """Поиск книг по различным критериям"""
        try:
            results = list(self.books.values())

            if 'title' in kwargs and kwargs['title']:
                results = [b for b in results if kwargs['title'].lower() in b.title.lower()]
            if 'author' in kwargs and kwargs['author']:
                results = [b for b in results if kwargs['author'].lower() in b.author.lower()]
            if 'genre' in kwargs and kwargs['genre']:
                results = [b for b in results if kwargs['genre'].lower() in b.genre.lower()]
            if 'max_price' in kwargs and kwargs['max_price']:
                results = [b for b in results if b.price <= kwargs['max_price']]

            return results

        except Exception as e:
            raise BookstoreError(f"Ошибка при поиске книг: {e}")

    def get_sales_by_customer(self, customer_id: int) -> List[Sale]:
        """Получение всех продаж для конкретного клиента"""
        try:
            return [sale for sale in self.sales.values() if sale.customer_id == customer_id]
        except Exception as e:
            raise BookstoreError(f"Ошибка при получении продаж клиента: {e}")

    def get_sales_by_employee(self, employee_id: int) -> List[Sale]:
        """Получение всех продаж для конкретного сотрудника"""
        try:
            return [sale for sale in self.sales.values() if sale.employee_id == employee_id]
        except Exception as e:
            raise BookstoreError(f"Ошибка при получении продаж сотрудника: {e}")

    def get_total_revenue(self) -> float:
        """Получение общей выручки магазина"""
        try:
            return sum(sale.total_price for sale in self.sales.values())
        except Exception as e:
            raise BookstoreError(f"Ошибка при расчете выручки: {e}")

    def get_inventory_value(self) -> float:
        """Получение общей стоимости инвентаря"""
        try:
            return sum(book.price * book.quantity for book in self.books.values())
        except Exception as e:
            raise BookstoreError(f"Ошибка при расчете стоимости инвентаря: {e}")

    def save_to_json(self, filename: str) -> None:
        """Сохранение данных в JSON файл"""
        self.file_ops.save_to_json(self, filename)

    def load_from_json(self, filename: str) -> None:
        """Загрузка данных из JSON файла"""
        self.file_ops.load_from_json(self, filename)

    def save_to_xml(self, filename: str) -> None:
        """Сохранение данных в XML файл"""
        self.file_ops.save_to_xml(self, filename)

    def load_from_xml(self, filename: str) -> None:
        """Загрузка данных из XML файла"""
        self.file_ops.load_from_xml(self, filename)

    def display_info(self) -> None:
        """Отображение информации о магазине"""
        print(f"\n=== {self.name} ===")
        print(f"Книг в ассортименте: {len(self.books)}")
        print(f"Сотрудников: {len(self.employees)}")
        print(f"Клиентов: {len(self.customers)}")
        print(f"Всего продаж: {len(self.sales)}")
        print(f"Общая стоимость инвентаря: {self.get_inventory_value():.2f} руб.")
        print(f"Общая выручка: {self.get_total_revenue():.2f} руб.")
