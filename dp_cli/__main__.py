"""
Запуск главной функции
"""
# pylint: disable=logging-fstring-interpolation
import logging
import click
import yaml
from dp_cli.ConfigCli import ConfigCli
#import requests



log = logging.getLogger("checker_validator")
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(
    level=logging.DEBUG,
    format=FORMAT
)

def make_url(shcema: dict):
    """
    Функция подготавливает url коннекта к API
    """
    return  (shcema['spec']['url'] \
        + "/" + str(shcema['apiVersion']) \
        + "/"+ str(shcema['kind'])).lower()

def load_yaml(file: str) -> dict:
    """
    Функция подготавливает загружает yaml файл
    """
    try:
        with open(file) as yaml_file:
            try:
                result = yaml.safe_load(yaml_file)
                log.debug(result)
            except yaml.YAMLError as yaml_error:
                log.error(f"Проблемы с загрузкой yaml файла {yaml_error}")
    except FileNotFoundError as file_error:
        log.error(f"Не задан файл конфигурации {file_error}")
    return result


@click.command()
@click.option('--config', default="config.yaml", help='Config file')
@click.option('--file', default="test.yaml", help='Object file')
@click.argument('action')
def main(config, file, action):
    """
    Функция вызова для объектов.
    Переменная:
        file - файл конфигурации
        action - действие применяемое к объекту
    """
    log.debug("Получил данные")
    program_config_yaml = load_yaml(config)
    log.debug("Инициализирую конфиг")
    program_config = ConfigCli(program_config_yaml)
    url = program_config.make_url()
    log.debug(f"Url = {url}")
    object_config = load_yaml(file)
    url = program_config.make_url(object_config)
    log.debug(f"Url = {url}")
    log.debug("Программа завершина")

if __name__ == '__main__':
    main()
