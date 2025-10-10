import bcrypt

class hash_component:

    def __init__(self):

        ...


    async def hash_password(self, password: str) -> str:
        '''
        Функция хэширует пароль пользователя

        :param password: Пароль пользователя
        :return: Захэшированный пароль
        '''


        password_hash: str = str(bcrypt.hashpw(password.encode(), bcrypt.gensalt()))

        return password_hash



    async def check_password(self, password: str, password_hash: str) -> bool:
        '''
        Функция сравнивает пароль с хэшем из базы данных

        :param password: Пароль пользователя
        :param password_hash: Хэш пароля из базы данных
        :return: Дествителен ли пароль
        '''

        password_bytes = password.encode('utf-8')

        hash_bytes = password_hash.encode('utf-8')

        if bcrypt.checkpw(password_bytes, hash_bytes):
            return True

        else:
            return False


HashComponent = hash_component()