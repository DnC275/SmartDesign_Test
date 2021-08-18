![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/DnC275/SmartDesign_Test)

##Микросервис для электронного магазина
Модель/cущности:
Товар - отвечает за товар на складе, например - телефон такой-то марки от такого-то производителя.

Поля: идентификатор (ID), название, описание, параметры: массив пар ключ/значение

###Подготовка к запуску
1. Склонировать репозиторий:
   ```bash
   git clone https://github.com/DnC275/SmartDesign_Test 
   ```
2. Перейти в скопированную директорию, создать виртуальное окружение и активировать его:
   ```bash
   cd SmartDesign_Test
   python -m venv venv
   ```
   Для Windows:
   ```bash
   venv\Scripts\activate.bat
   ```
   Для Linux/MacOS:
   ```bash
   source venv/bin/activate
   ```
3. Установить необходимые библиотеки:
   ```bash
   pip install -r requirements.txt 
   ```
4. Запустить сервер MongoDB:
   ```bash
   docker run -d -p 27017:27017 mongo
   ```
После этого можно запускать сервис:
```bash
python main.py
```

###Использование
* Создать товар:
   ```bash
   curl -i -H "Content-Type: application/json" -X POST "http://localhost:5000/test/api/products" -d '{"title": "Title of product", "description": "Some description", "parameters": {"first": "f_value", "second": "s_value"}}'
   ```
   Запрос возвращает json с ID созданного товара.
   Пример вывода:
   ```bash
   HTTP/1.0 201 CREATED
   Content-Type: text/html; charset=utf-8
   Content-Length: 34
   Server: Werkzeug/2.0.1 Python/3.9.6
   Date: Wed, 18 Aug 2021 17:05:05 GMT
   
   {"id": "611d3dc1293554d69a4684c2"}
   ```
* Получить список всех существующих товаров:
   ```bash
   curl -i -X GET "http://localhost:5000/test/api/products"
   ```
* Получить товар по его ID:
   ```bash
   curl -i -X GET "http://localhost:5000/test/api/products/<product_id>"
   ```
   Например:
   ```bash 
   [denis@my-laptop ~]$ curl -i -X GET "http://localhost:5000/test/api/products/611d3dc1293554d69a4684c2"
   HTTP/1.0 200 OK
   Content-Type: application/json
   Content-Length: 182
   Server: Werkzeug/2.0.1 Python/3.9.6
   Date: Wed, 18 Aug 2021 17:11:43 GMT
   
   {
     "id": "611d3dc1293554d69a4684c2", 
     "title": "Title of product", 
     "description": "Some description", 
     "parameters": {
       "first": "f_value", 
       "second": "s_value"
     }
   }
   ```
* Получить все товары с определенным названием/параметром:
   ```bash
   curl -i -H "Content-Type: application/json" -X GET "http://localhost:5000/test/api/products/find" -d '{"title": "Title of product"}'
   ```
   Вывод:
   ```bash
   HTTP/1.0 200 OK
   Content-Type: application/json
   Content-Length: 204
   Server: Werkzeug/2.0.1 Python/3.9.6
   Date: Wed, 18 Aug 2021 17:17:42 GMT
   
   [
     {
       "id": "611d3dc1293554d69a4684c2", 
       "title": "Title of product", 
       "description": "Some description", 
       "parameters": {
         "first": "f_value", 
         "second": "s_value"
       }
     }
   ]
   ```
   Аналогично с поиском по параметру:
   ```bash
   [denis@my-laptop ~]$ curl -i -H "Content-Type: application/json" -X GET "http://localhost:5000/test/api/products/find" -d '{"parameters": {"first": "f_value"}}'
   HTTP/1.0 200 OK
   Content-Type: application/json
   Content-Length: 204
   Server: Werkzeug/2.0.1 Python/3.9.6
   Date: Wed, 18 Aug 2021 17:19:56 GMT
   
   [
     {
       "id": "611d3dc1293554d69a4684c2", 
       "title": "Title of product", 
       "description": "Some description", 
       "parameters": {
         "first": "f_value", 
         "second": "s_value"
       }
     }
   ]
   ```
**Note:** В случае, если поиск по id/названию/параметрам не дал результатов, вернется код 404 с соответствующим сообщением:
```bash
[denis@my-laptop ~]$  curl -i -X GET "http://localhost:5000/test/api/products/111111111111111111111111"
HTTP/1.0 404 NOT FOUND
Content-Type: text/html; charset=utf-8
Content-Length: 33
Server: Werkzeug/2.0.1 Python/3.9.6
Date: Wed, 18 Aug 2021 21:15:28 GMT

There is no product with this id
```
или
```bash
[denis@denis-laptop ~]$ curl -i -H "Content-Type: application/json" -X GET "http://localhost:5000/test/api/products/find" -d '{"parameters": {"first": "s_value"}}'
HTTP/1.0 404 NOT FOUND
Content-Type: text/html; charset=utf-8
Content-Length: 48
Server: Werkzeug/2.0.1 Python/3.9.6
Date: Wed, 18 Aug 2021 21:18:53 GMT

There are no products with such characteristics
```
