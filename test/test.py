import os
import unittest
from dataclasses import dataclass
from typing import List, Optional

from attrs import define

from cattrs_env import CattrsEnv, CattrsEnvValidationError


@define
class NestedTestAttrsEnv:
    E: int
    F: str


@define
class TestAttrsEnv(CattrsEnv):
    A: int
    B: float
    C: List[str]
    D: Optional[NestedTestAttrsEnv] = None


@dataclass
class NestedTestDataClassEnv:
    E: int
    F: str


@dataclass
class TestDataClassEnv(CattrsEnv):
    A: int
    B: float
    C: List[str]
    D: Optional[NestedTestDataClassEnv] = None


class TestCattrsEnv(unittest.TestCase):
    def test_attrs_load(self):
        os.environ.clear()
        os.environ.update(
            {
                "A": "1",
                "B": "99.9",
                "C": '["foo", "bar"]',
            }
        )
        env = TestAttrsEnv.load()
        assert env.A == 1
        assert env.B == 99.9
        assert env.C == ["foo", "bar"]
        assert env.D is None

        os.environ.update({"D": "{'E': 1, 'F': 'zaboo'}"})
        env = TestAttrsEnv.load()
        assert env.A == 1
        assert env.B == 99.9
        assert env.C == ["foo", "bar"]
        assert env.D is not None
        assert env.D.E == 1
        assert env.D.F == "zaboo"

        os.environ.update({"A": "foo"})
        with self.assertRaises(CattrsEnvValidationError):
            env = TestAttrsEnv.load()

    def test_dataclass_load(self):
        os.environ.clear()
        os.environ.update(
            {
                "A": "1",
                "B": "99.9",
                "C": '["foo", "bar"]',
            }
        )
        env = TestDataClassEnv.load()
        assert env.A == 1
        assert env.B == 99.9
        assert env.C == ["foo", "bar"]
        assert env.D is None

        os.environ.update({"D": "{'E': 1, 'F': 'zaboo'}"})
        env = TestDataClassEnv.load()
        assert env.A == 1
        assert env.B == 99.9
        assert env.C == ["foo", "bar"]
        assert env.D is not None
        assert env.D.E == 1
        assert env.D.F == "zaboo"

        os.environ.update({"A": "foo"})
        with self.assertRaises(CattrsEnvValidationError):
            env = TestDataClassEnv.load()
