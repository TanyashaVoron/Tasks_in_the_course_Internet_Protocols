import time
import socket
import ssl
import mimetypes
import os
import base64
import json

from task5.Message import Message

# Инициализируем типы MIME
mimetypes.init()


class ConfigData:
    def __init__(self, path: str):
        # Устанавливаем порт по умолчанию
        self.port = 465
        # Открываем файл конфигурации и загружаем его содержимое в формате JSON
        with open(path, encoding="utf8") as file:
            config = json.load(file)
            # Получаем адрес сервера и пользователя из файла конфигурации
            self.host_address = config["host_address"]
            self.user_address = config["user_address"]
            # Имя пользователя из его адреса
            self.user_name = self.user_address.split('@')[0]
            # Пароль пользователя и список получателей сообщения
            self.password = config["password"]
            self.recipients = config["recipients"]
            # Файл с текстом сообщения, тему сообщения и список вложений
            self.message_file = config["message_file"]
            self.subject = config["subject"]
            self.attachments = config["attachments"]


class Attachment:
    def __init__(self, filename):
        # Получаем расширение файла и соответствующий ему тип MIME
        file_extension = os.path.splitext(filename)[1]
        content_type = mimetypes.types_map[file_extension]
        # Получаем имя файла и кодируем его в base64
        name = filename.split('/')[-1]
        base64_filename = f"=?UTF-8?B?{base64.b64encode(name.encode()).decode()}?="
        # Получаем содержимое файла и кодируем его в base64
        base64_attachment = self.get_file_content(filename)
        # Формируем содержимое вложения
        self.content = f'Content-Type: {content_type}; name="{base64_filename}"\n' \
                       f'Content-Disposition: attachment; filename="{base64_filename}"\n' \
                       f'Content-Transfer-Encoding: base64\n' \
                       f'\n' \
                       f'{base64_attachment}'

    @staticmethod
    def get_file_content(filename):
        # Открываем файл в бинарном режиме и читаем его содержимое
        with open(filename, "rb") as f:
            # Кодируем содержимое файла в base64 и декодируем в строку
            return base64.b64encode(f.read()).decode()


def request(socket, request):
    # Отправляем запрос на сервер и получаем ответ
    socket.send((request + '\n').encode())
    recv_data = socket.recv(65535).decode()
    return recv_data


def create_send_message(config):  # Создаем и отправляем сообщения на основе конфигурационных данных
    subject = config.subject
    message = Message(config)
    # Если нет вложений, формируем сообщение без них
    if not config.attachments:
        return f'Subject: =?UTF-8?B?{base64.b64encode(subject.encode()).decode()}?=\n{message.text}\n.\n'
    # Если есть вложения, добавляем их к сообщению
    message.append(message.text)
    attachments = [Attachment(filename).content for filename in config.attachments]
    [message.append(a) for a in attachments]
    message.end()
    return message.content()


def main():
    # Получаем конфигурационные данные
    config = ConfigData("./data/config.json")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        # Устанавливаем соединение с сервером
        client.connect((config.host_address, config.port))
        client = ssl.wrap_socket(client)
        client.recv(1024)
        # Аутентификация на сервере
        request(client, f'EHLO {config.user_name}')
        print(f'USERNAME: {config.user_name}\nPASSWORD: {config.password}\n')
        base64login = base64.b64encode(config.user_address.encode()).decode()
        base64password = base64.b64encode(config.password.encode()).decode()
        request(client, 'AUTH LOGIN')
        request(client, base64login)
        print('Authentication successful\n' if '2.7.0' in request(client, base64password)
              else 'Wrong login or password\n')
        # Отправка сообщения на сервер
        print('FROM:', request(client, f'MAIL FROM:{config.user_address}')[10::])
        for recipients in config.recipients:
            time.sleep(1)
            print('TO:', request(client, f'RCPT TO:{recipients}')[10::])
        request(client, 'DATA')
        print(request(client, create_send_message(config))[10::])


if __name__ == "__main__":
    main()
