import pytest
from datetime import datetime

from conftest import results


@pytest.mark.parametrize('get_parameters', ['empty'], indirect=True)
def test_empty(get_parameters):
    """
    Проверяет, верно ли работает функция в случае отсутствия пятна.
    
    Ожидаемый результат:
    std: null
    dispersion: null
    position: [null, null]

    """
    filename, parameters_expected, parameters_actual = get_parameters

    expected = parameters_expected
    actual = parameters_actual
    
    test_condition = expected == actual
    error_message = 'Значения не равны None'

    try:
        assert test_condition, error_message
        result = "pass"
        error_message = None
    except AssertionError as e:
        result = "fail"
        error_message = str(e)

    results.append({
        "test_type": f"test_empty[{filename}]",
        "input": actual,
        "expected": expected,
        "result": result,
        "error_message": error_message,
        "timestamp": datetime.now().isoformat()
    })

    assert test_condition, error_message


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
    filename, parameters_expected, parameters_actual = get_parameters
    
    expected = parameters_expected['position'][0]
    actual = parameters_actual['position'][0]
    
    test_condition = expected == actual
    error_message = 'Координаты X не совпадают'

    try:
        assert test_condition, error_message
        result = "pass"
        error_message = None
    except AssertionError as e:
        result = "fail"
        error_message = str(e)

    results.append({
        "test_type": f"test_position_x[{filename}]",
        "input": actual,
        "expected": expected,
        "result": result,
        "error_message": error_message,
        "timestamp": datetime.now().isoformat()
    })

    assert test_condition, error_message


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
    filename, parameters_expected, parameters_actual = get_parameters
    
    expected = parameters_expected['position'][1]
    actual = parameters_actual['position'][1]
    
    test_condition = expected == actual
    error_message = 'Координаты Y не совпадают'

    try:
        assert test_condition, error_message
        result = "pass"
        error_message = None
    except AssertionError as e:
        result = "fail"
        error_message = str(e)

    results.append({
        "test_type": f"test_position_y[{filename}]",
        "input": actual,
        "expected": expected,
        "result": result,
        "error_message": error_message,
        "timestamp": datetime.now().isoformat()
    })
    assert test_condition, error_message


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
    filename, parameters_expected, parameters_actual = get_parameters
    accuracy_value = accuracy
    expected = parameters_expected['std']
    actual = parameters_actual['std']

    test_condition = ((expected - actual) / expected <= (1 - accuracy_value)
                        or
                        (expected - actual) <= (1 - accuracy_value))
    error_message = f'Среднеквадратичные отклонения не совпадают с достатчной точностью ({accuracy_value*100}% либо разница <0.05)'
    
    try:
        assert test_condition, error_message
        result = "pass"
        error_message = None
    except AssertionError as e:
        result = "fail"
        error_message = str(e)

    results.append({
        "test_type": f"test_std[{filename}]",
        "input": actual,
        "expected": expected,
        "result": result,
        "error_message": error_message,
        "timestamp": datetime.now().isoformat()
    })
    assert test_condition, error_message


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
    filename, parameters_expected, parameters_actual = get_parameters
    accuracy_value = accuracy
    expected = parameters_expected['dispersion']
    actual = parameters_actual['dispersion']
    
    test_condition = ((expected - actual) / expected <= (1 - accuracy_value)
                        or
                        (expected - actual) <= (1 - accuracy_value))
    error_message = f'Дисперсии не совпадают с достатчной точностью ({accuracy_value*100}% либо разница <0.05)'

    try:
        assert test_condition, error_message
        result = "pass"
        error_message = None
    except AssertionError as e:
        result = "fail"
        error_message = str(e)

    results.append({
        "test_type": f"test_dispersion[{filename}]",
        "input": actual,
        "expected": expected,
        "result": result,
        "error_message": error_message,
        "timestamp": datetime.now().isoformat()
    })

    assert test_condition, error_message




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
    filename, _, parameters_actual = get_parameters
    
    actual = 'var == sigma**2' if parameters_actual['dispersion'] == parameters_actual['std']**2 else 'var <> sigma**2'
    expected = 'var == sigma**2'

    test_condition = actual
    error_message = f'Дисперсия пятна не равна квадрату его среднеквадратичного отклонения'

    try:
        assert test_condition, error_message
        result = "pass"
        error_message = None
    except AssertionError as e:
        result = "fail"
        error_message = str(e)

    results.append({
        "test_type": f"test_std_dispersion_congruence[{filename}]",
        "input": actual,
        "expected": expected,
        "result": result,
        "error_message": error_message,
        "timestamp": datetime.now().isoformat()
    })

    assert test_condition, error_message
