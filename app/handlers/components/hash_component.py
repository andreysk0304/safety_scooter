import bcrypt


class HashComponent:

    @staticmethod
    async def hash_password(self, password: str) -> str:
        '''
        Функция хэширует пароль пользователя

        :param password: Пароль пользователя
        :return: Захэшированный пароль
        '''


        password_hash: str = str(bcrypt.hashpw(password.encode(), bcrypt.gensalt()))

        return password_hash


    @staticmethod
    async def check_password(self, password: str, password_hash: str) -> bool:
        '''
        Функция сравнивает пароль с хэшем из базы данных

        :param password: Пароль пользователя
        :param password_hash: Хэш пароля из базы данных
        :return: Дествителен ли пароль
        '''

        password_bytes = password.encode('utf-8')

        hash_bytes = password_hash.encode('utf-8')

        return bcrypt.checkpw(password_bytes, hash_bytes)