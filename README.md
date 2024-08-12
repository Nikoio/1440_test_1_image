# Тестовое задание. 1 - изображение

План по заданию
- [x] Реализовать скрипт для обработки изображения
    - [x] Реализовать скрипт для генерации тестовых данных
- [x] Реализовать 3 тестовые функции для каждого входного значения
- [x] Реализовать функцию отправки метрик в базу данных
- [x] Результат обработки и результаты тестов собрать в json файл
- [x] В txt собрать проекцию на оси изображения

 
Проект состоит из следующих модулей:
- data_generator.py - Создает yaml-файлы с параметрами пятна и создает изображения пятен по этим файлам
- image_processor.py - Обрабатывает изображение пятна и возвращает его параметры
- test_all.py - Тест функций модуля image_processor
    - В силу реализации скрипта обработки, не все тесты проходят. На данный момент проходят 13 тестов, и не проходят 3.
    - Возвращает файл test_results.json с результатами теста
- conftest.py - вспомогательный модуль для тестирования
- metrics_to_DB.py - Отправляет посчитанные метрики в базу данныз с помощщью influx DB
    - Требует создания организации "1440_test_1_image" и бакета "Bucket_1"
- metrics_to_json.py - Считает параметры изображений и записывает в файл image_metrics.json 
- projections_to_txt.py - Считает проекции изображений и записывает в файл projetions.txt
