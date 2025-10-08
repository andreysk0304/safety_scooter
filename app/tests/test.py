import asyncio

from app.handlers.components.hash_component import HashComponent

passw = 'qwerty123!'

data = asyncio.run(HashComponent.hash_password(password=passw))

print(data)