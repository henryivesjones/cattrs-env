import os
from ast import literal_eval
from typing import List

import cattrs

converter: cattrs.Converter = cattrs.Converter()


class CattrsEnvValidationError(Exception):
    """
    Raised when Environment Variable validation fails.
    """

    validation_errors: List[str]

    def __init__(self, validation_errors: List[str]):
        self.validation_errors = validation_errors
        self.message = "\n" + "\n".join(self.validation_errors)
        super().__init__(self.message)


class CattrsEnv:
    """
        Subclass this class to utilize the `load` class method.

        ```
    # attrs example:
    @attrs.define
    class AppConfig(CattrsEnv):
        A: int
        B: float
    config = AppConfig.load()

    # dataclass example:
    @dataclass
    class AppConfig(CattrsEnv):
        A: int
        B: float
    config = AppConfig.load()
        ```
    """

    @classmethod
    def load(cls):
        """
        Loads, parses, and validates Environment Variables from `os.environ`.

        This should be called AFTER any `os.environ` manipulation is done.

        ```
        @dataclass
        class AppConfig(CattrsEnv):
            A: str

        # Raises CattrsEnvValidationError because 'A' envvar is not set.
        app_config = AppConfig.load()
        os.environ['A'] = 'abcdef'
        # succeeds because 'A' envvar is now set.
        app_config = AppConfig.load()
        ```
        """
        _errs = []
        parsed_env = {}
        for key, value in os.environ.items():
            try:
                evaluated_value = literal_eval(value)
            except ValueError:
                evaluated_value = value
            parsed_env[key] = evaluated_value
        try:
            return converter.structure(parsed_env, cls)
        except cattrs.ClassValidationError as e:
            _errs = cattrs.transform_error(e)
        raise CattrsEnvValidationError(_errs)


__all__ = ["CattrsEnv", "CattrsEnvValidationError", "converter"]
__version__ = "1.0.1"
