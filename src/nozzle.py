import math
from dataclasses import dataclass
from typing import Tuple

from .thermo import mach_from_area_ratio, pressure_ratio_from_M, temperature_ratio_from_M, R_UNIVERSAL

@dataclass
class NozzleInputs:
    Pc: float        # chamber pressure, Pa
    Tc: float        # chamber temperature, K
    Pa: float        # ambient pressure, Pa
    gamma: float     # specific heat ratio
    Mw: float        # molar mass, kg/mol
    epsilon: float   # area ratio Ae/At

@dataclass
class NozzleOutputs:
    Me: float
    Pe: float
    Te: float
    Ve: float
    CF: float
    Isp: float
    F_per_At: float  # thrust per throat area, N/m^2

def performance(inp: NozzleInputs) -> NozzleOutputs:
    """
    Ideal (isentropic) nozzle with separated thrust:
      CF = (F)/(Pc*At) = √((2γ^2)/(γ-1) * (2/(γ+1))^{(γ+1)/(γ-1)} * (1 - (Pe/Pc)^{(γ-1)/γ})) + (Pe - Pa)/Pc * ε
      Isp = F / (mdot*g0) ; mdot = ρt * At * at (implicitly canceled in CF-based form)
    Here we compute via exit velocity and then thrust coefficient.
    """
    g0 = 9.80665
    g = inp.gamma
    R = R_UNIVERSAL / inp.Mw

    # exit state (isentropic)
    Me = mach_from_area_ratio(inp.epsilon, g)
    Pe = inp.Pc * pressure_ratio_from_M(Me, g)
    Te = inp.Tc * temperature_ratio_from_M(Me, g)

    # exit velocity: Ve = M * a = M * sqrt(gamma*R*Te)
    Ve = Me * math.sqrt(g * R * Te)

    # Thrust coefficient (split into momentum + pressure terms):
    # Momentum term: CF_m = Ve / c*
    # Use characteristic velocity c* ≈ sqrt(R*Tc) / (γ * (2/(γ+1))^{(γ+1)/(2(γ-1))})   (ideal)
    cstar = math.sqrt(R * inp.Tc) / (g * (2/(g+1))**((g+1)/(2*(g-1))))
    CF_m = Ve / cstar
    CF_p = (Pe - inp.Pa) / inp.Pc * inp.epsilon
    CF = CF_m + CF_p

    # Thrust per throat area: F/At = CF * Pc
    F_per_At = CF * inp.Pc

    # Isp from CF: Isp = CF * Pc / (mdot/At * g0).
    # mdot/At ≈ Pc / c*  -> Isp ≈ CF * c* / g0
    Isp = CF * cstar / g0

    return NozzleOutputs(Me=Me, Pe=Pe, Te=Te, Ve=Ve, CF=CF, Isp=Isp, F_per_At=F_per_At)
