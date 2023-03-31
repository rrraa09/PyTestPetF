
from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat.jpg'):
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




def test_add_new_pet_witout_photo(name='Алиса', animal_type='кошка',
                                     age='4'):
    """Проверяем что можно добавить питомца без фото"""


    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name






def test_successful_add_self_pet_photo(pet_photo='images/cat.jpg'):
    """Проверяем возможность обновления фото питомца"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Если список не пустой, то пробуем обновить его фото
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

        # Проверяем что статус ответа = 200 и фото добавлено
        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        # если спиcок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


#1

def test_add_pet_negative_age_number(name='Fedor', animal_type='cat', age='-3', pet_photo='images/cat.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с отрицательным числом в переменной age.
    Тест не будет пройден если питомец будет добавлен на сайт с отрицательным числом в поле возраст.'''

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 400

#2

def test_unvalid_password(email=invalid_email, password=valid_password):
    '''Проверяем запрос с валидным паролем и с невалидным е-мейлом'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

#3

def test_unvalid_email(email=valid_email, password=invalid_password):
    '''Проверяем запрос с невалидным паролем и с валидным е-мейлом'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

#4

def test_add_new_pet_witout_type(name='Алиса', age='4'):
    """Проверяем что нельзя добавить питомца без породы"""


    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_type(auth_key, name, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

#5

def test_add_new_pet_witout_name(animal_type='кошка',
                                     age='4'):
    """Проверяем что нельзя добавить питомца без имени"""


    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet_without_name(auth_key, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400

#6


def test_get_api_key_without_passwd(email=valid_email):
    """Проверяем, что нельзя войти без пароля"""
    status, result = pf.get_api_key_without_passwd(email)
    assert status == 403
    assert 'key' not in result

#7

def test_add_pet_with_special_characters_in_variable_animal_type(name='Fedor', age='3', animal_type = 'Cat%@', pet_photo='images/cat.jpg'):
    #Проверяем, что можно добавить питомца с символами в породе

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200

#8

def test_add_pet_with_four_digit_age_number(name='Fedor', animal_type='cat', age='1234', pet_photo='images/cat.jpg'):
    '''Проверяем, что можжно добавить питомца с возрастом более трех знаков в переменной age'''
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    number = result['age']

    assert status == 200
    assert len(number) > 3

#9

def test_add_pet_with_a_lot_of_words_in_variable_name(name= 'Пабло Диего Хозе Франциско де Паула Хуан Непомукено Криспин Криспиано де ла Сантисима Тринидад Руиз и Пикассо', animal_type='cat', age='2', pet_photo='images/cat.jpg'):
    '''Проверяем, что можно добавить питомца имя которого превышает 10 слов'''

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    list_name = result['name'].split()
    word_count = len(list_name)

    assert status == 200
    assert word_count > 10

#10

def test_add_pet_with_a_lot_of_words_in_variable_type(name= 'Fedor', animal_type='артезианский нормандский бассет гриффон ', age='2', pet_photo='images/cat.jpg'):
    '''Проверяем, что можно добавить питомца порода которого превышает 3 слов'''

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    list_type = result['animal_type'].split()
    word_count = len(list_type)

    assert status == 200
    assert word_count > 3
