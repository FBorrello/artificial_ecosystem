import numpy as np
import math
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Define the modified Andrade equation
def modified_andrade_equation(T, A, B, C):
    return A * np.exp(B / (T - C))

# Convert temperatures from Celsius to Kelvin
temperatures_C = np.array([25, 50, 100])
temperatures_K = temperatures_C + 273.15

# Expected viscosities in Pa·s
expected_viscosities = np.array([0.00089, 0.00054, 0.00028])

# Perform curve fitting to find the best-fit values for A, B, and C
popt, pcov = curve_fit(modified_andrade_equation, temperatures_K, expected_viscosities, maxfev=10000000)

# Extract the best-fit values for A, B, and C
A_fit, B_fit, C_fit = popt

print(f"Best-fit values: A = {A_fit}, B = {B_fit}, C = {C_fit}")

# Define a function to calculate viscosity using the fitted constants
def calculate_water_viscosity_fitted(temperature):
    T = temperature + 273.15
    return A_fit * math.exp(B_fit / (T - C_fit))

# Test the function with the given temperatures
viscosities_fitted = {temp: calculate_water_viscosity_fitted(temp) for temp in temperatures_C}

print(viscosities_fitted)

# Plot the results
plt.figure(figsize=(10, 6))
plt.scatter(temperatures_C, expected_viscosities, color='red', label='Expected Viscosities')
plt.plot(temperatures_C, [calculate_water_viscosity_fitted(temp) for temp in temperatures_C], color='blue', label='Fitted Andrade Equation')
plt.xlabel('Temperature (°C)')
plt.ylabel('Viscosity (Pa·s)')
plt.title('Water Viscosity vs Temperature')
plt.legend()
plt.grid(True)
plt.show()
