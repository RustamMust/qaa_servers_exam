# Экзамен 'Сайт для автотестов API и UI'

## Описание

Проект - экзаменационная работа по Python, Selenium, requests, pytest

## Installation

1. Склонируйте репозиторий с сайтом:
```
git clone https://github.com/GC-QAA-Edu/exam_srv.git
```

2. Соберите образ сайта:
```
docker build -t exam_srv .
```

3. Склонируйте репозиторий с тестами:
```
git clone https://github.com/RustamMust/qaa_servers_exam.git
```

4. Соберите образ из Dockerfile с тестами:
```
docker build -t rustamtest .
```

5. Скачайте образ Selenium + Chrome:
```
docker pull seleniarm/standalone-chromium
```

6. Создайте общую для всех контейнеров сеть:
```
docker network create exam_network
```

7. Проверьте, что сеть создалась:
```
docker network ls
```

8. Запустите контейнер с сайтом:
```
docker run -it --rm --name exam_srv -p 8081:8081 --network exam_network exam_srv
```

9. Запустите контейнер с Selenium + Chrome:
```
docker run --name rustamselenium -d -p 4444:4444 -p 7900:7900 --shm-size="2g" --rm --network exam_network seleniarm/standalone-chromium
```

10. Запустите контейнер с Python (замените путь "/Users/qamacos/PycharmProjects/servers_exam" на аналогичный на своем хосте):
```
docker run --name rustamtest -d --rm --network exam_network -e REMOTE_BROWSER=http://rustamselenium:4444/wd/hub -e BASE_URL_2=http://host.docker.internal:8081 -v /Users/qamacos/PycharmProjects/servers_exam/allureresults:/test_dir/allure-results rustamtest
```

10. Откройте ссылку в браузере, если нужно посмотреть на работу автотестов:
```
http://localhost:7900/
```
11. Пароль для VNC:
```
secret
```

## How to use the project

1. Основной файл с тестами:
```
test_servers_page.py
```
2. Сгенерировать Allure отчет:
```
pytest -s -v --aluredir=allureresults
```
3. Посмотреть Allure отчет:
```
allure serve allureresults
```
4. Запустить тесты локально: 
```
conftest.py/LOCAL_BROWSER = True
```
5. Запустить в Docker:
```
conftest.py/LOCAL_BROWSER = False
```


