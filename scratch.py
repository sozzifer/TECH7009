import numpy as np
from scipy.stats import norm


np.random.seed(0)
z1, z2, z3 = np.random.random((3, 7, 7))
customdata = np.dstack((z2, z3))

print(f"z2: {z2}")
print(f"z3: {z3}")
print(customdata)