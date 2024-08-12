import cv2
import numpy as np
from pathlib import Path
import yaml

def gauss_spot(x0, y0, std, width = 100, height = 100):
    """
    Создает массив, содержащий значения пикселей для Гауссовго пятна.

    Аргументы:
    x0 -- x-координата центра (int или float)
    y0 -- y-координата центра (int или float)
    std -- ширина пятна, выраженная в среднеквадратичном отклонении (int или float)
    width -- количество пикселей по ширине
    height -- количество пикселей по высоте

    Возвращает:
    Трехмерный массив:
    - номер строки пикселя (сверху вниз) (! не снизу вверх, потому что это особенности библиотеки cv2)
    - номер столбца пикселя (слева направо)
    - цвета пикселя по палитре BGR (не RGB, потому что это особенности библиотеки cv2)

    """
    
    image = np.zeros((height, width, 3), dtype=np.uint8)

    if not None in (x0, y0, std):
        for x in range(width):
            for y in range(height):
                dx = x - (x0 + width // 2)              # Сдвиг на половину ширины картинки, чтобы 0 координата была в центре
                dy = (height - y) - (y0 + height // 2)  # Сдвиг на половину высоты картинки, чтобы 0 координата была в центре и 
                                                        # отражение направления y, так как заполнение массива по y соответствует движению вниз по картинке
                g = np.exp(-(dx**2 + dy**2) / (2 * std**2))
                
                green_value = int(g * 255)
                image[y, x] = (0, green_value, 0)

    return image
    
def generate_image_from_yaml(path):
    """
    Сохраняет картинку пятна по параметрам из yaml-файла.

    Аргументы:
    path -- путь к yaml-файлу, содержащим параметры пятна

    Возвращает:
    Изображение пятна в формате .png в том же расположении, что и yaml-файл

    """

    with path.open() as f:
        parameters = yaml.safe_load(f)
    sigma = parameters['std']
    x0, y0 = parameters['position']

    cv2.imwrite(path.parent / f'{path.stem}.png', gauss_spot(x0, y0, sigma))


def get_input(message):
    """
    Делает аккуратный ввод с клавиатуры, с учетом None.

    Аргументы:
    message -- сообщение - приглашение ко вводу

    Возвращает:
    - число, если введено число
    - None, если не введено ничего
    - None, если некорректный ввод

    """
    user_input = input(message)
    
    if user_input == "":
        return None
    
    try:
        return float(user_input)
    except ValueError:
        print("Ошибка: введено не число.")
        return None



if input('Создать новый тест-кейс (\'y\' если да)? ') == 'y':
    while True:
        name = input('Название файла:')
        x0 = get_input('X координата центра:')
        y0 = get_input('Y координата центра:')
        std = get_input('Стандартное отклонение:')
        try:
            var = std**2
        except TypeError:
            var = None

        to_yaml = {
            'std': std,
            'dispersion':  var,
            'position': [x0, y0]
        }

        with open(f'Test Data/{name}.yaml', 'w') as f:
            yaml.safe_dump(to_yaml, f, sort_keys=False)

        cv2.imwrite(f'Test Data/{name}.png', gauss_spot(x0, y0, std))

        if input('Создать новый файл параметров (\'y\' если да)?') != 'y':
            print('Завершаю работу.')
            break


if input('Обновить изображения (\'y\' если да)? ') == 'y':
    pathlist = Path('Test Data/').glob('**/*.yaml')
    for path in pathlist:
        generate_image_from_yaml(path)
