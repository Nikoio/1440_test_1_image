import cv2
import numpy as np


def spot_parameters(path):
    """
    Рассчитывает параметры пятна на иображении (координаты центра, размер)

    Аргументы:
    path -- расположение изображения

    Возвращает:
    Словарь со значениями:
    - std -- среднеквадратичное отклонение пятна
    - dispertion -- дисперсия пятна
    - position -- координаты пятна ([0, 0] - центр изображения)

    Метод:
    1. Делаем из трехцветного изображения одноцветное
    2. Делаем пороговый фильтр ([0-255] -> (0; 255)) с порогом на уровне, соответствующим 1 sigma
    3. Определяем координаты центра с помощью моментов контура пятна
    4. Определяем среднеквадратичное отклонение по среднему расстоянию от центра до контура  
    
    """

    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    height, width = image.shape

    treshold_value = max([max(row) for row in image]) * np.exp(-0.5)
    _, binary_image = cv2.threshold(image, treshold_value, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        M = cv2.moments(contours[0])
        
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00']) 
            cy = int(M['m01'] / M['m00'])
        else:
            cx, cy = width //2, height // 2

        distances = []
        for point in contours[0]:
            distances.append(np.sqrt((point[0][0] - cx)**2 + (point[0][1] - cy)**2))
        std_dev = np.mean(distances)

        return {'std': std_dev, 
                'dispersion': std_dev**2,
                'position': [cx - width //2, height // 2 - cy]}

    else:
        return {'std': None, 
                'dispersion': None,
                'position': [None, None]}