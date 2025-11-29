"""
Кастомные исключения для книжного магазина
"""

class BookstoreError(Exception):
    """Базовое исключение для книжного магазина"""
    pass

class BookNotFoundError(BookstoreError):
    """Книга не найдена"""
    pass

class InsufficientQuantityError(BookstoreError):
    """Недостаточное количество книг"""
    pass

class InvalidPriceError(BookstoreError):
    """Неверная цена"""
    pass

class EmployeeNotFoundError(BookstoreError):
    """Сотрудник не найден"""
    pass

class CustomerNotFoundError(BookstoreError):
    """Клиент не найден"""
    pass

class FileOperationError(BookstoreError):
    """Ошибка операции с файлом"""
    pass
