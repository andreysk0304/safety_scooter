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


        password_hash: str = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        return password_hash



    async def check_password(self, password: str, password_hash: str) -> bool:
        '''
        Функция сравнивает пароль с хэшем из базы данных

        :param password: Пароль пользователя
        :param password_hash: Хэш пароля из базы данных
        :return: Дествителен ли пароль
        '''

        if bcrypt.checkpw(password_hash.encode(), password_hash):
            return True

        else:
            return False


HashComponent = hash_component()