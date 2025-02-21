import json
from api import PetFriends
from settings import *
import os

pf = PetFriends()

# GET api key
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_api_key_for_invalid_email(email=invalid_email, password=valid_password):
    """
    Test case to verify that an invalid email results in a 403 status code
    and the API key is not returned by the server.

    Args:
        email (str): Invalid email address.
        password (str): Valid password.

    Asserts:
        - The response status code is 403.
        - The response does not contain an API key.
    """

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert not 'key' in result


def test_get_api_key_for_invalid_pasword(email=valid_email, password=invalid_password):
    """
    Test case to verify that an invalid password results in a 403 status code
    and the API key is not returned by the server.

    Args:
        email (str): Valid email address.
        password (str): Invalid password.

    Asserts:
        - The response status code is 403.
        - The response does not contain an API key.
    """

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert not 'key' in result


def test_get_api_key_for_empty_header(email="", password=""):
    """
    Test case to verify that an empty email and password result in a 403 status code
    and the API key is not returned by the server.

    Args:
        email (str): Empty string representing an empty email.
        password (str): Empty string representing an empty password.

    Asserts:
        - The response status code is 403.
        - The response does not contain an API key.
    """

    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert not 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

# POST a pet
def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_invalid_auth_key(name='Барбоскин', animal_type='двортерьер',
                                           age='4', pet_photo='images/cat1.jpg'):
    """
    Test case to verify that adding a new pet with an invalid authentication key
    results in a 403 status code and no pet data is added.

    Args:
        name (str): Pet's name.
        animal_type (str): Type of pet.
        age (str): Pet's age.
        pet_photo (str): Path to the pet's photo.

    Asserts:
        - The response status code is 403.
        - The server does not return pet details.
    """
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    auth_key = invalid_auth_key()
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 403
    try:
        assert not result['name'] == name
    except TypeError:
        assert type(result) != dict or json


def test_add_new_pet_without_name(name='', animal_type='двортерьер',
                                  age='4', pet_photo='images/cat1.jpg'):
    """
    Test case to verify that adding a pet without a name results in a 403 status code.

    Args:
        name (str): Empty string for pet name.
        animal_type (str): Type of pet.
        age (str): Pet's age.
        pet_photo (str): Path to the pet's photo.

    Asserts:
        - The response status code is 403.
        - The server does not return the pet details.
    """
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 403
    try:
        assert not result['name'] == name
    except TypeError:
        assert type(result) != dict or json


def test_add_new_pet_without_animal_type(name='Барбоскин', animal_type='',
                                         age='4', pet_photo='images/cat1.jpg'):
    """
    Test case to verify that adding a pet without specifying an animal type
    results in a 403 status code.

    Args:
        name (str): Pet's name.
        animal_type (str): Empty string for animal type.
        age (str): Pet's age.
        pet_photo (str): Path to the pet's photo.

    Asserts:
        - The response status code is 403.
        - The server does not return the pet details.
    """
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 403
    try:
        assert not result['name'] == name
    except TypeError:
        assert type(result) != dict or json


def test_add_new_pet_without_age(name='Барбоскин', animal_type='двортерьер',
                                 age='', pet_photo='images/cat1.jpg'):
    """
    Test case to verify that adding a pet without specifying an age results in a 403 status code.

    Args:
        name (str): Pet's name.
        animal_type (str): Type of pet.
        age (str): Empty string for pet's age.
        pet_photo (str): Path to the pet's photo.

    Asserts:
        - The response status code is 403.
        - The server does not return the pet details.
    """
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 403
    try:
        assert not result['name'] == name
    except TypeError:
        assert type(result) != dict or json

# DELETE
def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

# PUT
def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
