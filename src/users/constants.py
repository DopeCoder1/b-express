class ErrorCode:
    AUTHENTICATION_REQUIRED = "Требуется аутентификация."
    AUTHORIZATION_FAILED = "Ошибка авторизации. Пользователь не имеет доступа."
    INVALID_TOKEN = "Неверный токен."
    INVALID_CREDENTIALS = "Неверные учетные данные."
    EMAIL_TAKEN = "Email уже занят."
    REFRESH_TOKEN_NOT_VALID = "Недействительный токен обновления."
    REFRESH_TOKEN_REQUIRED = "Требуется токен обновления, либо в теле запроса, либо в куки."
    EMAIL_NOT_FOUND = "Пользыватель с таким email не найден."