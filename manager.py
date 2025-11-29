"""
Менеджер для интерактивного управления книжным магазином
"""

from bookstore import Bookstore
from models import Book, Employee, Customer
from exceptions import *


class BookstoreManager:
    """Менеджер для управления книжным магазином с обработкой исключений"""

    def __init__(self, bookstore: Bookstore):
        self.bookstore = bookstore

    def safe_execute(self, operation, *args, **kwargs):
        """Безопасное выполнение операций с обработкой исключений"""
        try:
            return operation(*args, **kwargs)
        except BookstoreError as e:
            print(f"Ошибка в работе магазина: {e}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return None

    def _get_float_input(self, prompt: str) -> float:
        """Безопасный ввод числа с плавающей точкой"""
        while True:
            try:
                value = input(prompt).strip()
                return float(value)
            except ValueError:
                print("Ошибка: введите число (например: 100.50)")

    def _get_int_input(self, prompt: str) -> int:
        """Безопасный ввод целого числа"""
        while True:
            try:
                value = input(prompt).strip()
                return int(value)
            except ValueError:
                print("Ошибка: введите целое число (например: 5)")

    def interactive_mode(self):
        """Интерактивный режим работы с магазином"""
        print(f"Добро пожаловать в систему управления '{self.bookstore.name}'!")

        while True:
            print("\n" + "=" * 50)
            print("Меню:")
            print("1. Показать все книги")
            print("2. Найти книгу")
            print("3. Добавить книгу")
            print("4. Удалить книгу")
            print("5. Продать книгу")
            print("6. Показать клиентов")
            print("7. Добавить клиента")
            print("8. Показать сотрудников")
            print("9. Добавить сотрудника")
            print("10. Показать продажи")
            print("11. Сохранить данные (JSON)")
            print("12. Сохранить данные (XML)")
            print("13. Загрузить данные (JSON)")
            print("14. Загрузить данные (XML)")
            print("15. Информация о магазине")
            print("0. Выход")

            choice = input("Выберите действие: ").strip()

            if choice == '1':
                self._show_books()
            elif choice == '2':
                self._search_books_interactive()
            elif choice == '3':
                self._add_book_interactive()
            elif choice == '4':
                self._remove_book_interactive()
            elif choice == '5':
                self._sell_book_interactive()
            elif choice == '6':
                self._show_customers()
            elif choice == '7':
                self._add_customer_interactive()
            elif choice == '8':
                self._show_employees()
            elif choice == '9':
                self._add_employee_interactive()
            elif choice == '10':
                self._show_sales()
            elif choice == '11':
                self._save_json_interactive()
            elif choice == '12':
                self._save_xml_interactive()
            elif choice == '13':
                self._load_json_interactive()
            elif choice == '14':
                self._load_xml_interactive()
            elif choice == '15':
                self.safe_execute(self.bookstore.display_info)
            elif choice == '0':
                print("До свидания!")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

    def _show_books(self):
        """Показать все книги"""
        if not self.bookstore.books:
            print("В магазине нет книг")
            return

        print("\nКниги в магазине:")
        for book in self.bookstore.books.values():
            print(f"  {book}")

    def _show_customers(self):
        """Показать всех клиентов"""
        if not self.bookstore.customers:
            print("В базе нет клиентов")
            return

        print("\nКлиенты магазина:")
        for customer in self.bookstore.customers.values():
            print(f"  {customer}")

    def _show_employees(self):
        """Показать всех сотрудников"""
        if not self.bookstore.employees:
            print("В базе нет сотрудников")
            return

        print("\nСотрудники магазина:")
        for employee in self.bookstore.employees.values():
            print(f"  {employee}")

    def _show_sales(self):
        """Показать все продажи"""
        if not self.bookstore.sales:
            print("Продаж пока не было")
            return

        print("\nИстория продаж:")
        total_revenue = 0
        for sale in self.bookstore.sales.values():
            print(f"  {sale}")
            total_revenue += sale.total_price

        print(f"\nОбщая выручка: {total_revenue:.2f} руб.")

    def _add_book_interactive(self):
        """Интерактивное добавление книги"""
        try:
            print("\nДобавление новой книги:")
            title = input("Название: ").strip()
            if not title:
                print("Ошибка: название не может быть пустым")
                return

            author = input("Автор: ").strip()
            if not author:
                print("Ошибка: автор не может быть пустым")
                return

            genre = input("Жанр: ").strip()
            if not genre:
                print("Ошибка: жанр не может быть пустым")
                return

            price = self._get_float_input("Цена: ")
            quantity = self._get_int_input("Количество: ")
            year = self._get_int_input("Год издания: ")

            book = Book(0, title, author, genre, price, quantity, year)
            self.safe_execute(self.bookstore.add_book, book)

        except Exception as e:
            print(f"Ошибка: {e}")

    def _remove_book_interactive(self):
        """Интерактивное удаление книги"""
        try:
            if not self.bookstore.books:
                print("В магазине нет книг")
                return

            print("\nУдаление книги:")
            self._show_books()

            book_id = self._get_int_input("\nID книги для удаления: ")
            quantity = self._get_int_input("Количество для удаления: ")

            self.safe_execute(self.bookstore.remove_book, book_id, quantity)

        except Exception as e:
            print(f"Ошибка: {e}")

    def _search_books_interactive(self):
        """Интерактивный поиск книг"""
        print("\nПоиск книг:")
        print("Введите критерии поиска (оставьте пустым для пропуска)")

        title = input("Название: ").strip() or None
        author = input("Автор: ").strip() or None
        genre = input("Жанр: ").strip() or None

        max_price = None
        max_price_input = input("Максимальная цена: ").strip()
        if max_price_input:
            try:
                max_price = float(max_price_input)
                if max_price <= 0:
                    print("Цена должна быть положительной. Этот критерий будет проигнорирован.")
                    max_price = None
            except ValueError:
                print("Неверный формат цены. Этот критерий будет проигнорирован.")
                max_price = None

        criteria = {}
        if title:
            criteria['title'] = title
        if author:
            criteria['author'] = author
        if genre:
            criteria['genre'] = genre
        if max_price:
            criteria['max_price'] = max_price

        results = self.safe_execute(self.bookstore.search_books, **criteria)

        if results:
            print(f"\nНайдено {len(results)} книг:")
            for book in results:
                print(f"  {book}")
        else:
            print("Книги по заданным критериям не найдены")

    def _sell_book_interactive(self):
        """Интерактивная продажа книги"""
        try:
            print("\nПродажа книги:")

            if not self.bookstore.books:
                print("В магазине нет книг для продажи")
                return

            print("\nДоступные книги:")
            self._show_books()

            if not self.bookstore.customers:
                print("В базе нет клиентов. Сначала добавьте клиента.")
                return

            print("\nДоступные клиенты:")
            self._show_customers()

            if not self.bookstore.employees:
                print("В базе нет сотрудников. Сначала добавьте сотрудника.")
                return

            print("\nДоступные сотрудники:")
            self._show_employees()

            book_id = self._get_int_input("\nID книги для продажи: ")
            quantity = self._get_int_input("Количество: ")
            customer_id = self._get_int_input("ID клиента: ")
            employee_id = self._get_int_input("ID сотрудника: ")

            sale = self.safe_execute(self.bookstore.sell_book, book_id, quantity, customer_id, employee_id)
            if sale is not None:
                print(f"Продажа #{sale.sale_id} завершена!")

        except Exception as e:
            print(f"Ошибка: {e}")

    def _add_employee_interactive(self):
        """Интерактивное добавление сотрудника"""
        try:
            print("\nДобавление сотрудника:")
            name = input("Имя: ").strip()
            if not name:
                print("Ошибка: имя не может быть пустым")
                return

            position = input("Должность: ").strip()
            if not position:
                print("Ошибка: должность не может быть пустой")
                return

            salary = self._get_float_input("Зарплата: ")

            employee = Employee(0, name, position, salary)
            self.safe_execute(self.bookstore.add_employee, employee)

        except Exception as e:
            print(f"Ошибка: {e}")

    def _add_customer_interactive(self):
        """Интерактивное добавление клиента"""
        try:
            print("\nДобавление клиента:")
            name = input("Имя: ").strip()
            if not name:
                print("Ошибка: имя не может быть пустым")
                return

            email = input("Email: ").strip()
            if not email or '@' not in email:
                print("Ошибка: введите корректный email")
                return

            phone = input("Телефон: ").strip()
            if not phone:
                print("Ошибка: телефон не может быть пустым")
                return

            customer = Customer(0, name, email, phone)
            self.safe_execute(self.bookstore.add_customer, customer)

        except Exception as e:
            print(f"Ошибка: {e}")

    def _save_json_interactive(self):
        """Интерактивное сохранение данных в JSON"""
        filename = input("Имя файла для сохранения (JSON): ").strip()

        if not filename:
            print("Имя файла не может быть пустым")
            return

        if not filename.endswith('.json'):
            filename += '.json'

        self.safe_execute(self.bookstore.save_to_json, filename)

    def _save_xml_interactive(self):
        """Интерактивное сохранение данных в XML"""
        filename = input("Имя файла для сохранения (XML): ").strip()

        if not filename:
            print("Имя файла не может быть пустым")
            return

        if not filename.endswith('.xml'):
            filename += '.xml'

        self.safe_execute(self.bookstore.save_to_xml, filename)

    def _load_json_interactive(self):
        """Интерактивная загрузка данных из JSON"""
        filename = input("Имя файла для загрузки (JSON): ").strip()

        if not filename:
            print("Имя файла не может быть пустым")
            return

        if not filename.endswith('.json'):
            filename += '.json'

        self.safe_execute(self.bookstore.load_from_json, filename)

    def _load_xml_interactive(self):
        """Интерактивная загрузка данных из XML"""
        filename = input("Имя файла для загрузки (XML): ").strip()

        if not filename:
            print("Имя файла не может быть пустым")
            return

        if not filename.endswith('.xml'):
            filename += '.xml'

        self.safe_execute(self.bookstore.load_from_xml, filename)
