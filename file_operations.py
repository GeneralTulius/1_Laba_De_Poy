"""
Операции с файлами JSON и XML
"""

import json
import xml.etree.ElementTree as ET
from models import Book, Employee, Customer, Sale
from exceptions import FileOperationError


class FileOperations:
    """Класс для операций с файлами JSON и XML"""

    @staticmethod
    def save_to_json(bookstore, filename: str) -> None:
        """Сохранение данных в JSON файл"""
        try:
            data = {
                'name': bookstore.name,
                'next_book_id': bookstore._next_book_id,
                'next_emp_id': bookstore._next_emp_id,
                'next_cust_id': bookstore._next_cust_id,
                'next_sale_id': bookstore._next_sale_id,
                'books': [book.to_dict() for book in bookstore.books.values()],
                'employees': [emp.to_dict() for emp in bookstore.employees.values()],
                'customers': [cust.to_dict() for cust in bookstore.customers.values()],
                'sales': [sale.to_dict() for sale in bookstore.sales.values()]
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"Данные успешно сохранены в {filename}")

        except Exception as e:
            raise FileOperationError(f"Ошибка при сохранении в JSON: {e}")

    @staticmethod
    def load_from_json(bookstore, filename: str) -> None:
        """Загрузка данных из JSON файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

            bookstore.name = data['name']

            bookstore.books.clear()
            bookstore.employees.clear()
            bookstore.customers.clear()
            bookstore.sales.clear()

            bookstore._next_book_id = data.get('next_book_id', 1)
            bookstore._next_emp_id = data.get('next_emp_id', 1)
            bookstore._next_cust_id = data.get('next_cust_id', 1)
            bookstore._next_sale_id = data.get('next_sale_id', 1)

            for book_data in data['books']:
                book = Book.from_dict(book_data)
                bookstore.books[book.book_id] = book

            for emp_data in data['employees']:
                employee = Employee.from_dict(emp_data)
                bookstore.employees[employee.emp_id] = employee

            for cust_data in data['customers']:
                customer = Customer.from_dict(cust_data)
                bookstore.customers[customer.cust_id] = customer

            for sale_data in data.get('sales', []):
                sale = Sale.from_dict(sale_data)
                bookstore.sales[sale.sale_id] = sale

            print(f"Данные успешно загружены из {filename}")

        except FileNotFoundError:
            raise FileOperationError(f"Файл {filename} не найден")
        except Exception as e:
            raise FileOperationError(f"Ошибка при загрузке из JSON: {e}")

    @staticmethod
    def save_to_xml(bookstore, filename: str) -> None:
        """Сохранение данных в XML файл"""
        try:
            root = ET.Element('bookstore')

            # Основная информация
            ET.SubElement(root, 'name').text = bookstore.name
            ET.SubElement(root, 'next_book_id').text = str(bookstore._next_book_id)
            ET.SubElement(root, 'next_emp_id').text = str(bookstore._next_emp_id)
            ET.SubElement(root, 'next_cust_id').text = str(bookstore._next_cust_id)
            ET.SubElement(root, 'next_sale_id').text = str(bookstore._next_sale_id)

            # Книги
            books_elem = ET.SubElement(root, 'books')
            for book in bookstore.books.values():
                book_elem = ET.SubElement(books_elem, 'book')
                for key, value in book.to_dict().items():
                    child = ET.SubElement(book_elem, key)
                    child.text = str(value)

            # Сотрудники
            employees_elem = ET.SubElement(root, 'employees')
            for employee in bookstore.employees.values():
                emp_elem = ET.SubElement(employees_elem, 'employee')
                for key, value in employee.to_dict().items():
                    child = ET.SubElement(emp_elem, key)
                    child.text = str(value)

            # Клиенты
            customers_elem = ET.SubElement(root, 'customers')
            for customer in bookstore.customers.values():
                cust_elem = ET.SubElement(customers_elem, 'customer')
                for key, value in customer.to_dict().items():
                    child = ET.SubElement(cust_elem, key)
                    child.text = str(value)

            # Продажи
            sales_elem = ET.SubElement(root, 'sales')
            for sale in bookstore.sales.values():
                sale_elem = ET.SubElement(sales_elem, 'sale')
                for key, value in sale.to_dict().items():
                    child = ET.SubElement(sale_elem, key)
                    child.text = str(value)

            # Создание XML дерева и сохранение
            tree = ET.ElementTree(root)
            tree.write(filename, encoding='utf-8', xml_declaration=True)

            print(f"Данные успешно сохранены в {filename}")

        except Exception as e:
            raise FileOperationError(f"Ошибка при сохранении в XML: {e}")

    @staticmethod
    def load_from_xml(bookstore, filename: str) -> None:
        """Загрузка данных из XML файла"""
        try:
            tree = ET.parse(filename)
            root = tree.getroot()

            # Загрузка основной информации
            bookstore.name = root.find('name').text
            bookstore._next_book_id = int(root.find('next_book_id').text)
            bookstore._next_emp_id = int(root.find('next_emp_id').text)
            bookstore._next_cust_id = int(root.find('next_cust_id').text)
            bookstore._next_sale_id = int(root.find('next_sale_id').text)

            # Очистка текущих данных
            bookstore.books.clear()
            bookstore.employees.clear()
            bookstore.customers.clear()
            bookstore.sales.clear()

            # Загрузка книг
            books_elem = root.find('books')
            if books_elem is not None:
                for book_elem in books_elem.findall('book'):
                    book_data = {}
                    for child in book_elem:
                        book_data[child.tag] = child.text

                    # Преобразование типов данных
                    book_data['book_id'] = int(book_data['book_id'])
                    book_data['price'] = float(book_data['price'])
                    book_data['quantity'] = int(book_data['quantity'])
                    book_data['year'] = int(book_data['year'])

                    book = Book.from_dict(book_data)
                    bookstore.books[book.book_id] = book

            # Загрузка сотрудников
            employees_elem = root.find('employees')
            if employees_elem is not None:
                for emp_elem in employees_elem.findall('employee'):
                    emp_data = {}
                    for child in emp_elem:
                        emp_data[child.tag] = child.text

                    emp_data['emp_id'] = int(emp_data['emp_id'])
                    emp_data['salary'] = float(emp_data['salary'])

                    employee = Employee.from_dict(emp_data)
                    bookstore.employees[employee.emp_id] = employee

            # Загрузка клиентов
            customers_elem = root.find('customers')
            if customers_elem is not None:
                for cust_elem in customers_elem.findall('customer'):
                    cust_data = {}
                    for child in cust_elem:
                        cust_data[child.tag] = child.text

                    cust_data['cust_id'] = int(cust_data['cust_id'])

                    customer = Customer.from_dict(cust_data)
                    bookstore.customers[customer.cust_id] = customer

            # Загрузка продаж
            sales_elem = root.find('sales')
            if sales_elem is not None:
                for sale_elem in sales_elem.findall('sale'):
                    sale_data = {}
                    for child in sale_elem:
                        sale_data[child.tag] = child.text

                    sale_data['sale_id'] = int(sale_data['sale_id'])
                    sale_data['book_id'] = int(sale_data['book_id'])
                    sale_data['customer_id'] = int(sale_data['customer_id'])
                    sale_data['employee_id'] = int(sale_data['employee_id'])
                    sale_data['quantity'] = int(sale_data['quantity'])
                    sale_data['total_price'] = float(sale_data['total_price'])

                    sale = Sale.from_dict(sale_data)
                    bookstore.sales[sale.sale_id] = sale

            print(f"Данные успешно загружены из {filename}")

        except FileNotFoundError:
            raise FileOperationError(f"Файл {filename} не найден")
        except Exception as e:
            raise FileOperationError(f"Ошибка при загрузке из XML: {e}")
