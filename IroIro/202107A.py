#%%
import numpy as np
x = ((np.arange(10100)))/10E5
print(x)

#%%
import pybamm
model = pybamm.lithium_ion.DFN()
sim = pybamm.Simulation(model)
sim.solve([0,7200])
sim.plot()

#%%
