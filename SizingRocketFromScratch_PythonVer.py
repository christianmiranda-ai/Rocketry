# %% Sizing Rocket Engine from Scratch
# by Christian Miranda
# this is for an N2O/IPA rocket ONLY
# based on Rocket Propulsion Elements & (fill)

# balanced chemical reaction for N2O/IPA combustion:
# C3H8O (l) + 9 N2O (g) -> 9 N2 (g) + 3 CO2 (g) + 4 H2O (g)

# ---------------------------------------------------------------------------------------------------

# library imports:

import math
import matplotlib.pyplot

# ---------------------------------------------------------------------------------------------------

# fundamental assumptions made:

# 1: 
# 2: 
# 3:
# 4:
# 5: at the calculated speed of the exhaust gas, its velocity is greater than Mach 1. as such, the compressible
# flow mach equation has been used to determine what the mach number of the exhaust actually is.

# Me depends on V_e. V_e depends on R_gamma, gamma, T_o, and M_bar.

# ---------------------------------------------------------------------------------------------------

# input parameters:

# Desired thrust (N)
F = input("Enter desired thrust (N): ")
F = float(F)
g_o = 9.81 # acceleration due to gravity (m/s^2)

# ---------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------

# Section 2: Solving for R_gamma (specific gas constant)

# equation: R_gamma = R_u / M_bar
# given:
R_u = 8.314  # universal gas constant (J/(mol*K))
mm_N2 = 28.01 / 1000  # molar mass in kg/mol (applies to all mm's)
mm_CO2 = 44.01 / 1000
mm_H2O = 18.02 / 1000
N2_co = 9
CO2_co = 3
H2O_co = 4

M_bar = ((N2_co * mm_N2) + (CO2_co * mm_CO2) + (H2O_co * mm_H2O)) / (N2_co + CO2_co + H2O_co)
R_gamma = R_u / M_bar

# ---------------------------------------------------------------------------------------------------

# Section 3: Solving for gamma

# equation 1: gamma = (sum n*C_p) / (sum n*C_v)
# equation 2: C_v = C_p - R_gamma
# given: (converted to J/(mol*K))
Cp_N2 = 1.039 * 1000
Cp_CO2 = 0.846 * 1000
Cp_H2O = 1.8723 * 1000
Cv_N2 = Cp_N2 - R_gamma
Cv_CO2 = Cp_CO2 - R_gamma
Cv_H2O = Cp_H2O - R_gamma

gamma_num = (Cp_N2 * N2_co) + (Cp_CO2 * CO2_co) + (Cp_H2O * H2O_co)  # numerator
gamma_denom = (Cv_N2 * N2_co) + (Cv_CO2 * CO2_co) + (Cv_H2O * H2O_co)

gamma = gamma_num / gamma_denom  # no unit

# ---------------------------------------------------------------------------------------------------

# Section 3: Solving for T_o (Flame temp)

# equation 1: T_o = T_i + deltaH_comb / sum (n * Cp)
# equation 2: deltaH_comb = deltaH_sumP - deltaH_sumR
# given:

deltaH_IPA = -272.8 * 1000 # (J/mol) -- applies to all delta H's
deltaH_N2O = 82.05 * 1000
deltaH_N2 = 0
deltaH_CO2 = -393.51 * 1000
deltaH_H2O = -241.82 * 1000

deltaH_prod = (N2_co * deltaH_N2) + (CO2_co * deltaH_CO2) + (H2O_co * deltaH_H2O)
deltaH_reac = deltaH_IPA + (N2_co * deltaH_N2O)
deltaH_comb = deltaH_prod - deltaH_reac

T_i = 298  #initial ambient temp (77 F | 25 C)
T_o = T_i + (deltaH_comb / gamma_num) #stagnation temperature

# ---------------------------------------------------------------------------------------------------

# Section 4: Solving for P_e (exhaust pressure)

# assuming P_e = P_o for idealized case
# given:

P_o = 101.3 * 1000  #atmospheric pressure in Pa
P_e = P_o

# ---------------------------------------------------------------------------------------------------

# Section 5: Solving for V_e (exhaust velocity)

