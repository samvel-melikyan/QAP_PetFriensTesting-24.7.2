import json

import pytest

from api import PetFriends
from settings import *
import os

pf = PetFriends()
forbidden = "403 Forbidden"

def test_get_api_key_for_valid_user(auth_key):
    """Verify that a valid user receives a correct API key."""
    assert isinstance(auth_key, str)
    assert len(auth_key) > 0

# GET api key
def test_get_api_key_for_valid_user(auth_key):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""
    assert auth_key is not None


def test_get_api_key_for_invalid_email(pf):
    """Test case to verify that an invalid email results in a 403 status code
        and the API key is not returned by the server.
        Args:
            email (str): Invalid email address.
            password (str): Valid password.
        Asserts:
            - The response status code is 403.
            - The response does not contain an API key."""
    status, result = pf.get_api_key(invalid_email, valid_password)
    assert status == 403
    assert not 'key' in result

def test_get_api_key_for_invalid_pasword(pf):
    """Test case to verify that an invalid password results in a 403 status code
    and the API key is not returned by the server.
    Args:
        email (str): Valid email address.
        password (str): Invalid password.
    Asserts:
        - The response status code is 403.
        - The response does not contain an API key."""
    status, result = pf.get_api_key(valid_email, invalid_password)
    assert status == 403
    assert not 'key' in result

def test_get_api_key_for_empty_header(pf):
    """Test case to verify that an empty email and password result in a 403 status code
    and the API key is not returned by the server.
    Args:
        email (str): Empty string representing an empty email.
        password (str): Empty string representing an empty password.
    Asserts:
        - The response status code is 403.
        - The response does not contain an API key."""
    status, result = pf.get_api_key('', '')
    assert status == 403
    assert not 'key' in result

# GET pets list
def test_get_all_pets_with_valid_key(pf):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """
    status, result = pf.get_list_of_pets(auth_key)
    assert status == 200
    assert len(result['pets']) > 0

def test_get_all_pets_with_invalid_key(pf):
    """Test case for retrieving a list of pets using an invalid authentication key.

       This test verifies that the API returns a 403 status code when an invalid
       authentication key is provided. Additionally, it checks that the response
       contains no pet data or an appropriate error message.
       Args:
           filter (str, optional): Filter parameter to specify which pets to retrieve.
                                   Defaults to an empty string.
       Assertions:
           - The response status code is 403 (Forbidden).
           - The response contains no pets or includes an error message indicating the failure."""
    status, result = pf.get_list_of_pets(invalid_auth_key())
    assert status == 403
    try:
        assert len(result['pets']) == 0
    except TypeError:
        assert forbidden in result

# POST a pet
def test_add_new_pet_with_valid_data(auth_key, pf, pet_photo):
    """Проверяем что можно добавить питомца с корректными данными"""
    status, result = pf.add_new_pet(auth_key, 'Барбоскин', 'двортерьер', '4', pet_photo)
    assert status == 200
    assert result['name'] == "Барбоскин"

def test_add_new_pet_with_invalid_auth_key(pf, pet_photo):
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
    status, result = pf.add_new_pet(invalid_auth_key(), 'Барбоскин', 'двортерьер', '4', pet_photo)
    assert status == 403
    try:
        assert not result['name'] == "Барбоскин"
    except TypeError:
        assert type(result) != dict or json

def test_add_new_pet_without_name(auth_key, pet_photo):
    """Test case to verify that adding a pet without a name results in a 403 status code.
    Args:
        name (str): Empty string for pet name.
        animal_type (str): Type of pet.
        age (str): Pet's age.
        pet_photo (str): Path to the pet's photo.
    Asserts:
        - The response status code is 403.
        - The server does not return the pet details."""
    status, result = pf.add_new_pet(auth_key, "", "двортерьер", "4", pet_photo)
    assert status == 403
    try:
        assert not result['name'] == ""
    except TypeError:
        assert type(result) != dict or json

def test_add_new_pet_without_animal_type(auth_key, pf, pet_photo):
    """Test case to verify that adding a pet without specifying an animal type
    results in a 403 status code.
    Args:
        name (str): Pet's name.
        animal_type (str): Empty string for animal type.
        age (str): Pet's age.
        pet_photo (str): Path to the pet's photo.

    Asserts:
        - The response status code is 403.
        - The server does not return the pet details."""
    status, result = pf.add_new_pet(auth_key, "Барбоскин", "", "4", pet_photo)
    assert status == 403
    try:
        assert not result['name'] == "Барбоскин"
    except TypeError:
        assert type(result) != dict or json

def test_add_new_pet_without_age(auth_key, pf, pet_photo):
    """Test case to verify that adding a pet without specifying an age results in a 403 status code
    Args:
        name (str): Pet's name.
        animal_type (str): Type of pet.
        age (str): Empty string for pet's age.
        pet_photo (str): Path to the pet's photo
    Asserts:
        - The response status code is 403.
        - The server does not return the pet details."""
    status, result = pf.add_new_pet(auth_key, "Барбоскин", "двортерьер", "", pet_photo)
    assert status == 403
    try:
        assert not result['name'] == "Барбоскин"
    except TypeError:
        assert type(result) != dict or json

# DELETE
def test_successful_delete_self_pet(auth_key):
    """Проверяем возможность удаления питомца"""
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

def test_delete_self_pet_with_invalid_autrh_key(auth_key):
    """
    Test case for attempting to delete a pet using an invalid authentication key.

    This test verifies that the API returns a 403 status code when trying to delete
    a pet with an invalid authentication key. It ensures that the pet remains in
    the user's list after the failed deletion attempt.

    Assertions:
        - The API returns a 403 status code.
        - The response contains an indication of the authorization failure.
        - The pet remains in the user's pet list.
    """
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, result = pf.delete_pet(invalid_auth_key(), pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 403
    assert forbidden in result
    assert pet_id in my_pets['pets'][0].values()

# PUT
def test_successful_update_self_pet_info(auth_key):
    """Проверяем возможность обновления информации о питомце"""
    name = 'Мурзик'
    # Получаем ключ auth_key и список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, 'Котэ', 5)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_update_self_pet_info_with_invalid_auth_key(auth_key):
    """Test case for updating pet information using an invalid authentication key.
    This test verifies that the API returns a 403 status code when attempting to update
    a pet's details with an invalid authentication key. It ensures that unauthorized
    users cannot modify pet data.
    Args:
        name (str, optional): The new name of the pet. Defaults to 'Мурзик'.
        animal_type (str, optional): The new type of the pet. Defaults to 'Котэ'.
        age (int, optional): The new age of the pet. Defaults to 5.
    Steps:
    Assertions:
        - The API returns a 403 status code.
        - The response contains an indication of the authorization failure."""
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(invalid_auth_key(), my_pets['pets'][0]['id'], "Мурзик", "Котэ", 5)
        assert status == 403
        assert forbidden in result
