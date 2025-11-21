import bcrypt


class HashComponent:

    @staticmethod
    async def hash_password(password: str) -> str:
        '''
        Функция хэширует пароль пользователя

        :param password: Пароль пользователя
        :return: Захэшированный пароль
        '''

        password_hash_bytes = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        password_hash: str = password_hash_bytes.decode('utf-8')

        return password_hash


    @staticmethod
    async def check_password(password: str, password_hash: str) -> bool:
        '''
        Функция сравнивает пароль с хэшем из базы данных

        :param password: Пароль пользователя
        :param password_hash: Хэш пароля из базы данных (может быть в формате b'...' или обычной строке)
        :return: Действителен ли пароль
        '''

        password_bytes = password.encode('utf-8')
        
        if password_hash.startswith("b'") and password_hash.endswith("'"):
            password_hash = password_hash[2:-1]
        elif password_hash.startswith('b"') and password_hash.endswith('"'):
            password_hash = password_hash[2:-1]

        hash_bytes = password_hash.encode('utf-8')

        return bcrypt.checkpw(password_bytes, hash_bytes)