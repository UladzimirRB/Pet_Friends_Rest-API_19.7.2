import pytest

from api import PetFriends
from settings import valid_email, valid_password
import os
from api import ArgumentsException

pf = PetFriends()

def test_add_pet_without_photo(name='Микки', animal_type='кошка', age='2'):
    """Проверяем что можно добавить питомца с корректными данными без фото"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца без фото
    status, result = pf.add_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name
    assert result['pet_photo'] == ''

def test_add_photo_to_pet_without_photo(pet_photo='images/manyak.jpg'):
    """Проверяем что можно добавить фото питомцу у которого не было фото"""

    # Создание питомца без фото
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_pet_without_photo(auth_key, 'Robert', 'dog', '8')

    # Добавление фотографии питомцу
    status, result = pf.add_photo_to_pet_without_photo(auth_key, result['id'], pet_photo)
    assert status == 200
    assert "pet_photo" in result

def test_add_new_pet_with_age_bigger_then_max(name='Маньяк', animal_type='британец',
                                     age='215', pet_photo='images/manyak.jpg'):
    """Проверяем что нельзя добавить питомца с возрастом больше 100 лет"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Проверяем, что срабатывает исключение при вводе возраста больше 100
    with pytest.raises(ArgumentsException):
        pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

def test_add_new_pet_with_age_less_then_min(name='Маньяк', animal_type='британец',
                                     age='-8', pet_photo='images/manyak.jpg'):
    """Проверяем что нельзя добавить питомца с возрастом меньше 0 лет"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Проверяем, что срабатывает исключение при вводе возраста меньше 0
    with pytest.raises(ArgumentsException):
        pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

def test_add_new_pet_with_no_age(name='Маньяк', animal_type='британец',
                                     age='', pet_photo='images/manyak.jpg'):
    """Проверяем что нельзя добавить питомца без указания возраста"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Проверяем, что срабатывает исключение при осутствии ввода возраста
    with pytest.raises(ArgumentsException):
        pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

def test_add_new_pet_with_no_animal_type(name='Маньяк', animal_type='',
                                     age='8', pet_photo='images/manyak.jpg'):
    """Проверяем что нельзя добавить питомца без указания породы"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Проверяем, что срабатывает исключение при вводе пустого типа животного
    with pytest.raises(ArgumentsException):
        pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

def test_add_new_pet_with_no_name(name='', animal_type='cat',
                                     age='8', pet_photo='images/manyak.jpg'):
    """Проверяем что нельзя добавить питомца без указания имени"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Проверяем, что срабатывает исключение при вводе пустого имени
    with pytest.raises(ArgumentsException):
        pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

def test_add_new_pet_with_spec_symbols_in_name(name='[!Маньяк', animal_type='cat',
                                     age='8', pet_photo='images/manyak.jpg'):
    """Проверяем что нельзя добавить питомца который содержит спецсимволы в имени"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Проверяем, что срабатывает исключение при вводе имени, содержащего спецсимволы
    with pytest.raises(ArgumentsException):
        pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

def test_add_new_pet_with_spec_symbols_in_animal_type(name='Маньяк', animal_type='[(@ds!',
                                     age='8', pet_photo='images/manyak.jpg'):
    """Проверяем что нельзя добавить питомца который содержит спецсимволы в породе"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Проверяем, что срабатывает исключение при вводе породы, содержащей спецсимволы
    with pytest.raises(ArgumentsException):
        pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

def test_add_new_pet_with_space_at_beggining_of_name(name=' Маньяк', animal_type='cat',
                                     age='8', pet_photo='images/manyak.jpg'):
    """Проверяем что нельзя добавить питомца c пробелом в начале имени"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Проверяем, что срабатывает исключение при вводе пробела в начале имени
    with pytest.raises(ArgumentsException):
        pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

def test_add_new_pet_with_space_at_beggining_of_animal_type(name='Woolf', animal_type=' dog',
                                     age='10', pet_photo='images/rudik.jpg'):
    """Проверяем что нельзя добавить питомца c пробелом в начале имени"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Проверяем, что срабатывает исключение при вводе пробела в начале имени
    with pytest.raises(ArgumentsException):
        pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)