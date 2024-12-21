# %% Sizing Rocket Engine from Scratch
# by Christian Miranda
# this is for an N2O/IPA rocket

import math
import matplotlib.pyplot

# Desired thrust in Newtons
F = input("Enter desired thrust (N): ")
F = float(F)
g_o = 9.81 # acceleration due to gravity (m/s^2)
#O/F ratio:
#by the stoichiometry, ideal O/F ratio is 9:1. so right now im assuming fuel rich is better therefore 7:1...
OF_ratio = 7

#propellant mass calculation:
#given: (Vol adjustable by tank) #YOU choose propellant amount.
Vol_N2O = input("Enter the N2O tank size (L) that you purchased: ") # in liters
Vol_N2O = float(Vol_N2O)
rho_N2O = 1.23 # kg/L
m_oxidizer = rho_N2O*Vol_N2O

# 128 oz of IPA easily sourcable
# switching to a O/F driving model
m_fuel = m_oxidizer / OF_ratio
rho_IPA = 0.786 #kg/L

Vol_IPA = m_fuel / rho_IPA
# Vol_IPA = math.ceil(Vol_IPA)

# Vol_IPA = input("Enter the IPA tank size (L) that you purchased: ") #in liters
# Vol_IPA = float(Vol_IPA)
# rho_IPA = 0.786 #kg/L
# m_fuel = rho_IPA*Vol_IPA

# %% 
# Section 1: Solving for R_gamma
# equation: R_gamma = R_u / M_bar
# chemical formula for N2O/IPA reaction:
# C3H8O (l) + 9 N2O (g) -> 9 N2 (g) + 3 CO2 (g) + 4 H2O (g)

# given:
R_u = 8.314  # universal gas constant (J/(mol*K))
mm_N2 = 28.01 / 1000  # molar mass in kg/mol
mm_CO2 = 44.01 / 1000
mm_H2O = 18.02 / 1000

N2_co = 9
CO2_co = 3
H2O_co = 4

# calc
M_bar = ((N2_co * mm_N2) + (CO2_co * mm_CO2) + (H2O_co * mm_H2O)) / (N2_co + CO2_co + H2O_co)
R_gamma = R_u / M_bar

# %% 
# Section 2: Solving for gamma

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

gamma = gamma_num / gamma_denom  # no unit!

# %% 
# Section 3: Solving for T_o (Flame temp)
# equation 1: T_o = T_i + deltaH_comb / sum (n * Cp)
# equation 2: deltaH_comb = deltaH_sumP - deltaH_sumR

# given: (J/mol)
deltaH_IPA = -272.8 * 1000
deltaH_N2O = 82.05 * 1000
deltaH_N2 = 0
deltaH_CO2 = -393.51 * 1000
deltaH_H2O = -241.82 * 1000

deltaH_prod = (N2_co * deltaH_N2) + (CO2_co * deltaH_CO2) + (H2O_co * deltaH_H2O)
deltaH_reac = deltaH_IPA + (N2_co * deltaH_N2O)
deltaH_comb = deltaH_prod - deltaH_reac

T_i = 298.15  #initial ambient temp (77 F | 25 C)
T_o = T_i + (deltaH_comb / gamma_num) #stagnation temperature

# %% 
# Section 4: Solving for P_e (exhaust pressure)
# assuming P_e = P_o for idealized case
P_o = 101.3 * 1000  #atmospheric pressure in Pa
P_e = P_o

# %% 
# Section 5: Solving for V_e (exhaust velocity)
V_e = math.sqrt((2 * gamma / (gamma - 1)) * R_gamma * T_o)

# %%

# LOOP BEGINS! ----------------------------------

# Section 6: Solving for Mass Flow Rate
m_dot = float(F) / V_e

# Section 7: Area Ratio (A/A*)
#equation 1: (1 / Me) * ((2 / (gamma + 1)) * (1 + ((gamma - 1) / 2) * Me**2))**((gamma + 1) / (2 * (gamma - 1)))

#given:
Me = 2.5  # mach number at exhaust

area_ratio = (1 / Me) * ((2 / (gamma + 1)) * (1 + ((gamma - 1) / 2) * Me**2))**((gamma + 1) / (2 * (gamma - 1)))

# LOOP ENDS! ------------------------------------

# # 1 lb-f = 4.448 N

# if 100 <= float(F) <= 1000:
#     F_new = float(F)
#     F_end = F_new * 10
#     F_step = 100

#     # iteration
#     for i in range(int(F_new), int(F_end), int(F_step)):
#         m_dot_new = i / V_e
#         print(f"For Thrust {i} N, Mass Flow Rate: {m_dot_new:.5f} kg/s")

# elif 1001 <= float(F) <= 10000:
#     F_new = float(F)
#     F_end = F_new * 10
#     F_step = 500

#     for i in range(int(F_new), int(F_end), int(F_step)):
#         m_dot_new = i / V_e
#         print(f"For Thrust {i} N, Mass Flow Rate: {m_dot_new:.5f} kg/s")

# 





# #propellant mass calculation:
# #given: (Vol adjustable by tank) #YOU choose propellant amount.
# Vol_N2O = input("Enter the N2O tank size (L) that you purchased: ") # in liters
# rho_N2O = 1.23 # kg/L
# m_oxidizer = rho_N2O*Vol_N2O
# print(f'The estimated N2O propellant mass required from the tank size you purchased is {m_oxidizer:.2f} kg')
# print()

# # 128 oz of IPA easily sourcable
# Vol_IPA = input("Enter the IPA tank size (L) that you purchased: ") #in liters
# rho_IPA = 0.786 #kg/L
# m_fuel = rho_IPA*Vol_IPA
# print(f'The estimated IPA propellant mass required from the tank size you purchased is {m_fuel:.2f} kg')
1
# #O/F ratio:
# #by the stoichiometry, ideal O/F ratio is 9:1. so right now im assuming fuel rich is better therefore 7:1...
# OF_ratio = 7

m_dot_oxidizer = (OF_ratio * m_dot) / (1 + OF_ratio)
m_dot_fuel = m_dot / (1 + OF_ratio)

#mass calcs
m_prop_total = m_oxidizer + m_fuel
m_dot_total = m_dot_oxidizer + m_dot_fuel

# burn time:
t_burn = m_prop_total / m_dot_total

#specific impulse calc:
I_sp = F / ((m_dot_total) * g_o)


######################################
# all prints here:

#exhaust velocity print

# print(f'Exhaust Velocity, V_e = {V_e:.2f} m/s [Mach {(V_e * 0.00291545):.2f}]')
# print()

# #exhaust velocity print
# print(f'Total Mass flow rate equals {m_dot:.5f} kg/s')
# print()

# print(f'Area ratio of the exhaust relative to the throat is {area_ratio:.3f}')
# print()

# print(f'The expected mass flow rate for the oxidizer is {m_dot_oxidizer:.5f} in kg/s')
# print()

# print(f'The expected mass flow rate for the fuel is  {m_dot_fuel:.5f} in kg/s')
# print()

# print(f'The expected burn time for this engine is {t_burn:.2f} seconds')
# print()

# print(f'The expected Specific Impulse for this engine is {I_sp:.2f} seconds')

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

Performance Parameters:
    Specific Impulse, I_sp = {I_sp:.2f} seconds

END OF PERFORMANCE REPORT
***************************************************************
""")