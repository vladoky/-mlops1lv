# MLOPS-1LV

1. **/models** - Выводит список моделей, которые мы используем 
2. **/predict** - Предсказывает значение модели
3. **/delete_model** - Удаляет существующую модель.

Образ лежит на DockerHub под названием vladokyokydoky/my-microservice

Образ в dockerhub:
https://hub.docker.com/r/vladokyokydoky/my-microservice

Здесь у нас есть два класса тестов: 
1.**TestModelTrainingAPI для тестирования API обучения моделей**
2.**TestModelPredictionAPI для тестирования API предсказаний**

### Каждый класс содержит несколько тестов, которые используют requests для отправки HTTP-запросов к икросервису и проверяют ответы


