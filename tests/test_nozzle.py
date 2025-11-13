import unittest
from src.nozzle import NozzleInputs, performance

class TestNozzle(unittest.TestCase):
    def test_reasonable_numbers(self):
        inp = NozzleInputs(Pc=60e5, Tc=3500.0, Pa=101325.0, gamma=1.22, Mw=0.022, epsilon=10.0)
        out = performance(inp)
        # Exit flow should be supersonic for a typical expanded nozzle
        self.assertGreater(out.Me, 1.0)
        # Exit velocity, specific impulse, and thrust coefficient should be in a plausible range
        self.assertGreater(out.Ve, 1000.0)
        self.assertGreater(out.Isp, 100.0)
        self.assertGreater(out.CF, 1.0)

    def test_epsilon_increase_effect(self):
        # Increasing area ratio (ε) generally increases exit Mach (Me) and CF (ideal, all else equal)
        base = NozzleInputs(Pc=60e5, Tc=3500.0, Pa=101325.0, gamma=1.22, Mw=0.022, epsilon=10.0)
        big  = NozzleInputs(Pc=60e5, Tc=3500.0, Pa=101325.0, gamma=1.22, Mw=0.022, epsilon=20.0)
        ob = performance(base); og = performance(big)
        self.assertGreater(og.Me, ob.Me)
        self.assertGreater(og.CF, ob.CF)
