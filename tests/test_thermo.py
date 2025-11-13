import unittest
from src.thermo import mach_from_area_ratio, pressure_ratio_from_M

class TestThermo(unittest.TestCase):
    def test_mach_monotonic(self):
        g = 1.22
        M1 = mach_from_area_ratio(5.0, g)
        M2 = mach_from_area_ratio(20.0, g)
        # Larger area ratio (ε) -> higher exit Mach number (Me) for the supersonic branch
        self.assertGreater(M2, M1)

    def test_pressure_ratio_bounds(self):
        g = 1.22
        M = 3.0
        pr = pressure_ratio_from_M(M, g)
        # Isentropic expansion: Pe/Pc must be strictly between 0 and 1
        self.assertGreater(pr, 0.0)
        self.assertLess(pr, 1.0)
