# cattrs-env
`cattrs-env` is an Environment Variable parser/validator which utilizes the [`cattrs`](https://github.com/python-attrs/cattrs) library.

`cattrs-env` parses Environment Variables from `os.environ` and structures them into a [`cattrs` compatible dataclass](https://catt.rs/en/stable/structuring.html#simple-attrs-classes-and-dataclasses). Providing you with easy and type safe environment variables in your project.

Because `cattrs-env` gets the Environment Variables from `os.environ`, it is fully compatible with any Environment Variable loading library such as [`python-dotenv`](https://github.com/theskumar/python-dotenv).

```python
from dataclasses import dataclass
from typing import List, Optional
from cattrs_env import CattrsEnv

@dataclass
class Env(CattrsEnv):
    A: int
    C: List[str]
    B: Optional[float] = None

env = Env.load()

env.A
env.C
env.B
```

# Examples

## dataclass example
```python
import os
from dataclasses import dataclass
from typing import List, Optional

from cattrs_env import CattrsEnv


@dataclass
class Env(CattrsEnv):
    A: int
    C: List[str]
    B: Optional[float] = None


if __name__ == "__main__":
    os.environ.update(
        {
            "A": "99",
            "B": "9.9",
            "C": '["a","b","c", 1]',
        }
    )
    env = Env.load()
    print(env)
```

## attrs example
```python
import os
from typing import List, Optional
import attrs
from cattrs_env import CattrsEnv


@attrs.define
class Config:
    E: str
    F: Optional[int] = None


@attrs.define
class Env(CattrsEnv):
    A: int
    C: List[str]
    D: Config
    B: Optional[float] = None


if __name__ == "__main__":
    os.environ.update(
        {
            "A": "99",
            "B": "9.9",
            "C": '["a","b","c", 1]',
            "D": """{'E':"abcdef"}""",
        }
    )
    env = Env.load()
```
## python-dotenv example
```python
from dataclasses import dataclass
from typing import List, Optional
import dotenv
from cattrs_env import CattrsEnv


@dataclass
class Env(CattrsEnv):
    A: int
    C: List[str]
    B: Optional[float] = None


ENV_FILE_CONTENTS = """
A=1
B=99.9
C="['foo', 'bar']"
"""

if __name__ == "__main__":
    with open(".env", "w") as env_file:
        env_file.write(ENV_FILE_CONTENTS)
    dotenv.load_dotenv()
    env = Env.load()
    print(env)

```

