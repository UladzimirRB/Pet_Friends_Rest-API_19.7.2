import json
from settings import valid_email, valid_password
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


class ArgumentsException (Exception):
    pass

class PetFriends:
    """API библиотека к приложению Pet Friends"""

    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, passwd: str) -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате
        JSON с уникальным ключем пользователя, найденного по указанным e-mail и паролем"""

        headers = {
            'email': email,
            'password': passwd,
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result

    def get_list_of_pets(self, auth_key: json, filter: str = "") -> json:
        """Метод делает запрос к API сервера и возвращает статус запроса и результат в формате JSON
        со списком найденных питомцев, совпадающих с фильтром"""

        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        # if filter != "" or filter != "my_pets"
        #     raise

        res = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str,
                    age: str, pet_photo: str) -> json:
        """Метод отправляет  на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        # Задаем диапазон валидных значений возраста
        if len(age) != 0:
            if int(age) <0 or int(age)>100:
                raise  ArgumentsException("возраст питомца может быть в диапазоне от 0 до 100 лет")
        if age =='':
            raise ArgumentsException("возраст не может быть пустым")
        if name == '':
            raise ArgumentsException("имя не может быть пустым")
        if animal_type == '':
            raise ArgumentsException("порода не может быть пустой")

        for i in range(33, 65):
            if chr(i) in name:
                raise ArgumentsException("имя не может содержать спецсимволы")
                break
        for i in range(91, 97):
            if chr(i) in name:
                raise ArgumentsException("имя не может содержать спецсимволы")
                break

        for i in range(33, 65):
            if chr(i) in animal_type:
                raise ArgumentsException("вид животного не может содержать спецсимволы")
                break
        for i in range(91, 97):
            if chr(i) in animal_type:
                raise ArgumentsException("вид животного не может содержать спецсимволы")
                break
        if name[0] == ' ':
            raise ArgumentsException("имя животного не может начинаться с пробела")
        if animal_type[0] == ' ':
            raise ArgumentsException("вид животного не может начинаться с пробела")



        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет на сервер запрос на удаление питомца по указанному ID и возвращает
        статус запроса и результат в формате JSON с текстом уведомления о успешном удалении.
        НО, есть баг - в result приходит пустая строка, но status при этом = 200"""

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def update_pet_info(self, auth_key: json, pet_id: str, name: str,
                        animal_type: str, age: int) -> json:
        """Метод отправляет запрос на сервер о обновлении данных питомца по указанному ID и
        возвращает статус запроса и result в формате JSON с обновлённыи данными питомца"""

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

    def add_pet_without_photo(self, auth_key: json, name: str, animal_type: str,
                    age: str) -> json:
        """Метод отправляет на сервер данные о добавляемом питомце (без фото) и возвращает статус
        запроса на сервер и результат в формате JSON с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result

    def add_photo_to_pet_without_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет на сервер данные о добавляемой фотографии питомца и возвращает статус
        запроса на сервер и результат в формате JSON """

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url +'api/pets/set_photo/'+pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text

        return status, result
