import base64


class Message:
    def __init__(self, config):
        # Формируем строку с адресами получателей
        targets_address = ','.join(f'"{x}" <{x}>' for x in config.recipients)
        # Устанавливаем границу для разделения частей сообщения
        self.boundary = f'BoUnD1234567890987654321BoUnD'
        # Формируем заголовок сообщения
        self.header = f'From:{config.user_address}\n' \
                      f'To:{targets_address}\n' \
                      f'Subject: =?UTF-8?B?{base64.b64encode(config.subject or "No subject".encode()).decode()}?=\n' \
                      f'Content-type: multipart/mixed; boundary={self.boundary}\n' \
                      f'\n'
        # Получаем текст сообщения из файла и заменяем символ '.' на '..'
        self.text = self.get_text(config.message_file).replace('\n.', '\n..')

    def append(self, message):
        # Добавляем новую часть сообщения
        self.text += f'{self.start_bound()}\n{message}'

    def start_bound(self):
        # Начальная граница для новой части сообщения
        return f'--{self.boundary}'

    def end_bound(self):
        # Конечна граница для сообщения
        return f'--{self.boundary}--'

    def content(self):
        # Содержимое сообщения
        return f'{self.header}\n{self.text}'

    def end(self):
        # Конец формирования сообщения
        self.text += f'\n{self.end_bound()}\n.\n'

    @staticmethod
    def get_text(filename):
        # Получаем текст сообщения из файла и формируем его содержимое
        with open(filename, "r", encoding="utf8") as f:
            message = "".join(f.readlines())
        content = f'Content-Transfer-Encoding: 8bit\n' \
                  f"Content-Type: text/plain; charset=utf-8\n\n" \
                  f"{message}"
        return content
