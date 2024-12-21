import re
import yaml
import sys

class ConstDeclaration:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Array:
    def __init__(self, values):
        self.values = values

class Config:
    def __init__(self):
        self.constants = []
        self.arrays = []

    def add_constant(self, const):
        self.constants.append(const)

    def add_array(self, array):
        self.arrays.append(array)

# Функция для вычисления константных выражений
def evaluate_expression(expr, constants):
    # Сначала определим все константы
    for const in constants:
        # Если значение константы - строка, обрабатываем её как строку
        if isinstance(const.value, str):
            expr = re.sub(r'\b' + const.name + r'\b', f'"{const.value}"', expr)
        else:
            expr = re.sub(r'\b' + const.name + r'\b', str(const.value), expr)

    # Поддержка функций len() и ord()
    expr = re.sub(r'len\(([^)]+)\)', r'len(\1)', expr)  # Поддержка len()
    expr = re.sub(r'ord\(([^)]+)\)', r'ord(\1)', expr)  # Поддержка ord()

    # Вычислим результат простого математического выражения
    try:
        return eval(expr)
    except Exception as e:
        raise ValueError(f"Ошибка при вычислении выражения: {expr}") from e

# Функция для парсинга константных выражений
def parse_const_definition(line):
    print(f"Проверка константы: {line}")  # Отладочный вывод
    match = re.match(r'\(def (\w+) (.+)\);', line)
    if match:
        name = match.group(1)
        value_expr = match.group(2)
        # Убираем кавычки вокруг строк (если они есть)
        value_expr = value_expr.strip('"')
        # Преобразуем строку в число или оставляем строкой
        try:
            value_expr = float(value_expr) if '.' in value_expr else int(value_expr)
        except ValueError:
            pass  # Оставляем как строку, если не можем преобразовать в число
        return ConstDeclaration(name, value_expr)
    return None

# Функция для парсинга массивов
def parse_array(line):
    print(f"Проверка массива: {line}")  # Отладочный вывод
    match = re.match(r'\((.*)\)', line)
    if match:
        values_str = match.group(1).strip()
        values = [v.strip() for v in values_str.split()]
        return Array(values)
    return None

# Функция для парсинга выражений с вычислением
def parse_expression(line, constants):
    print(f"Проверка выражения: {line}")  # Отладочный вывод
    match = re.match(r'\|(.+)\|', line)
    if match:
        expression = match.group(1).strip()
        return evaluate_expression(expression, constants)
    return None

# Основной парсер конфигурации
def parse_config(file_path):
    config = Config()
    result = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()

            # Пропуск пустых строк
            if not line:
                continue

            # Пропуск комментариев
            if line.startswith('%'):
                continue

            # Парсинг объявления констант
            const = parse_const_definition(line)
            if const:
                config.add_constant(const)
                continue

            # Парсинг массивов
            array = parse_array(line)
            if array:
                config.add_array(array)
                continue

            # Парсинг выражений
            expression_result = parse_expression(line, config.constants)
            if expression_result is not None:
                result.append(expression_result)
                continue

            # Обработка ошибки, если строка не соответствует синтаксису
            print(f"Ошибка: Неизвестная конструкция: {line}")  # Отладочный вывод
            raise SyntaxError(f"Неизвестная конструкция: {line}")

    return config, result


# Функция для конвертации в формат YAML
def config_to_yaml(config, result):
    # Преобразуем константы в YAML-совместимый формат без кавычек
    def represent_no_quotes(dumper, value):
        # Если значение - строка, и она не содержит пробелов или специальных символов, не заключаем в кавычки
        if isinstance(value, str) and not re.search(r'\s', value):
            return dumper.represent_scalar('tag:yaml.org,2002:str', value, style=None)  # без кавычек
        return dumper.represent_scalar('tag:yaml.org,2002:str', value)  # с кавычками если это строка

    yaml.add_representer(str, represent_no_quotes)  # Для строковых значений

    data = {
        'constants': {const.name: const.value for const in config.constants},
        'arrays': [array.values for array in config.arrays],
        'results': result
    }
    
    return yaml.dump(data, default_flow_style=False, allow_unicode=True)

# Главная функция обработки
def main(input_file, output_file):
    try:
        # Парсим конфигурационный файл
        config, result = parse_config(input_file)
        
        # Преобразуем в YAML и записываем в файл
        yaml_content = config_to_yaml(config, result)
        with open(output_file, 'w') as output:
            output.write(yaml_content)

        print(f"Конфигурация успешно преобразована в YAML и сохранена в {output_file}")
    except (FileNotFoundError, SyntaxError, ValueError) as e:
        print(f"Ошибка: {str(e)}")

# Точка входа в программу
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Использование: python config_parser.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    main(input_file, output_file)
