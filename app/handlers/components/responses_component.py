from fastapi import Request, status, HTTPException
from starlette.responses import JSONResponse


class ResponsesComponent:

    '''Класс содержит ответы с "отключением" защиты по политике CORS (Даёт возможность производить запросы с любого домена, т.к у нас приложение, а не сайт.)'''

    @staticmethod
    def response(request: Request, json: dict, status_code: int = 200) -> JSONResponse:
        return JSONResponse(content=json, headers={
            "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
            "Access-Control-Allow-Credentials": "true","Vary": "Origin"
        }, status_code=status_code)


    @staticmethod
    def response_401(request: Request) -> JSONResponse:
        return JSONResponse(content={'detail': 'Не известный токен авторизации.'}, headers={
            "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
            "Access-Control-Allow-Credentials": "true","Vary": "Origin"
        }, status_code=401)


    @staticmethod
    def response_403(request: Request) -> JSONResponse:
        return JSONResponse(content={'detail': 'Отказ доступа.'}, headers={
            "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
            "Access-Control-Allow-Credentials": "true","Vary": "Origin"
        }, status_code=403)


    @staticmethod
    def response_409(request: Request) -> JSONResponse:
        return JSONResponse(content={'detail': 'Аккаунт с таким номером телефона уже существует.'}, headers={
            "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
            "Access-Control-Allow-Credentials": "true", "Vary": "Origin"
        }, status_code=409)


    @staticmethod
    def response_503(request: Request) -> JSONResponse:
        return JSONResponse(content={'detail': 'Не удалось загрузить видео в S3.'}, headers={
            "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
            "Access-Control-Allow-Credentials": "true", "Vary": "Origin"
        }, status_code=503)


    @staticmethod
    def response_401_error() -> HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не верный токен авторизации."
        )