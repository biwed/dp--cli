"""
Содержит клас, для хранения информации о конфигурации приложения
"""
import logging
from functools import cached_property
from jsonschema import validate
from multipledispatch import dispatch


log = logging.getLogger("ConfigCli")
class ConfigCli:
    """Класс конфигурации приложения
    """
    @cached_property
    def schema(self):
        """
        Схема валидатора
        """
        schema = {
            "type": "object",
            "properties":{
                "apiVersion": {"enum":["v0"]},
                "kind": {"enum":["Config"]},
                "spec": {
                    "type": "object",
                        "properties":{
                        "url": {"type":"string"}
                        },
                        "required": ["url"]
                },
            },
            "required": ["apiVersion", "kind"]
        }
        return schema

    def __init__(self, config):
        log.debug("Инифиализирую объект")
        validate(config, self.schema)
        self.config = config
        self.url = config["spec"]["url"]
        log.debug("Объект инициализировался")

    @dispatch(object)
    def make_url(self, config)-> str:
        """
        Функция подготавливает url коннекта к API
        """
        return  (self.url \
            + "/" + str(config['apiVersion']) \
            + "/"+ str(config['kind'])).lower()

    @dispatch()
    def make_url(self)-> str:
        """
        Функция подготавливает url коннекта к API
        """
        return  self.url
