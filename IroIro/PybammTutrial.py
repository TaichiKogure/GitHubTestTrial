# %%
import pybamm

model = pybamm.lithium_ion.DFN()
sim = pybamm.Simulation(model)
sim.solve([0, 3600])
# sim.plot()

# %%
# models = [
#     pybamm.lithium_ion.SPM(),
#     pybamm.lithium_ion.SPMe(),
#     pybamm.lithium_ion.DFN(),
# ]

# #モデル違いでカーブ形状がどのように変わるかを計算して比較する．

# sims = []
# for model in models:
#     sim = pybamm.Simulation(model)
#     sim.solve([0, 3600])
#     sims.append(sim)
#
# pybamm.dynamic_plot(sims, time_unit="seconds")
#
# model = pybamm.lithium_ion.DFN()
# sim = pybamm.Simulation(model)
# sim.solve([0, 3600])

##見たい部分だけの情報をプロットしてみる．

# model.variable_names()
# model.variables.search("electrolyte")
# output_variables = ["Terminal voltage [V]"]
# sim.plot(output_variables=output_variables)
# output_variables = ["Electrolyte concentration [mol.m-3]", "Terminal voltage [V]"]
# sim.plot(output_variables=output_variables)
# sim.plot([["Electrode current density", "Electrolyte current density"], "Terminal voltage [V]"])


# %%
# yBaMM has a number of in-built parameter sets (check the list here), which can be selected doing
# https://pybamm.readthedocs.io/en/latest/source/parameters/parameter_sets.html
# ここで使うパラメータをえらんでおく 例えば　Chen2020　とか

chemistry = pybamm.parameter_sets.Chen2020

# https://github.com/pybamm-team/PyBaMM/tree/main/pybamm/input/parameters
parameter_values = pybamm.ParameterValues(chemistry=chemistry)
# コンソールからparameter_valuesと打ち込むと設定値が出てくる．

# %%

# or we can search for a particular parameter

parameter_values.search("electrolyte")

# %%
# 電解液のパラメータこんなのはいってた

# import matplotlib.pyplot as plt
# import numpy as np

# c_e = np.linspace(0.01, 30, 100)
# sigma_e = (0.1297 * (c_e / 1000) ** 3 - 2.51 * (c_e / 1000) ** 1.5 + 3.329 * (c_e / 1000))
# D_c_e = 8.794e-11 * (c_e / 1000) ** 2 - 3.972e-10 * (c_e / 1000) + 4.862e-10
# plt.plot(c_e, sigma_e)
# plt.plot(c_e, D_c_e)
# plt.show()

# %%

# To run a simulation with this parameter set, we can proceed
# as usual but passing the parameters as a keyword argument

#model = pybamm.lithium_ion.DFN()
# sim = pybamm.Simulation(model, parameter_values=parameter_values)
# sim.solve([0, 3600])
# sim.plot()

#%%
#You can implement drive cycles importing the dataset and creating an interpolant to pass as the current function.
#データ補完もできるっぽい．運転中の充放電電流カーブをインプットして電圧計算する感じ

import pandas as pd    # needed to read the csv data file

#Import drive cycle from file

drive_cycle = pd.read_csv(r"C:\Users\auror\AppData\Local\Programs\Python\Python39\Lib\site-packages\pybamm\input\drive_cycles\US06.csv", comment="#", header=None).to_numpy()

#バックスラッシュがエスケープシーケンスになるのでｒをいれてキャンセルしてる．または最初C:\\,をいれる/にする．でもいいらしい．

Create interpolant

timescale = parameter_values.evaluate(model.timescale)
current_interpolant = pybamm.Interpolant(drive_cycle[:, 0], drive_cycle[:, 1], timescale * pybamm.t)

#Set drive cycle
parameter_values["Current function [A]"] = current_interpolant

model = pybamm.lithium_ion.SPMe()
sim = pybamm.Simulation(model, parameter_values=parameter_values)
sim.solve()
sim.plot(["Current [A]", "Terminal voltage [V]"])

#%%
# Alternatively, we can define the current to be an arbitrary function of time
import numpy as np

def my_current(t):
    return pybamm.sin(2 * np.pi * t / 60)

parameter_values["Current function [A]"] = my_current

# and we can now solve the model again. In this case, we can pass t_eval
# to the solver to make sure we have enough time points to resolve the function in our output.

model = pybamm.lithium_ion.SPMe()
sim = pybamm.Simulation(model, parameter_values=parameter_values)
t_eval = np.arange(0, 121, 1)
sim.solve(t_eval=t_eval)
sim.plot(["Current [A]", "Terminal voltage [V]"])

# In this notebook we have seen how we can change the parameters of our model.
# In Tutorial 5 we show how can we define and run experiments.

#%%

# Tutorial 5