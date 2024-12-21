# %% Sizing Rocket Engine from Scratch
# by Christian Miranda
# this is for an N2O/IPA rocket

import math
import matplotlib.pyplot

# Desired thrust in Newtons
F = input("Enter desired thrust (N): ")

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
T_o = T_i + (deltaH_comb / gamma_num) #flame temp

# %% 
# Section 4: Solving for P_e (exhaust pressure)
# assuming P_e = P_o for idealized case
P_o = 101.3 * 1000  #atmospheric pressure in Pa
P_e = P_o

# %% 
# Section 5: Solving for V_e (exhaust velocity)
V_e = math.sqrt((2 * gamma / (gamma - 1)) * R_gamma * T_o)
print(f'Exhaust Velocity, V_e = {V_e:.2f} m/s')
print()

# %%

# LOOP BEGINS!

# Section 6: Solving for Mass Flow Rate
m_dot = float(F) / V_e
print(f'Mass flow rate equals {m_dot:.5f} kg/s')
print()

# Section 7: Area Ratio
Me = 2.5  # Mach number at the exhaust

area_ratio = (1 / Me) * ((2 / (gamma + 1)) * (1 + ((gamma - 1) / 2) * Me**2))**((gamma + 1) / (2 * (gamma - 1)))
print(f'Area ratio of the exhaust relative to the throat is {area_ratio:.3f}')
print()


# LOOP ENDS!

# 1 lb-f = 4.448 N

if 100 <= float(F) <= 1000:
    #breh
    F_new = F
    F_end = F*10
    F_step = 100
    
    for i in range(F_new, F_end, F_step):
        m_dot_new = F_new / V_e
        print(m_dot_new)
# elif 1001 < F < 5000:
#     #breh
#     F_new = F
#     F_end = F*5
#     F_step = 450

#     for i in range(F_new, F_end, F_step):
#         m_dot_new = F_new/




# %%




