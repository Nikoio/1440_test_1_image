import pytest
import yaml

from image_processor import spot_parameters


@pytest.fixture()
def get_parameters(request):
    filename = request.param

    with open(f'Test Data/{filename}.yaml', 'r') as f:
        parameters_expected = yaml.safe_load(f)

    parameters_actual = spot_parameters(f'Test Data/{filename}.png')

    return parameters_expected, parameters_actual

@pytest.fixture()
def accuracy():
    return 0.95



@pytest.mark.parametrize('get_parameters', ['empty'], indirect=True)
def test_position(get_parameters):
    """
    Проверяет, верно ли работает функция в случае отсутствия пятна.
    
    Ожидаемый результат:
    std: null
    dispersion: null
    position: [null, null]

    """
    parameters_expected, parameters_actual = get_parameters
    
    assert  parameters_expected == parameters_actual, 'Значения не равны None'


@pytest.mark.parametrize('get_parameters', ['center', 'x_shifted', 'y_shifted'], indirect=True)
def test_position_x(get_parameters):
    """
    Проверяет, верно ли функция определяет X-координату пятна.

    Тест кейсы:
    - Пятно в центре (center)
    - Пятно смещено от центра по оси X (x_shifted)
    - Пятно смещено от центра по оси Y (y_shifted) 

    Ожидаемый результат:
    - center - 0
    - x_shifted - не 0, соответствует валидному значению
    - y_shifted - 0 

    """
    parameters_expected, parameters_actual = get_parameters
    
    assert  parameters_expected['position'][0] == parameters_actual['position'][0], 'Координаты X не совпадают'


@pytest.mark.parametrize('get_parameters', ['center', 'x_shifted', 'y_shifted'], indirect=True)
def test_position_y(get_parameters):
    """
    Проверяет, верно ли функция определяет Y-координату пятна.

    Тест кейсы:
    - Пятно в центре (center)
    - Пятно смещено от центра по оси X (x_shifted)
    - Пятно смещено от центра по оси Y (y_shifted) 

    Ожидаемый результат:
    - center - 0
    - x_shifted - 0
    - y_shifted - не 0, соответствует валидному значению

    """
    parameters_expected, parameters_actual = get_parameters
    
    assert  parameters_expected['position'][1] == parameters_actual['position'][1], 'Координаты Y не совпадают'


@pytest.mark.parametrize('get_parameters', ['center', 'dot', 'plane'], indirect=True)
def test_std(get_parameters, accuracy):
    """
    Проверяет, верно ли функция определяет среднеквадратичное отклонение пятна.

    Тест кейсы:
    - Обычный размер (center)
    - Один пиксель (dot)
    - Размеры пятна больше картинки (plane) 

    Ожидаемый результат:
    - center - не 0, соответствует валидному значению
    - dot - около 0
    - plane - не 0, соответствует валидному значению

    Так как результат вычисления float, то соответствие устанавливается 
    в пределах определенной точности, заданной выше как accuracy.

    """
    parameters_expected, parameters_actual = get_parameters
    accuracy_value = accuracy
    
    assert ((parameters_expected['std'] - parameters_actual['std']) / parameters_expected['std'] <= (1 - accuracy_value)
            or
            (parameters_expected['std'] - parameters_actual['std']) <= (1 - accuracy_value)), f'Среднеквадратичные отклонения не совпадают с достатчной точностью ({accuracy_value*100}% либо разница <0.05)'


@pytest.mark.parametrize('get_parameters', ['center', 'dot', 'plane'], indirect=True)
def test_dispersion(get_parameters, accuracy):
    """
    Проверяет, верно ли функция определяет дисперсию пятна.

    Тест кейсы:
    - Обычный размер (center)
    - Один пиксель (dot)
    - Размеры пятна больше картинки (plane) 

    Ожидаемый результат:
    - center - не 0, соответствует валидному значению
    - dot - около 0
    - plane - не 0, соответствует валидному значению

    Так как результат вычисления float, то соответствие устанавливается 
    в пределах определенной точности, заданной выше как accuracy.

    """
    parameters_expected, parameters_actual = get_parameters
    accuracy_value = accuracy
    
    assert ((parameters_expected['dispersion'] - parameters_actual['dispersion']) / parameters_expected['dispersion'] <= (1 - accuracy_value)
            or
            (parameters_expected['dispersion'] - parameters_actual['dispersion']) <= (1 - accuracy_value)), f'Дисперсии не совпадают с достатчной точностью ({accuracy_value*100}% либо разница <0.05)'



@pytest.mark.parametrize('get_parameters', ['center', 'dot', 'plane'], indirect=True)
def test_std_dispersion_congruence(get_parameters):
    """
    Проверяет, соответствует ли дисперсия пятна квадрату среднеквадратичного отклонения.

    Тест кейсы:
    - Обычный размер (center)
    - Один пиксель (dot)
    - Размеры пятна больше картинки (plane) 

    Ожидаемый результат:
    - center - дисперсия пятна равна квадрату среднеквадратичного отклонения
    - dot - дисперсия пятна равна квадрату среднеквадратичного отклонения
    - plane - дисперсия пятна равна квадрату среднеквадратичного отклонения

    """
    parameters_expected, parameters_actual = get_parameters
    
    assert parameters_actual['dispersion'] == parameters_actual['std']**2, f'Дисперсия пятна не равна квадрату его среднеквадратичного отклонения'
