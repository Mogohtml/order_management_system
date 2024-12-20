# Flask API с документацией Swagger

Это проект Flask API с документацией Swagger, использующий библиотеку `flasgger`. Проект включает аутентификацию пользователей, валидацию данных формы и сопоставление шаблонов.

## Использование

### Запуск приложения

1. **Активируйте виртуальное окружение**:
   - Для Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Для macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

2. **Запустите приложение**:
   ```bash
   python app.py
Отправка запросов
Вы можете использовать инструменты, такие как Postman или cURL, для отправки запросов к API. Вот пример запроса:

Пример запроса
Эндпоинт: /get_form
Метод: POST
Заголовки:

Authorization: Basic YWRtaW46YWRtaW5fcGFzc3dvcmQ=
Тело запроса:

user_name: John Doe
order_date: 2023-10-01
lead_email: john.doe@example.com
Пример ответа

{
  "name": "Order Form"
}
Пример использования cURL
Вы также можете использовать cURL для отправки запросов к API. Вот пример команды:


curl -X POST http://127.0.0.1:5000/get_form \
     -H "Authorization: Basic YWRtaW46YWRtaW5fcGFzc3dvcmQ=" \
     -d "user_name=John Doe&order_date=2023-10-01&lead_email=john.doe@example.com"
Документация API
Документация API автоматически генерируется с использованием библиотеки flasgger. Вы можете просмотреть документацию, перейдя по адресу http://127.0.0.1:5000/apidocs в вашем браузере.
