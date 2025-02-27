# Calculations derived from "Turbopump Retrospective"
# by: Christian Miranda


# Library Import:
import math
import matplotlib.pyplot
import numpy

# ---------------------------------------------------------------------------------------------------

# FOUNDATIONAL ASSUMPTIONS: 

# 1) lol idk if we're assuming certain assumptions w.r.t. thermodynamic system properties
# 2)
# 3)
# 4) 


# ---------------------------------------------------------------------------------------------------

# QUICK REFERENCES

# 1) Page 7 denotes the idealized specific speed to be between [0.1 and 0.6] for centrifugal pumps AND [0.29 and 0.36]
# oxidizers and fuel
# 2) Page 7 also denotes that the ideal eye flow coefficient is between [0.2 and 0.3].

# ---------------------------------------------------------------------------------------------------

# Section 0: Preliminary Equations

# Equations that need to be defined:

# delta_p

# ---------------------------------------------------------------------------------------------------

# Section 1: {Impeller Geometry Equations} | Calculating Specific Speed (Omega_s), Exit Flow Coefficient (Phi_t)
# and Head coefficient (Psi)

# initialization
g_constant = 9.81 # acceleration due to gravity (m/s^2)
omega = 20000 # shaft speed (RPM) -- this value was CHOSEN
delta_p = 1 # change in pressure (Pa) -- define later
Q = 1 # volumetric flow rate (m^3) -- define later

delta_H = delta_p / g_constant # change in fluid head equation (m)
Omega_s = (omega * math.sqrt(Q) / ((g*delta_H)**(3/4))) # specific speed equation (unitless)
phi_t = 0.1715*math.sqrt(Omega_s) # exit flow coefficient equation (unitless)
psi = (0.4 / ((Omega_s)**(1/4))) # Head coefficient equation (unitless)

# ---------------------------------------------------------------------------------------------------

# Section 2: {Profile Curve Equations} | Calculating Eye Radius (r_eye), Exit Radius (r_exit), and Exit Width (w_exit)

# initialization
phi_e = 0.25 # eye flow coefficient (unitless) -- this value was CHOSEN per Section 0 range
r_inner = 1 # inner radius (m) -- define later

r_eye = (Q / (math.pi * omega *phi_e)*(1 - ((r_inner**2) / (r_eye**2)))) # eye radius equation (m) -- use MATLAB solver?
r_exit = ((1/omega)*math.sqrt(g_constant*delta_H/psi)) # exit radius equation (m)
w_exit = (Q / 2*math.pi*omega*(r_exit**2)*phi_e) # exit width (m) 

# ---------------------------------------------------------------------------------------------------

# Section 3: {Blade Curve Equations} | Calculating Inlet Angle (beta_inlet), Combined Hydraulic Efficiency (eta_HY), 
# and Outlet Angle (beta_outlet)

# initialization
b_eye = 1 # inlet width at eye of impeller (m) -- define later
mu = 0.15 # slip factor -- this value was CHOSEN per Section 0 range
U_inlet = ((omega/r_eye)) # tangential velocity at inlet equation (m/s)
V_inlet = ((Q)/(2 * math.pi * r_eye * b_eye)) # axial velocity at inlet equation (m/s)

beta_inlet = math.atan(U_inlet / V_inlet) # inlet angle equation (degrees)
eta_HY = 1 - (0.071 / (Q**0.25)) # jekat's formula (unitless) -- combined hydraulic efficiency
beta_outlet = math.atan((Q / (2*math.pi*r_exit*w_exit)) / (omega*r_exit*(1 - mu) - ((g_constant*delta_p) / (eta_HY * omega * r_exit))))
# outlet angle equation (degrees)

# ---------------------------------------------------------------------------------------------------

# Section 4: {Inducer Geometry Equations} | Calculating Net Positive Suction Head [Shockless Entry] (NPSH_se), 
# Suction Specific Speed (S_s), Optimal Flow Coefficient (phi_opt), and Optimal Inducer Tip Radius (r_tip)

# initialization
ang_vel = 1 # angular velocity (m/s) -- uhhh not sure how he got this value
n = omega # rotational speed of inducer (RPM) -- assuming the shaft and inducer are at the same RPM??
v = 1 # hub to tip ratio (unitless) -- this value was CHOSEN per Section 0 range
alpha_lil = 1 # flow incidence angle -- idk how to find this lol
beta_lil = 1 # blade angle -- wtf????? another transcendent equation or am i dumb??????
r = 1 # radius of inducer (m) -- maybe???????
sigma = 2.5 # solidity (unitless) -- this value was CHOSEN per Section 0 range
N = 6 # number of blades (unitless, obv) -- this value was CHOSEN per Section 0 range

beta_blade = alpha_lil / beta_lil # blade angle (degrees)
NPSH_se = (1.2*(phi_e**2) + (0.2334 + ((ang_vel*r) / 128.3)**4)*((phi_e**2)+1)) # net positive suction head equation (m)
S_s = ((n*Q)**(1/2) / (NPSH_se)**(3/4)) # suction specific speed equation (unitless)
phi_opt = (1.3077 * math.sqrt(1 - (v**2)) / (1 + (1/2)*math.sqrt(1 + 10.261*(1 - (v**2)) / S_s))) # optimal flow coefficient (unitless)
r_tip = ((1.449)*((Q) / (1 - (v**2)*omega*phi_opt))) # tip radius (m)
alpha = (2*math.pi*r*math.tan(beta_blade)) # blade lead (m) -- distance a blade advances per turn
h_min = (((alpha*sigma)/N)*math.sin(beta_blade)) # minimum required length of inducer (m)

# ---------------------------------------------------------------------------------------------------

# Section 5: {Volute Geometry Equations} | Calculating Total Head Change

# initialization
delta_h_s = 1 # static head (m) -- define later
phi = 1 # flow coefficient (unitless) -- define later?
delta_h_v = 1 # velocity head term -- define later
phi_el = 1 # expansion energy loss (units?) -- define later
c_i = 1 # incidence angle loss coefficient (unitless) -- define later
c_m = 1 # mach-number coefficient (unitless) -- define later

psi_ke = math.sqrt((2*(phi_el**2)-1)) # kinetic energy loss coefficient (unitless) -- define later
delta_h_es = (delta_h_s * (phi**2)) # static head change equation (m)
delta_h_ev = (delta_h_v * (psi_ke**2) * c_i * c_m) # velocity head change equation (m)
delta_h_e = delta_h_es + delta_h_ev # total head change euqation (m)