# Design Document
# by: Christian Miranda

# ---------------------------------------------------------------------------------------------------

# Library Import:
import numpy as np
import scipy as spi
import math
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------------------------------

# Section 1:

g_0 = 9.81
rho = 1
A = 1
v = 1

m_dot_ox = 1
m_dot_fuel = 1
m_dot_total = m_dot_ox + m_dot_fuel

NPSH_a = ((p_inlet / rho*g_0) - h_vap - h_fric)