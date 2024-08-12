import json
from datetime import datetime
import pytest
import yaml

from image_processor import spot_parameters

results = []

@pytest.fixture()
def accuracy():
    return 0.95


@pytest.fixture()
def get_parameters(request):
    filename = request.param

    with open(f'Test Data/{filename}.yaml', 'r') as f:
        parameters_expected = yaml.safe_load(f)
    parameters_actual = spot_parameters(f'Test Data/{filename}.png')

    return filename, parameters_expected, parameters_actual


def pytest_sessionfinish(session, exitstatus):
    with open('test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)