V_e = math.sqrt((2 * gamma / (gamma - 1)) * R_gamma * T_o)

# ---------------------------------------------------------------------------------------------------

# Section 6: Solving for Mass Flow Rates

m_dot = float(F) / V_e

# ---------------------------------------------------------------------------------------------------

# Section 7: Generalized Mass Calculations

#given: (Vol adjustable by tank) #YOU choose propellant amount

Vol_N2O = input("Enter the N2O tank size (L) that you purchased: ") # in liters
Vol_N2O = float(Vol_N2O)
rho_N2O = 1.23 # kg/L
m_oxidizer = rho_N2O*Vol_N2O

OF_ratio = 7 #ideal = 9:1

m_fuel = m_oxidizer / OF_ratio

rho_IPA = 0.786 #kg/L
Vol_IPA = m_fuel / rho_IPA

m_dot_oxidizer = (OF_ratio * m_dot) / (1 + OF_ratio)
m_dot_fuel = m_dot / (1 + OF_ratio)

m_prop_total = m_oxidizer + m_fuel
m_dot_total = m_dot_oxidizer + m_dot_fuel

# ---------------------------------------------------------------------------------------------------

# Section 8: Area Ratio (A/A*)

#equation 1: (1 / Me) * ((2 / (gamma + 1)) * (1 + ((gamma - 1) / 2) * Me**2))**((gamma + 1) / (2 * (gamma - 1)))
# given:

Me = 2.5  # mach number at exhaust

area_ratio = (1 / Me) * ((2 / (gamma + 1)) * (1 + ((gamma - 1) / 2) * Me**2))**((gamma + 1) / (2 * (gamma - 1)))

# ---------------------------------------------------------------------------------------------------

# Section 9: Mass Flow Rate Iterations

# iteration case 1: 100N through 1000N
if 100 <= float(F) <= 1000:
    F_new = float(F)
    F_end = F_new * 10
    F_step = 100

    for i in range(int(F_new), int(F_end), int(F_step)):
        m_dot_new = i / V_e
        #print(f"For Thrust {i} N, Mass Flow Rate: {m_dot_new:.5f} kg/s")

elif 1001 <= float(F) <= 10000:
    F_new = float(F)
    F_end = F_new * 10
    F_step = 500

    for i in range(int(F_new), int(F_end), int(F_step)):
        m_dot_new = i / V_e
        #print(f"For Thrust {i} N, Mass Flow Rate: {m_dot_new:.5f} kg/s")

# ---------------------------------------------------------------------------------------------------

# Section 10: Expected Burn time

# burn time:
t_burn = m_prop_total / m_dot_total

# ---------------------------------------------------------------------------------------------------

# Section 11: Specific Impulse

#specific impulse calc:
I_sp = F / ((m_dot_total) * g_o)

# ---------------------------------------------------------------------------------------------------
# %%
# chamber pressure calculation

P_c = P_e * ( (2 * gamma) / (gamma + 1) ) ** (gamma / (gamma - 1)) * area_ratio 
#rework
# %%
# ---------------------------------------------------------------------------------------------------

print(f"""
IMPORTANT: The following data represents the computed engine performance parameters.

THEORETICAL ROCKET PERFORMANCE ASSUMING EQUILIBRIUM COMPOSITION
***************************************************************

Exhaust Velocity:
    V_e = {V_e:.2f} m/s [Mach {(V_e * 0.00291545):.2f}]

Mass Flow Rates:
    Total Mass Flow Rate, m_dot = {m_dot:.5f} kg/s
    Oxidizer Mass Flow Rate, m_dot_oxidizer = {m_dot_oxidizer:.5f} kg/s
    Fuel Mass Flow Rate, m_dot_fuel = {m_dot_fuel:.5f} kg/s

Area Ratio:
    Exhaust Area Ratio to Throat, Ae/At = {area_ratio:.3f}

Burn Time:
    t_burn = {t_burn:.2f} seconds

Specific Impulse:
    Specific Impulse, I_sp = {I_sp:.2f} seconds

    
Combustion Pressure:
    Combustion Chamber Pressure, P_c = {P_c:.2f} Pa

END OF PERFORMANCE REPORT
***************************************************************
""")
