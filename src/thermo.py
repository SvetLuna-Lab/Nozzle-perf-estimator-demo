import math

R_UNIVERSAL = 8.314462618  # J/(mol·K)

def gamma_cp(Mw: float, gamma: float) -> float:
    """
    Cp [J/(kg·K)] from gamma and molar mass (Mw in kg/mol):
        Cp = (gamma * R) / (gamma - 1), where R = R_universal / Mw
    """
    R = R_UNIVERSAL / Mw
    return gamma * R / (gamma - 1.0)

def mach_from_area_ratio(epsilon: float, gamma: float) -> float:
    """
    Solve for exit Mach number M_e from area ratio eps = Ae/At (supersonic root).
    Uses fixed-point iteration on isentropic area–Mach relation.
    """
    g = gamma
    # initial guess for supersonic root
    M = 2.5
    for _ in range(100):
        f = (1.0/M) * ((2/(g+1))*(1 + (g-1)*0.5*M*M))**((g+1)/(2*(g-1))) - epsilon
        # derivative (numerical)
        dM = 1e-4
        f2 = (1.0/(M+dM)) * ((2/(g+1))*(1 + (g-1)*0.5*(M+dM)*(M+dM)))**((g+1)/(2*(g-1))) - epsilon
        df = (f2 - f)/dM
        M_new = M - f/df if abs(df) > 1e-12 else M
        if abs(M_new - M) < 1e-8:
            return max(M_new, 1.01)
        M = M_new
    return max(M, 1.01)

def pressure_ratio_from_M(M: float, gamma: float) -> float:
    """Pe/P0 for isentropic expansion."""
    return (1 + (gamma-1)*0.5*M*M) ** (-gamma/(gamma-1))

def temperature_ratio_from_M(M: float, gamma: float) -> float:
    """Te/T0 for isentropic expansion."""
    return (1 + (gamma-1)*0.5*M*M) ** -1
