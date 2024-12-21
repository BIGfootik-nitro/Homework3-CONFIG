import pytest
import yaml
import os
from config_parser import main  

def test_math_operations():
    input_file = 'math_config.cfg'
    output_file = 'math_output.yaml'
    
    expected_result = {
        'arrays': [],
        'constants': {
            'a': 5,
            'b': 10,
            'c': 3
        },
        'results': [
            15,  # a + b
            5,   # b - a
            15,  # a * c
            2,   # b / a
            18   # (a + b) + c
        ]
    }
    
    if not os.path.exists(input_file):
        pytest.fail(f"Файл конфигурации {input_file} не найден.")
    
    main(input_file, output_file)
    
    assert os.path.exists(output_file), f"Файл вывода {output_file} не был создан."
    
    with open(output_file, 'r') as file:
        output_data = yaml.safe_load(file)
    
    assert output_data == expected_result, f"Ошибка: {output_data} != {expected_result}"

def test_text_operations():
    input_file = 'text_config.cfg'
    output_file = 'text_output.yaml'
    
    expected_result = {
        'arrays': [],
        'constants': {
            'greeting': 'Hello',
            'name': 'Alice'
        },
        'results': [
            5, 
            72, 
            'Hello Alice', 
            10  
        ]
    }

    if not os.path.exists(input_file):
        pytest.fail(f"Файл конфигурации {input_file} не найден.")
    
    main(input_file, output_file)
    
    assert os.path.exists(output_file), f"Файл вывода {output_file} не был создан."
    
    with open(output_file, 'r') as file:
        output_data = yaml.safe_load(file)
    
    assert output_data == expected_result, f"Ошибка: {output_data} != {expected_result}"

def test_economics_operations():
    input_file = 'economics_config.cfg'
    output_file = 'economics_output.yaml'
    
    expected_result = {
        'arrays': [],
        'constants': {
            'revenue': 50000,
            'expenses': 30000,
            'employees': 50,
            'company_name': 'TechCorp'
        },
        'results': [
            20000,  
            1000,   
            8       
        ]
    }

    if not os.path.exists(input_file):
        pytest.fail(f"Файл конфигурации {input_file} не найден.")
    
    main(input_file, output_file)
    
    assert os.path.exists(output_file), f"Файл вывода {output_file} не был создан."
    
    with open(output_file, 'r') as file:
        output_data = yaml.safe_load(file)
    
    assert output_data == expected_result, f"Ошибка: {output_data} != {expected_result}"
