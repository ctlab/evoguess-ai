import unittest

from algorithm.module.mutation import OneBit, Uniform, Doer
from instance.module.variables import Backdoor, Interval


class RandomStateStub:
    def __init__(self, *values):
        self.index = -1
        self.values = values

    def randint(self, *args):
        self.index += 1
        return self.values[0][self.index]

    def rand(self, *args):
        self.index += 1
        return self.values[self.index]


class TestMutation(unittest.TestCase):
    def test_one_bit(self):
        mutation = OneBit()
        backdoor = Backdoor(
            from_vars=Interval(start=1, length=8).variables()
        )

        mutation.random_state = RandomStateStub([3])
        self.assertEqual(
            mutation.mutate(
                backdoor.get_copy([1, 1, 0, 1, 1, 0, 1, 1]),
            ),
            backdoor.get_copy([1, 1, 0, 0, 1, 0, 1, 1]),
        )

        mutation.random_state = RandomStateStub([7])
        self.assertEqual(
            mutation.mutate(
                backdoor.get_copy([1, 1, 0, 1, 1, 0, 1, 1]),
            ),
            backdoor.get_copy([1, 1, 0, 1, 1, 0, 1, 0]),
        )

    def test_uniform(self):
        backdoor = Backdoor(
            from_vars=Interval(start=1, length=8).variables()
        )

        mutation = Uniform()
        mutation.random_state = RandomStateStub(
            [0, 0.51, 0.1, 0.23, 0.9, 0.13, 0.8, 0.7]
        )
        self.assertEqual(
            mutation.mutate(
                backdoor.get_copy([1, 1, 0, 1, 1, 0, 1, 1]),
            ),
            backdoor.get_copy([0, 1, 1, 1, 1, 0, 1, 1]),
        )

        mutation.random_state = RandomStateStub(
            [0.6, 0.5, 0.52, 0.69, 0.3, 0.53, 0.8, 0.7],
            [0.01, 0.51, 0.1, 0.23, 0.9, 0.13, 0.8, 0.7]
        )
        self.assertEqual(
            mutation.mutate(
                backdoor.get_copy([1, 1, 0, 1, 1, 0, 1, 1]),
            ),
            backdoor.get_copy([0, 1, 1, 1, 1, 0, 1, 1]),
        )

        mutation = Uniform(flip_scale=2)
        mutation.random_state = RandomStateStub(
            [0, 0.51, 0.1, 0.23, 0.9, 0.13, 0.8, 0.7]
        )
        self.assertEqual(
            mutation.mutate(
                backdoor.get_copy([1, 1, 0, 1, 1, 0, 1, 1]),
            ),
            backdoor.get_copy([0, 1, 1, 0, 1, 1, 1, 1]),
        )

    def test_doer(self):
        backdoor = Backdoor(
            from_vars=Interval(start=1, length=8).variables()
        )

        mutation = Doer()
        mutation.random_state = RandomStateStub(
            0.2, [0, 0.51, 0.1, 0.23, 0.9, 0.13, 0.8, 0.7]
        )
        self.assertEqual(
            mutation.mutate(
                backdoor.get_copy([1, 1, 0, 1, 1, 0, 1, 1]),
            ),
            backdoor.get_copy([0, 1, 1, 1, 1, 0, 1, 1]),
        )
