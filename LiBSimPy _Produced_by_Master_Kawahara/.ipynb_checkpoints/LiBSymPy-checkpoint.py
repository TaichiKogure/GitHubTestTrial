import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import fsolve


class CellDesign():

    # def __init__(self,x_p_s, x_p_e):
    #    self.x_p_s = x_p_s
    #    self.x_p_e = x_p_e

    def __init__(self):
        self.new_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                           '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                           '#bcbd22', '#17becf']

    def set_param_dict(self):
        dict_param = dict(C_rate=0.8)

        dict_param.update(x_p_s=0.2)
        dict_param.update(x_p_e=0.99)
        dict_param.update(x_n_s=0.17)
        dict_param.update(x_n_e=0.94)

        # Time delta
        dict_param.update(dt=0.1)  # [sec]

        # Temperature
        dict_param.update(T=298)  # [K]

        # Constant
        dict_param.update(R=8.3144598)  # [J/(mol K)]
        dict_param.update(F=96485.33289)  # [C/mol]
        dict_param.update(z=1)
        dict_param.update(alpha=0.5)

        dict_param.update(k_o_p=2.344E-11)  # 7.13E-8
        dict_param.update(k_o_n=5.0307E-11)  # 1.47E-7
        dict_param.update(C_e_0=1000)  # [mol/m3]
        dict_param.update(C_s_max_p=2.39E4)  # [mol/m3]
        dict_param.update(C_s_max_n=1.61E4)  # [mol/m3]

        dict_param.update(epsilon_e=0.724)
        dict_param.update(brugg_e=4)

        # Area Dimension
        dict_param.update(S_Al=100E-6 * 150E-6)  # [m2]
        dict_param.update(S_Cu=100E-6 * 200E-6)  # [m2]
        dict_param.update(S_el=150E-6 * 150E-6)  # [m2]
        dict_param.update(S_p=10 * 100E-6 * 100E-6)  # [m2]
        dict_param.update(S_n=10 * 100E-6 * 100E-6)  # [m2]

        # Cathode Dimension
        dict_param.update(L_Al=100E-6)  # [m]
        dict_param.update(L_p=50E-6)  # [m]
        dict_param.update(X_p=40E-6)  # [m]

        # Electrolyte Dimension
        dict_param.update(L_el=10E-6)  # [m]

        # Anode Dimension
        dict_param.update(L_Cu=100E-6)  # [m]
        dict_param.update(X_n=40E-6)  # [m]

        # Charge or Discharge
        # Condition = 'Discharge'
        # if Condition == 'Charge':
        # I = abs(I)*(-1)

        # Diffusion coefficient
        dict_param.update(D_p=0.5E-11)  # [m2/s]
        dict_param.update(D_n=1.0E-11)  # [m2/s]

        # Li ion concentration in Liquid phase (Electrolyte)
        dict_param.update(epsilon=1)
        dict_param.update(Deff=7.5E-12 * 0.5)  # [m2/sec]
        dict_param.update(t_plus=0.363)

        # resistivity at 294.15K (20deg.C)
        dict_param.update(rho_0_Al=2.82E-8)  # [ohm m]
        dict_param.update(rho_0_Cu=1.68E-8)  # [ohm m]
        dict_param.update(alpha_Al=0.0039)  # [/K]
        dict_param.update(alpha_Cu=0.003862)  # [/K]

        # electronic resistance of conductive agent per 1m
        dict_param.update(R_s_p=1E10)  # [ohm m] Temporary number
        dict_param.update(R_s_n=5E9)  # [ohm m] Temporary number

        # Memo
        # C = C/sec sec = A sec
        # C*60*60 = Ah

        return dict_param

    def update_param_dict(self, df_cell, dict_param):

        # Constant
        dict_param.update(C_s_p_0=dict_param["C_s_max_p"] * df_cell['Cathode x (-)'][0])
        dict_param.update(C_s_n_0=dict_param["C_s_max_n"] * (1 - df_cell['Anode x (-)'][0]))

        # Cathode Dimension
        dict_param.update(V_p=3 / 4 * np.pi * dict_param["L_p"] ** 3)  # [m3]

        # Anode Dimension
        dict_param.update(
            V_n=(((max(df_cell['Cathode x (-)'])
                   - min(df_cell['Cathode x (-)'])) * dict_param["C_s_max_p"] * dict_param["V_p"] * dict_param["F"])
                 / ((max(df_cell['Anode x (-)']) - min(df_cell['Anode x (-)'])) * dict_param["C_s_max_n"] * dict_param[
                        "F"])))
        dict_param.update(L_n=(dict_param["V_n"] * 4 / 3 / np.pi) ** (1 / 3))  # [m]

        # 1C Current per one particle
        dict_param.update(
            I_1C=abs((max(df_cell['Cathode x (-)'])
                      - min(df_cell['Cathode x (-)'])) * dict_param["C_s_max_p"]
                     * dict_param["V_p"] * dict_param["F"] / 60 / 60))  # [A = C/sec]

        # xC Current density
        dict_param.update(I=dict_param["C_rate"] * dict_param["I_1C"] * 5)  # [A = C/sec] 5 particles

        # Discharge time
        dict_param.update(t_total=dict_param["I_1C"] / dict_param["I"] * 60 * 60 * 5)  # [sec] 5 particles

        return dict_param

    def kappa_e(C_el, epsilon_e, brugg_e):
        return epsilon_e ** brugg_e * (4.1253 * 1E-2 + 5.007 * 1E-4 * C_el - 4.7212 * 1E-7 * C_el ** 2
                                       + 1.5094 * 1E-10 * C_el ** 3 - 1.6018 * 1E-14 * C_el ** 4)

    def smooth(df, delta):

        df_tmp = np.zeros((2 * delta, len(df)))
        for i in range(delta):
            df_tmp[(i - 1), :] = np.roll(df, i)
            df_tmp[(i - 1 + delta), :] = np.roll(df, -i)
        df_tmp2 = np.median(df_tmp, axis=0)
        df_tmp2[:delta] = np.nan
        df_tmp2[-delta:] = np.nan
        return df_tmp2

    def DOD_norm2(df, x_s, x_e):
        return (df - x_s) * 100 / (x_e - x_s)

    def re_DOD_norm2(df, x_s, x_e):
        return df * (x_e - x_s) / 100 + x_s

    def dQdV(df_x, df_y, delta):

        dQ = abs(np.roll(df_x, delta) - np.roll(df_x, -delta))
        dV = abs(np.roll(df_y, delta) - np.roll(df_y, -delta))
        dQ = np.where(dQ <= 0, np.nan, dQ)
        df_dQdV = dV / dQ
        df_dQdV[:delta] = np.nan
        df_dQdV[-delta:] = np.nan
        return df_dQdV

    def ocv_cathode(self, x_p_s, x_p_e):

        # df_LCO_OCV = pd.read_csv('OCV_curves/LCO_OCV1.csv')
        df_LCO_OCV = pd.read_csv('LCO_OCV1.csv')
        df_LCO_OCV.columns = ['x', 'Potential(V)']
        df_LCO_OCV = df_LCO_OCV.sort_values(by=['x'], ascending=False)
        df_LCO_OCV = df_LCO_OCV.reset_index(drop=True)
        df_LCO_OCV['x'] = 1 - df_LCO_OCV['x']
        df_LCO_OCV['x'] = CellDesign.smooth(df_LCO_OCV['x'], 20)
        df_LCO_OCV['Potential(V)'] = CellDesign.smooth(df_LCO_OCV['Potential(V)'], 20)
        df_LCO_OCV = df_LCO_OCV.dropna()
        df_LCO_OCV = df_LCO_OCV.sort_values(by=['x'], ascending=True)
        df_LCO_OCV['DOD'] = CellDesign.DOD_norm2(df_LCO_OCV['x'], x_p_s, x_p_e)
        return df_LCO_OCV

    def ocv_anode(self, x_n_s, x_n_e):

        # df_LiC6_OCV = pd.read_csv('OCV_curves/LiC6_OCV1.csv')
        df_LiC6_OCV = pd.read_csv('LiC6_OCV1.csv')
        df_LiC6_OCV.columns = ['x', 'Potential(V)']
        df_LiC6_OCV = df_LiC6_OCV.sort_values(by=['x'], ascending=False)
        df_LiC6_OCV = df_LiC6_OCV.reset_index(drop=True)
        df_LiC6_OCV['x'] = 1 - df_LiC6_OCV['x']
        df_LiC6_OCV['x'] = CellDesign.smooth(df_LiC6_OCV['x'], 10)
        df_LiC6_OCV['Potential(V)'] = CellDesign.smooth(df_LiC6_OCV['Potential(V)'], 10)
        df_LiC6_OCV = df_LiC6_OCV.dropna()
        df_LiC6_OCV = df_LiC6_OCV.sort_values(by=['x'], ascending=True)
        df_LiC6_OCV['DOD'] = CellDesign.DOD_norm2(df_LiC6_OCV['x'], x_n_s, x_n_e)

        return df_LiC6_OCV

    def ocv_cell(self, df_LCO_OCV, df_LiC6_OCV):

        df_cell = pd.DataFrame(np.arange(1001)) / 10
        df_cell.columns = ['DOD']
        df_cell = pd.merge_asof(df_cell, df_LCO_OCV, on='DOD', direction='nearest')
        df_cell = pd.merge_asof(df_cell, df_LiC6_OCV, on='DOD', direction='nearest')
        df_cell.columns = ['DOD', 'Cathode x (-)', 'Cathode OCV (V)', 'Anode x (-)', 'Anode OCV (V)']
        df_cell['Cell OCV (V)'] = (df_cell['Cathode OCV (V)'] - df_cell['Anode OCV (V)'])

        return df_cell

    def plot_ocv_curves(self, df_cell, x_p_s, x_p_e, x_n_s, x_n_e):

        fig, (ax1, ax3) = plt.subplots(1, 2, figsize=(16, 5))
        plt.subplots_adjust(wspace=0.25)
        ax2 = ax1.twinx()
        ax1.plot(df_cell['DOD'], df_cell['Cathode OCV (V)'], color=self.new_colors[1])
        ax1.plot(df_cell['DOD'], df_cell['Cell OCV (V)'], color=self.new_colors[0])
        ax1.set_ylabel('Cell voltage, Cathode potential (V)')
        ax2.plot(df_cell['DOD'], df_cell['Anode OCV (V)'], color=self.new_colors[2])
        ax2.set_ylabel('Anode potential (V)')
        ax1.set_xlabel('DOD')

        ax1.set_ylim([3, 4.6])
        ax2.set_ylim([0, 1.6])
        ax1.grid()

        ax1.set_xlim([0, 100])
        ax4 = ax1.twiny()
        ax4.xaxis.set_ticks_position("bottom")
        ax4.xaxis.set_label_position("bottom")
        ax4.spines["bottom"].set_position(("axes", -0.15))

        ax4.set_frame_on(True)
        ax4.patch.set_visible(False)
        ax4.spines["bottom"].set_visible(True)
        ax4.set_xticks([0, 20, 40, 60, 80, 100])
        ax4.set_xticklabels(CellDesign.re_DOD_norm2(np.array([0, 20, 40, 60, 80, 100]), x_n_s, x_n_e))
        ax4.set_xlabel("x of $Li_{1-x}C_6$")

        ax5 = ax1.twiny()
        ax5.xaxis.set_ticks_position("top")
        ax5.xaxis.set_label_position("top")
        ax5.spines["top"].set_position(("axes", +1.05))

        ax5.set_frame_on(True)
        ax5.patch.set_visible(False)
        ax5.spines["top"].set_visible(True)
        ax5.set_xticks([0, 20, 40, 60, 80, 100])
        ax5.set_xticklabels(np.round(CellDesign.re_DOD_norm2(np.array([0, 20, 40, 60, 80, 100]), x_p_s, x_p_e), 3))
        ax5.set_xlabel("x of $Li_{x}CoO_2$")

        ax3.plot(df_cell['DOD'], CellDesign.dQdV(df_cell['DOD'], df_cell['Cathode OCV (V)'], 10),
                 color=self.new_colors[1])
        ax3.plot(df_cell['DOD'], CellDesign.dQdV(df_cell['DOD'], df_cell['Anode OCV (V)'], 10),
                 color=self.new_colors[2])
        ax3.plot(df_cell['DOD'], CellDesign.dQdV(df_cell['DOD'], df_cell['Cell OCV (V)'], 10), color=self.new_colors[0])

        ax3.set_ylabel('dVdQ (V/%)')
        ax3.set_xlabel('DOD (%)')

        ax3.set_ylim([0, 0.05])
        ax3.grid(which='both')

        ax3.set_xlim([0, 100])
        ax6 = ax3.twiny()
        ax6.xaxis.set_ticks_position("bottom")
        ax6.xaxis.set_label_position("bottom")
        ax6.spines["bottom"].set_position(("axes", -0.15))

        ax6.set_frame_on(True)
        ax6.patch.set_visible(False)
        ax6.spines["bottom"].set_visible(True)
        ax6.set_xticks([0, 20, 40, 60, 80, 100])
        ax6.set_xticklabels(CellDesign.re_DOD_norm2(np.array([0, 20, 40, 60, 80, 100]), x_n_s, x_n_e))
        ax6.set_xlabel("x of $Li_{1-x}C_6$")

        ax7 = ax3.twiny()
        ax7.xaxis.set_ticks_position("top")
        ax7.xaxis.set_label_position("top")
        ax7.spines["top"].set_position(("axes", +1.05))

        ax7.set_frame_on(True)
        ax7.patch.set_visible(False)
        ax7.spines["top"].set_visible(True)
        ax7.set_xticks([0, 20, 40, 60, 80, 100])
        ax7.set_xticklabels(np.round(CellDesign.re_DOD_norm2(np.array([0, 20, 40, 60, 80, 100]), x_p_s, x_p_e), 3))
        ax7.set_xlabel("x of $Li_{x}CoO_2$")

        plt.show()

    def init_df_sim(self, dict_param, df_cell, tt=0):

        t = np.arange(0, dict_param["t_total"] + dict_param["dt"], dict_param["dt"])

        # Preparation of dataframe to store result of simulation.

        df_sim = pd.DataFrame(t)
        df_sim.columns = ['Time (sec)']

        # Cathode
        df_sim = df_sim.assign(U_p1=np.nan)
        df_sim = df_sim.assign(C_el_p1=np.nan)
        df_sim = df_sim.assign(C_s_p1_surface=np.nan)
        df_sim = df_sim.assign(I_p1=np.nan)
        df_sim = df_sim.assign(DV_eta_p1=np.nan)
        df_sim = df_sim.assign(Dphi_sp10=np.nan)
        # df_sim = df_sim.assign(Dphi_elp10 = np.nan)
        df_sim = df_sim.assign(Dphi_elp1=np.nan)

        df_sim = df_sim.assign(U_p2=np.nan)
        df_sim = df_sim.assign(C_el_p2=np.nan)
        df_sim = df_sim.assign(C_s_p2_surface=np.nan)
        df_sim = df_sim.assign(I_p2=np.nan)
        df_sim = df_sim.assign(DV_eta_p2=np.nan)
        df_sim = df_sim.assign(Dphi_sp21=np.nan)
        df_sim = df_sim.assign(Dphi_elp21=np.nan)
        df_sim = df_sim.assign(Dphi_elp2=np.nan)

        df_sim = df_sim.assign(U_p3=np.nan)
        df_sim = df_sim.assign(C_el_p3=np.nan)
        df_sim = df_sim.assign(C_s_p3_surface=np.nan)
        df_sim = df_sim.assign(I_p3=np.nan)
        df_sim = df_sim.assign(DV_eta_p3=np.nan)
        df_sim = df_sim.assign(Dphi_sp32=np.nan)
        df_sim = df_sim.assign(Dphi_elp32=np.nan)
        df_sim = df_sim.assign(Dphi_elp3=np.nan)

        df_sim = df_sim.assign(U_p4=np.nan)
        df_sim = df_sim.assign(C_el_p4=np.nan)
        df_sim = df_sim.assign(C_s_p4_surface=np.nan)
        df_sim = df_sim.assign(I_p4=np.nan)
        df_sim = df_sim.assign(DV_eta_p4=np.nan)
        df_sim = df_sim.assign(Dphi_sp43=np.nan)
        df_sim = df_sim.assign(Dphi_elp43=np.nan)
        df_sim = df_sim.assign(Dphi_elp4=np.nan)

        df_sim = df_sim.assign(U_p5=np.nan)
        df_sim = df_sim.assign(C_el_p5=np.nan)
        df_sim = df_sim.assign(C_s_p5_surface=np.nan)
        df_sim = df_sim.assign(I_p5=np.nan)
        df_sim = df_sim.assign(DV_eta_p5=np.nan)
        df_sim = df_sim.assign(Dphi_sp54=np.nan)
        df_sim = df_sim.assign(Dphi_elp54=np.nan)
        df_sim = df_sim.assign(Dphi_elp5=np.nan)

        df_sim = df_sim.assign(Dphi_elpB5=np.nan)

        df_sim = df_sim.assign(Dphi_elp=np.nan)
        df_sim = df_sim.assign(DV_Al=np.nan)

        df_sim["U_p1"][tt] = df_cell['Cathode OCV (V)'][0]
        df_sim["C_el_p1"][tt] = dict_param["C_e_0"]
        df_sim["C_s_p1_surface"][tt] = dict_param["C_s_p_0"]
        df_sim["I_p1"][tt] = 0
        df_sim["DV_eta_p1"][tt] = 0
        df_sim["Dphi_sp10"][tt] = 0
        # df_sim["Dphi_elp10"][tt] = 0
        df_sim["Dphi_elp1"][tt] = 0

        df_sim["U_p2"][tt] = df_cell['Cathode OCV (V)'][0]
        df_sim["C_el_p2"][tt] = dict_param["C_e_0"]
        df_sim["C_s_p2_surface"][tt] = dict_param["C_s_p_0"]
        df_sim["I_p2"][tt] = 0
        df_sim["DV_eta_p2"][tt] = 0
        df_sim["Dphi_sp21"][tt] = 0
        df_sim["Dphi_elp21"][tt] = 0
        df_sim["Dphi_elp2"][tt] = 0

        df_sim["U_p3"][tt] = df_cell['Cathode OCV (V)'][0]
        df_sim["C_el_p3"][tt] = dict_param["C_e_0"]
        df_sim["C_s_p3_surface"][tt] = dict_param["C_s_p_0"]
        df_sim["I_p3"][tt] = 0
        df_sim["DV_eta_p3"][tt] = 0
        df_sim["Dphi_sp32"][tt] = 0
        df_sim["Dphi_elp32"][tt] = 0
        df_sim["Dphi_elp3"][tt] = 0

        df_sim["U_p4"][tt] = df_cell['Cathode OCV (V)'][0]
        df_sim["C_el_p4"][tt] = dict_param["C_e_0"]
        df_sim["C_s_p4_surface"][tt] = dict_param["C_s_p_0"]
        df_sim["I_p4"][tt] = 0
        df_sim["DV_eta_p4"][tt] = 0
        df_sim["Dphi_sp43"][tt] = 0
        df_sim["Dphi_elp43"][tt] = 0
        df_sim["Dphi_elp4"][tt] = 0

        df_sim["U_p5"][tt] = df_cell['Cathode OCV (V)'][0]
        df_sim["C_el_p5"][tt] = dict_param["C_e_0"]
        df_sim["C_s_p5_surface"][tt] = dict_param["C_s_p_0"]
        df_sim["I_p5"][tt] = 0
        df_sim["DV_eta_p5"][tt] = 0
        df_sim["Dphi_sp54"][tt] = 0
        df_sim["Dphi_elp54"][tt] = 0
        df_sim["Dphi_elp5"][tt] = 0

        df_sim["Dphi_elpB5"][tt] = 0

        df_sim["Dphi_elp"][tt] = df_cell['Cathode OCV (V)'][0]
        df_sim["DV_Al"][tt] = 0

        # Anode
        df_sim = df_sim.assign(U_n1=np.nan)
        df_sim = df_sim.assign(C_el_n1=np.nan)
        df_sim = df_sim.assign(C_s_n1_surface=np.nan)
        df_sim = df_sim.assign(I_n1=np.nan)
        df_sim = df_sim.assign(DV_eta_n1=np.nan)
        df_sim = df_sim.assign(Dphi_sn10=np.nan)
        # df_sim = df_sim.assign(Dphi_eln10 = np.nan)
        df_sim = df_sim.assign(Dphi_eln1=np.nan)

        df_sim = df_sim.assign(U_n2=np.nan)
        df_sim = df_sim.assign(C_el_n2=np.nan)
        df_sim = df_sim.assign(C_s_n2_surface=np.nan)
        df_sim = df_sim.assign(I_n2=np.nan)
        df_sim = df_sim.assign(DV_eta_n2=np.nan)
        df_sim = df_sim.assign(Dphi_sn21=np.nan)
        df_sim = df_sim.assign(Dphi_eln21=np.nan)
        df_sim = df_sim.assign(Dphi_eln2=np.nan)

        df_sim = df_sim.assign(U_n3=np.nan)
        df_sim = df_sim.assign(C_el_n3=np.nan)
        df_sim = df_sim.assign(C_s_n3_surface=np.nan)
        df_sim = df_sim.assign(I_n3=np.nan)
        df_sim = df_sim.assign(DV_eta_n3=np.nan)
        df_sim = df_sim.assign(Dphi_sn32=np.nan)
        df_sim = df_sim.assign(Dphi_eln32=np.nan)
        df_sim = df_sim.assign(Dphi_eln3=np.nan)

        df_sim = df_sim.assign(U_n4=np.nan)
        df_sim = df_sim.assign(C_el_n4=np.nan)
        df_sim = df_sim.assign(C_s_n4_surface=np.nan)
        df_sim = df_sim.assign(I_n4=np.nan)
        df_sim = df_sim.assign(DV_eta_n4=np.nan)
        df_sim = df_sim.assign(Dphi_sn43=np.nan)
        df_sim = df_sim.assign(Dphi_eln43=np.nan)
        df_sim = df_sim.assign(Dphi_eln4=np.nan)

        df_sim = df_sim.assign(U_n5=np.nan)
        df_sim = df_sim.assign(C_el_n5=np.nan)
        df_sim = df_sim.assign(C_s_n5_surface=np.nan)
        df_sim = df_sim.assign(I_n5=np.nan)
        df_sim = df_sim.assign(DV_eta_n5=np.nan)
        df_sim = df_sim.assign(Dphi_sn54=np.nan)
        df_sim = df_sim.assign(Dphi_eln54=np.nan)
        df_sim = df_sim.assign(Dphi_eln5=np.nan)

        df_sim = df_sim.assign(Dphi_elnB5=np.nan)

        df_sim = df_sim.assign(Dphi_eln=np.nan)
        df_sim = df_sim.assign(DV_Cu=np.nan)

        df_sim["U_n1"][tt] = df_cell['Anode OCV (V)'][0]
        df_sim["C_el_n1"][tt] = dict_param["C_e_0"]
        df_sim["C_s_n1_surface"][tt] = dict_param["C_s_n_0"]
        df_sim["I_n1"][tt] = 0
        df_sim["DV_eta_n1"][tt] = 0
        df_sim["Dphi_sn10"][tt] = 0
        # df_sim["Dphi_eln10"][tt] = 0
        df_sim["Dphi_eln1"][tt] = 0

        df_sim["U_n2"][tt] = df_cell['Anode OCV (V)'][0]
        df_sim["C_el_n2"][tt] = dict_param["C_e_0"]
        df_sim["C_s_n2_surface"][tt] = dict_param["C_s_n_0"]
        df_sim["I_n2"][tt] = 0
        df_sim["DV_eta_n2"][tt] = 0
        df_sim["Dphi_sn21"][tt] = 0
        df_sim["Dphi_eln21"][tt] = 0
        df_sim["Dphi_eln2"][tt] = 0

        df_sim["U_n3"][tt] = df_cell['Anode OCV (V)'][0]
        df_sim["C_el_n3"][tt] = dict_param["C_e_0"]
        df_sim["C_s_n3_surface"][tt] = dict_param["C_s_n_0"]
        df_sim["I_n3"][tt] = 0
        df_sim["DV_eta_n3"][tt] = 0
        df_sim["Dphi_sn32"][tt] = 0
        df_sim["Dphi_eln32"][tt] = 0
        df_sim["Dphi_eln3"][tt] = 0

        df_sim["U_n4"][tt] = df_cell['Anode OCV (V)'][0]
        df_sim["C_el_n4"][tt] = dict_param["C_e_0"]
        df_sim["C_s_n4_surface"][tt] = dict_param["C_s_n_0"]
        df_sim["I_n4"][tt] = 0
        df_sim["DV_eta_n4"][tt] = 0
        df_sim["Dphi_sn43"][tt] = 0
        df_sim["Dphi_eln43"][tt] = 0
        df_sim["Dphi_eln4"][tt] = 0

        df_sim["U_n5"][tt] = df_cell['Anode OCV (V)'][0]
        df_sim["C_el_n5"][tt] = dict_param["C_e_0"]
        df_sim["C_s_n5_surface"][tt] = dict_param["C_s_n_0"]
        df_sim["I_n5"][tt] = 0
        df_sim["DV_eta_n5"][tt] = 0
        df_sim["Dphi_sn54"][tt] = 0
        df_sim["Dphi_eln54"][tt] = 0
        df_sim["Dphi_eln5"][tt] = 0

        df_sim["Dphi_elnB5"][tt] = 0

        df_sim["Dphi_eln"][tt] = df_cell['Anode OCV (V)'][0]
        df_sim["DV_Cu"][tt] = 0

        return df_sim

    def update_DV_foil(self, df_sim, dict_param, tt):
        df_sim["DV_Al"][tt] = -1 * (dict_param["rho_0_Al"]
                                    * (1 + dict_param["alpha_Al"] * (dict_param["T"] - 296.15))
                                    * dict_param["L_Al"] / dict_param["S_Al"] * dict_param["I"])
        df_sim["DV_Cu"][tt] = 1 * (dict_param["rho_0_Cu"]
                                   * (1 + dict_param["alpha_Cu"] * (dict_param["T"] - 296.15))
                                   * dict_param["L_Cu"] / dict_param["S_Cu"] * dict_param["I"])
        return df_sim

    def update_DV_eta_pn(self, df_sim, dict_param, df_el_blk_sim, df_DVel_blk_sim, tt, electrode_id):

        S_pn = dict_param["S_" + electrode_id]
        I_pn1 = df_sim["I_" + electrode_id + "1"][tt]
        I_pn2 = df_sim["I_" + electrode_id + "2"][tt]
        I_pn3 = df_sim["I_" + electrode_id + "3"][tt]
        I_pn4 = df_sim["I_" + electrode_id + "4"][tt]
        I_pn5 = df_sim["I_" + electrode_id + "5"][tt]
        R_s_pn = dict_param["R_s_" + electrode_id]

        z = dict_param["z"]
        F = dict_param["F"]
        R = dict_param["R"]
        T = dict_param["T"]
        alpha = dict_param["alpha"]
        epsilon_e = dict_param["epsilon_e"]
        brugg_e = dict_param["brugg_e"]
        t_plus = dict_param["t_plus"]
        k_o_pn = dict_param["k_o_" + electrode_id]
        dx = dict_param["X_" + electrode_id] / 5

        C_s_max_pn1 = dict_param["C_s_max_" + electrode_id]
        C_s_max_pn2 = dict_param["C_s_max_" + electrode_id]
        C_s_max_pn3 = dict_param["C_s_max_" + electrode_id]
        C_s_max_pn4 = dict_param["C_s_max_" + electrode_id]
        C_s_max_pn5 = dict_param["C_s_max_" + electrode_id]

        C_s_pn1_surface = df_sim["C_s_" + electrode_id + "1_surface"][tt - 1]
        C_s_pn2_surface = df_sim["C_s_" + electrode_id + "2_surface"][tt - 1]
        C_s_pn3_surface = df_sim["C_s_" + electrode_id + "3_surface"][tt - 1]
        C_s_pn4_surface = df_sim["C_s_" + electrode_id + "4_surface"][tt - 1]
        C_s_pn5_surface = df_sim["C_s_" + electrode_id + "5_surface"][tt - 1]

        C_el_pn1 = df_sim["C_el_" + electrode_id + "1"][tt - 1]
        C_el_pn2 = df_sim["C_el_" + electrode_id + "2"][tt - 1]
        C_el_pn3 = df_sim["C_el_" + electrode_id + "3"][tt - 1]
        C_el_pn4 = df_sim["C_el_" + electrode_id + "4"][tt - 1]
        C_el_pn5 = df_sim["C_el_" + electrode_id + "5"][tt - 1]
        if electrode_id == "p":
            C_el_blk = df_el_blk_sim["X_0"][tt - 1] / dict_param["S_el"]
        else:
            C_el_blk = df_el_blk_sim["X_4"][tt - 1] / dict_param["S_el"]

        j_pn1 = I_pn1 / S_pn
        j_pn2 = I_pn2 / S_pn
        j_pn3 = I_pn3 / S_pn
        j_pn4 = I_pn4 / S_pn
        j_pn5 = I_pn5 / S_pn

        j_0_pn1 = z * F * k_o_pn * C_el_pn1 ** alpha * (C_s_max_pn1 - C_s_pn1_surface) ** alpha * (
            C_s_pn1_surface) ** alpha  # [A/m2]
        j_0_pn2 = z * F * k_o_pn * C_el_pn2 ** alpha * (C_s_max_pn2 - C_s_pn2_surface) ** alpha * (
            C_s_pn2_surface) ** alpha  # [A/m2]
        j_0_pn3 = z * F * k_o_pn * C_el_pn3 ** alpha * (C_s_max_pn3 - C_s_pn3_surface) ** alpha * (
            C_s_pn3_surface) ** alpha  # [A/m2]
        j_0_pn4 = z * F * k_o_pn * C_el_pn4 ** alpha * (C_s_max_pn4 - C_s_pn4_surface) ** alpha * (
            C_s_pn4_surface) ** alpha  # [A/m2]
        j_0_pn5 = z * F * k_o_pn * C_el_pn5 ** alpha * (C_s_max_pn5 - C_s_pn5_surface) ** alpha * (
            C_s_pn5_surface) ** alpha  # [A/m2]

        DV_eta_pn1 = -1 * (R * T) / (alpha * z * F) * math.log(
            j_pn1 / (2 * j_0_pn1) + ((j_pn1 / (2 * j_0_pn1)) ** 2 + 1) ** 0.5)
        DV_eta_pn2 = -1 * (R * T) / (alpha * z * F) * math.log(
            j_pn2 / (2 * j_0_pn2) + ((j_pn2 / (2 * j_0_pn2)) ** 2 + 1) ** 0.5)
        DV_eta_pn3 = -1 * (R * T) / (alpha * z * F) * math.log(
            j_pn3 / (2 * j_0_pn3) + ((j_pn3 / (2 * j_0_pn3)) ** 2 + 1) ** 0.5)
        DV_eta_pn4 = -1 * (R * T) / (alpha * z * F) * math.log(
            j_pn4 / (2 * j_0_pn4) + ((j_pn4 / (2 * j_0_pn4)) ** 2 + 1) ** 0.5)
        DV_eta_pn5 = -1 * (R * T) / (alpha * z * F) * math.log(
            j_pn5 / (2 * j_0_pn5) + ((j_pn5 / (2 * j_0_pn5)) ** 2 + 1) ** 0.5)

        Dphi_spn54 = -1 * R_s_pn * dx * (I_pn5)
        Dphi_spn43 = -1 * R_s_pn * dx * (I_pn5 + I_pn4)
        Dphi_spn32 = -1 * R_s_pn * dx * (I_pn5 + I_pn4 + I_pn3)
        Dphi_spn21 = -1 * R_s_pn * dx * (I_pn5 + I_pn4 + I_pn3 + I_pn2)
        Dphi_spn10 = -1 * R_s_pn * dx * (I_pn5 + I_pn4 + I_pn3 + I_pn2 + I_pn1)

        Dphi_elpnB5 = (-(I_pn1 + I_pn2 + I_pn3 + I_pn4 + I_pn5) * dx / CellDesign.kappa_e((C_el_blk + C_el_pn5) / 2,
                                                                                          dict_param["epsilon_e"],
                                                                                          dict_param["brugg_e"])
                       + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                   np.log(C_el_blk) - np.log(C_el_pn5)))

        Dphi_elpn54 = (-(I_pn1 + I_pn2 + I_pn3 + I_pn4) * dx / CellDesign.kappa_e((C_el_pn5 + C_el_pn4) / 2,
                                                                                  dict_param["epsilon_e"],
                                                                                  dict_param["brugg_e"])
                       + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                   np.log(C_el_pn5) - np.log(C_el_pn4)))
        Dphi_elpn43 = (-(I_pn1 + I_pn2 + I_pn3) * dx / CellDesign.kappa_e((C_el_pn4 + C_el_pn3) / 2,
                                                                          dict_param["epsilon_e"],
                                                                          dict_param["brugg_e"])
                       + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                   np.log(C_el_pn4) - np.log(C_el_pn3)))
        Dphi_elpn32 = (-(I_pn1 + I_pn2) * dx / CellDesign.kappa_e((C_el_pn3 + C_el_pn2) / 2, dict_param["epsilon_e"],
                                                                  dict_param["brugg_e"])
                       + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                   np.log(C_el_pn3) - np.log(C_el_pn2)))
        Dphi_elpn21 = (-(I_pn1) * dx / CellDesign.kappa_e((C_el_pn2 + C_el_pn1) / 2, dict_param["epsilon_e"],
                                                          dict_param["brugg_e"])
                       + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                   np.log(C_el_pn2) - np.log(C_el_pn1)))

        df_sim["DV_eta_" + electrode_id + "1"][tt] = DV_eta_pn1
        df_sim["DV_eta_" + electrode_id + "2"][tt] = DV_eta_pn2
        df_sim["DV_eta_" + electrode_id + "3"][tt] = DV_eta_pn3
        df_sim["DV_eta_" + electrode_id + "4"][tt] = DV_eta_pn4
        df_sim["DV_eta_" + electrode_id + "5"][tt] = DV_eta_pn5

        df_sim["Dphi_s" + electrode_id + "10"][tt] = Dphi_spn10
        df_sim["Dphi_s" + electrode_id + "21"][tt] = Dphi_spn21
        df_sim["Dphi_s" + electrode_id + "32"][tt] = Dphi_spn32
        df_sim["Dphi_s" + electrode_id + "43"][tt] = Dphi_spn43
        df_sim["Dphi_s" + electrode_id + "54"][tt] = Dphi_spn54

        # df_sim["Dphi_el"+electrode_id+"10"][tt] = Dphi_elpn10
        df_sim["Dphi_el" + electrode_id + "21"][tt] = Dphi_elpn21
        df_sim["Dphi_el" + electrode_id + "32"][tt] = Dphi_elpn32
        df_sim["Dphi_el" + electrode_id + "43"][tt] = Dphi_elpn43
        df_sim["Dphi_el" + electrode_id + "54"][tt] = Dphi_elpn54
        df_sim["Dphi_el" + electrode_id + "B5"][tt] = Dphi_elpnB5

        if electrode_id == "p":
            df_sim["Dphi_el" + electrode_id + "5"][tt] = df_DVel_blk_sim["X_0"][tt] - \
                                                         df_sim["Dphi_el" + electrode_id + "B5"][tt]
        else:
            df_sim["Dphi_el" + electrode_id + "5"][tt] = df_DVel_blk_sim["X_4"][tt] - \
                                                         df_sim["Dphi_el" + electrode_id + "B5"][tt]
        df_sim["Dphi_el" + electrode_id + "4"][tt] = df_sim["Dphi_el" + electrode_id + "5"][tt] - \
                                                     df_sim["Dphi_el" + electrode_id + "54"][tt]
        df_sim["Dphi_el" + electrode_id + "3"][tt] = df_sim["Dphi_el" + electrode_id + "4"][tt] - \
                                                     df_sim["Dphi_el" + electrode_id + "43"][tt]
        df_sim["Dphi_el" + electrode_id + "2"][tt] = df_sim["Dphi_el" + electrode_id + "3"][tt] - \
                                                     df_sim["Dphi_el" + electrode_id + "32"][tt]
        df_sim["Dphi_el" + electrode_id + "1"][tt] = df_sim["Dphi_el" + electrode_id + "2"][tt] - \
                                                     df_sim["Dphi_el" + electrode_id + "21"][tt]

        return df_sim

    def update_CT_current(self, tt, df_sim, dict_param, df_cell, mode="discharge"):

        I = dict_param["I"]
        R_s_pn = dict_param["R_s_p"]
        mode_k = 1 if mode == "discharge" else -1

        C_el_pn1 = df_sim["C_el_p1"][tt - 1]
        C_s_max_pn1 = dict_param["C_s_max_p"]
        C_s_pn1_surface = df_sim["C_s_p1_surface"][tt - 1]
        U_pn1 = df_sim["U_p1"][tt - 1]

        C_el_pn2 = df_sim["C_el_p2"][tt - 1]
        C_s_max_pn2 = dict_param["C_s_max_p"]
        C_s_pn2_surface = df_sim["C_s_p2_surface"][tt - 1]
        U_pn2 = df_sim["U_p2"][tt - 1]

        C_el_pn3 = df_sim["C_el_p3"][tt - 1]
        C_s_max_pn3 = dict_param["C_s_max_p"]
        C_s_pn3_surface = df_sim["C_s_p3_surface"][tt - 1]
        U_pn3 = df_sim["U_p3"][tt - 1]

        C_el_pn4 = df_sim["C_el_p4"][tt - 1]
        C_s_max_pn4 = dict_param["C_s_max_p"]
        C_s_pn4_surface = df_sim["C_s_p4_surface"][tt - 1]
        U_pn4 = df_sim["U_p4"][tt - 1]

        C_el_pn5 = df_sim["C_el_p5"][tt - 1]
        C_s_max_pn5 = dict_param["C_s_max_p"]
        C_s_pn5_surface = df_sim["C_s_p5_surface"][tt - 1]
        U_pn5 = df_sim["U_p5"][tt - 1]

        def equations(p,
                      I=I,
                      S_pn=dict_param["S_p"],
                      k_o_pn=dict_param["k_o_p"],
                      dx=dict_param["X_p"] / 5,
                      C_el_pn1=C_el_pn1, C_el_pn2=C_el_pn2, C_el_pn3=C_el_pn3,
                      C_el_pn4=C_el_pn4, C_el_pn5=C_el_pn5,
                      C_s_max_pn1=C_s_max_pn1, C_s_max_pn2=C_s_max_pn2, C_s_max_pn3=C_s_max_pn3,
                      C_s_max_pn4=C_s_max_pn4, C_s_max_pn5=C_s_max_pn5,
                      C_s_pn1_surface=C_s_pn1_surface, C_s_pn2_surface=C_s_pn2_surface, C_s_pn3_surface=C_s_pn3_surface,
                      C_s_pn4_surface=C_s_pn4_surface, C_s_pn5_surface=C_s_pn5_surface,
                      R_s_pn=R_s_pn,
                      df_cell=df_cell,
                      U_pn1=U_pn1, U_pn2=U_pn2, U_pn3=U_pn3,
                      U_pn4=U_pn4, U_pn5=U_pn5,
                      z=dict_param["z"], F=dict_param["F"], R=dict_param["R"],
                      T=dict_param["T"], alpha=dict_param["alpha"],
                      epsilon_e=dict_param["epsilon_e"], brugg_e=dict_param["brugg_e"],
                      t_plus=dict_param["t_plus"]):
            I_pn1, I_pn2, I_pn3, I_pn4, I_pn5, Dphi_elpn = p
            j_pn1 = (I_pn1) / S_pn
            j_pn2 = (I_pn2) / S_pn
            j_pn3 = (I_pn3) / S_pn
            j_pn4 = (I_pn4) / S_pn
            j_pn5 = (I_pn5) / S_pn

            j_0_pn1 = z * F * k_o_pn * C_el_pn1 ** alpha * (C_s_max_pn1 - C_s_pn1_surface) ** alpha * (
                C_s_pn1_surface) ** alpha  # [A/m2]
            j_0_pn2 = z * F * k_o_pn * C_el_pn2 ** alpha * (C_s_max_pn2 - C_s_pn2_surface) ** alpha * (
                C_s_pn2_surface) ** alpha  # [A/m2]
            j_0_pn3 = z * F * k_o_pn * C_el_pn3 ** alpha * (C_s_max_pn3 - C_s_pn3_surface) ** alpha * (
                C_s_pn3_surface) ** alpha  # [A/m2]
            j_0_pn4 = z * F * k_o_pn * C_el_pn4 ** alpha * (C_s_max_pn4 - C_s_pn4_surface) ** alpha * (
                C_s_pn4_surface) ** alpha  # [A/m2]
            j_0_pn5 = z * F * k_o_pn * C_el_pn5 ** alpha * (C_s_max_pn5 - C_s_pn5_surface) ** alpha * (
                C_s_pn5_surface) ** alpha  # [A/m2]

            DV_eta_pn1 = (R * T) / (alpha * z * F) * math.log(
                j_pn1 / (2 * j_0_pn1) + ((j_pn1 / (2 * j_0_pn1)) ** 2 + 1) ** 0.5)
            DV_eta_pn2 = (R * T) / (alpha * z * F) * math.log(
                j_pn2 / (2 * j_0_pn2) + ((j_pn2 / (2 * j_0_pn2)) ** 2 + 1) ** 0.5)
            DV_eta_pn3 = (R * T) / (alpha * z * F) * math.log(
                j_pn3 / (2 * j_0_pn3) + ((j_pn3 / (2 * j_0_pn3)) ** 2 + 1) ** 0.5)
            DV_eta_pn4 = (R * T) / (alpha * z * F) * math.log(
                j_pn4 / (2 * j_0_pn4) + ((j_pn4 / (2 * j_0_pn4)) ** 2 + 1) ** 0.5)
            DV_eta_pn5 = (R * T) / (alpha * z * F) * math.log(
                j_pn5 / (2 * j_0_pn5) + ((j_pn5 / (2 * j_0_pn5)) ** 2 + 1) ** 0.5)

            Dphi_spn54 = R_s_pn * dx * (I_pn5)
            Dphi_spn43 = R_s_pn * dx * (I_pn5 + I_pn4)
            Dphi_spn32 = R_s_pn * dx * (I_pn5 + I_pn4 + I_pn3)
            Dphi_spn21 = R_s_pn * dx * (I_pn5 + I_pn4 + I_pn3 + I_pn2)
            Dphi_spn10 = R_s_pn * dx * (I_pn5 + I_pn4 + I_pn3 + I_pn2 + I_pn1)

            Dphi_elpn54 = (-(I_pn1 + I_pn2 + I_pn3 + I_pn4) * dx / CellDesign.kappa_e((C_el_pn5 + C_el_pn4) / 2,
                                                                                      dict_param["epsilon_e"],
                                                                                      dict_param["brugg_e"])
                           + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                       np.log(C_el_pn5) - np.log(C_el_pn4)))
            Dphi_elpn43 = (-(I_pn1 + I_pn2 + I_pn3) * dx / CellDesign.kappa_e((C_el_pn4 + C_el_pn3) / 2,
                                                                              dict_param["epsilon_e"],
                                                                              dict_param["brugg_e"])
                           + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                       np.log(C_el_pn4) - np.log(C_el_pn3)))
            Dphi_elpn32 = (
                        -(I_pn1 + I_pn2) * dx / CellDesign.kappa_e((C_el_pn3 + C_el_pn2) / 2, dict_param["epsilon_e"],
                                                                   dict_param["brugg_e"])
                        + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                    np.log(C_el_pn3) - np.log(C_el_pn2)))
            Dphi_elpn21 = (-(I_pn1) * dx / CellDesign.kappa_e((C_el_pn2 + C_el_pn1) / 2, dict_param["epsilon_e"],
                                                              dict_param["brugg_e"])
                           + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                       np.log(C_el_pn2) - np.log(C_el_pn1)))

            f1 = Dphi_spn10 - U_pn1 * mode_k + DV_eta_pn1 * mode_k + Dphi_elpn21 + Dphi_elpn32 + Dphi_elpn43 + Dphi_elpn54 - Dphi_elpn
            f2 = Dphi_spn10 + Dphi_spn21 - U_pn2 * mode_k + DV_eta_pn2 * mode_k + Dphi_elpn32 + Dphi_elpn43 + Dphi_elpn54 - Dphi_elpn
            f3 = Dphi_spn10 + Dphi_spn21 + Dphi_spn32 - U_pn3 * mode_k + DV_eta_pn3 * mode_k + Dphi_elpn43 + Dphi_elpn54 - Dphi_elpn
            f4 = Dphi_spn10 + Dphi_spn21 + Dphi_spn32 + Dphi_spn43 - U_pn4 * mode_k + DV_eta_pn4 * mode_k + Dphi_elpn54 - Dphi_elpn
            f5 = Dphi_spn10 + Dphi_spn21 + Dphi_spn32 + Dphi_spn43 + Dphi_spn54 - U_pn5 * mode_k + DV_eta_pn5 * mode_k - Dphi_elpn
            f6 = I_pn1 + I_pn2 + I_pn3 + I_pn4 + I_pn5 - I * mode_k

            return (f1, f2, f3, f4, f5, f6)

        I_p1, I_p2, I_p3, I_p4, I_p5, Dphi_elp = fsolve(equations, (I / 5, I / 5, I / 5, I / 5, I / 5, 0))
        df_sim["I_p1"][tt] = I_p1
        df_sim["I_p2"][tt] = I_p2
        df_sim["I_p3"][tt] = I_p3
        df_sim["I_p4"][tt] = I_p4
        df_sim["I_p5"][tt] = I_p5
        df_sim["Dphi_elp"][tt] = Dphi_elp

        I = dict_param["I"]
        R_s_pn = dict_param["R_s_n"]
        mode_k = -1 if mode == "discharge" else 1

        C_el_pn1 = df_sim["C_el_n1"][tt - 1]
        C_s_max_pn1 = dict_param["C_s_max_n"]
        C_s_pn1_surface = df_sim["C_s_n1_surface"][tt - 1]
        U_pn1 = df_sim["U_n1"][tt - 1]

        C_el_pn2 = df_sim["C_el_n2"][tt - 1]
        C_s_max_pn2 = dict_param["C_s_max_n"]
        C_s_pn2_surface = df_sim["C_s_n2_surface"][tt - 1]
        U_pn2 = df_sim["U_n2"][tt - 1]

        C_el_pn3 = df_sim["C_el_n3"][tt - 1]
        C_s_max_pn3 = dict_param["C_s_max_n"]
        C_s_pn3_surface = df_sim["C_s_n3_surface"][tt - 1]
        U_pn3 = df_sim["U_n3"][tt - 1]

        C_el_pn4 = df_sim["C_el_n4"][tt - 1]
        C_s_max_pn4 = dict_param["C_s_max_n"]
        C_s_pn4_surface = df_sim["C_s_n4_surface"][tt - 1]
        U_pn4 = df_sim["U_n4"][tt - 1]

        C_el_pn5 = df_sim["C_el_n5"][tt - 1]
        C_s_max_pn5 = dict_param["C_s_max_n"]
        C_s_pn5_surface = df_sim["C_s_n5_surface"][tt - 1]
        U_pn5 = df_sim["U_n5"][tt - 1]

        def equations(p,
                      I=I,
                      S_pn=dict_param["S_n"],
                      k_o_pn=dict_param["k_o_n"],
                      dx=dict_param["X_n"] / 5,
                      C_el_pn1=C_el_pn1, C_el_pn2=C_el_pn2, C_el_pn3=C_el_pn3,
                      C_el_pn4=C_el_pn4, C_el_pn5=C_el_pn5,
                      C_s_max_pn1=C_s_max_pn1, C_s_max_pn2=C_s_max_pn2, C_s_max_pn3=C_s_max_pn3,
                      C_s_max_pn4=C_s_max_pn4, C_s_max_pn5=C_s_max_pn5,
                      C_s_pn1_surface=C_s_pn1_surface, C_s_pn2_surface=C_s_pn2_surface, C_s_pn3_surface=C_s_pn3_surface,
                      C_s_pn4_surface=C_s_pn4_surface, C_s_pn5_surface=C_s_pn5_surface,
                      R_s_pn=R_s_pn,
                      df_cell=df_cell,
                      U_pn1=U_pn1, U_pn2=U_pn2, U_pn3=U_pn3,
                      U_pn4=U_pn4, U_pn5=U_pn5,
                      z=dict_param["z"], F=dict_param["F"], R=dict_param["R"],
                      T=dict_param["T"], alpha=dict_param["alpha"],
                      epsilon_e=dict_param["epsilon_e"], brugg_e=dict_param["brugg_e"],
                      t_plus=dict_param["t_plus"]):
            I_pn1, I_pn2, I_pn3, I_pn4, I_pn5, Dphi_elpn = p
            j_pn1 = (I_pn1) / S_pn
            j_pn2 = (I_pn2) / S_pn
            j_pn3 = (I_pn3) / S_pn
            j_pn4 = (I_pn4) / S_pn
            j_pn5 = (I_pn5) / S_pn

            j_0_pn1 = z * F * k_o_pn * C_el_pn1 ** alpha * (C_s_max_pn1 - C_s_pn1_surface) ** alpha * (
                C_s_pn1_surface) ** alpha  # [A/m2]
            j_0_pn2 = z * F * k_o_pn * C_el_pn2 ** alpha * (C_s_max_pn2 - C_s_pn2_surface) ** alpha * (
                C_s_pn2_surface) ** alpha  # [A/m2]
            j_0_pn3 = z * F * k_o_pn * C_el_pn3 ** alpha * (C_s_max_pn3 - C_s_pn3_surface) ** alpha * (
                C_s_pn3_surface) ** alpha  # [A/m2]
            j_0_pn4 = z * F * k_o_pn * C_el_pn4 ** alpha * (C_s_max_pn4 - C_s_pn4_surface) ** alpha * (
                C_s_pn4_surface) ** alpha  # [A/m2]
            j_0_pn5 = z * F * k_o_pn * C_el_pn5 ** alpha * (C_s_max_pn5 - C_s_pn5_surface) ** alpha * (
                C_s_pn5_surface) ** alpha  # [A/m2]

            DV_eta_pn1 = (R * T) / (alpha * z * F) * math.log(
                j_pn1 / (2 * j_0_pn1) + ((j_pn1 / (2 * j_0_pn1)) ** 2 + 1) ** 0.5)
            DV_eta_pn2 = (R * T) / (alpha * z * F) * math.log(
                j_pn2 / (2 * j_0_pn2) + ((j_pn2 / (2 * j_0_pn2)) ** 2 + 1) ** 0.5)
            DV_eta_pn3 = (R * T) / (alpha * z * F) * math.log(
                j_pn3 / (2 * j_0_pn3) + ((j_pn3 / (2 * j_0_pn3)) ** 2 + 1) ** 0.5)
            DV_eta_pn4 = (R * T) / (alpha * z * F) * math.log(
                j_pn4 / (2 * j_0_pn4) + ((j_pn4 / (2 * j_0_pn4)) ** 2 + 1) ** 0.5)
            DV_eta_pn5 = (R * T) / (alpha * z * F) * math.log(
                j_pn5 / (2 * j_0_pn5) + ((j_pn5 / (2 * j_0_pn5)) ** 2 + 1) ** 0.5)

            Dphi_spn54 = R_s_pn * dx * (I_pn5)
            Dphi_spn43 = R_s_pn * dx * (I_pn5 + I_pn4)
            Dphi_spn32 = R_s_pn * dx * (I_pn5 + I_pn4 + I_pn3)
            Dphi_spn21 = R_s_pn * dx * (I_pn5 + I_pn4 + I_pn3 + I_pn2)
            Dphi_spn10 = R_s_pn * dx * (I_pn5 + I_pn4 + I_pn3 + I_pn2 + I_pn1)

            Dphi_elpn54 = (-(I_pn1 + I_pn2 + I_pn3 + I_pn4) * dx / CellDesign.kappa_e((C_el_pn5 + C_el_pn4) / 2,
                                                                                      dict_param["epsilon_e"],
                                                                                      dict_param["brugg_e"])
                           + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                       np.log(C_el_pn5) - np.log(C_el_pn4)))
            Dphi_elpn43 = (-(I_pn1 + I_pn2 + I_pn3) * dx / CellDesign.kappa_e((C_el_pn4 + C_el_pn3) / 2,
                                                                              dict_param["epsilon_e"],
                                                                              dict_param["brugg_e"])
                           + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                       np.log(C_el_pn4) - np.log(C_el_pn3)))
            Dphi_elpn32 = (
                        -(I_pn1 + I_pn2) * dx / CellDesign.kappa_e((C_el_pn3 + C_el_pn2) / 2, dict_param["epsilon_e"],
                                                                   dict_param["brugg_e"])
                        + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                    np.log(C_el_pn3) - np.log(C_el_pn2)))
            Dphi_elpn21 = (-(I_pn1) * dx / CellDesign.kappa_e((C_el_pn2 + C_el_pn1) / 2, dict_param["epsilon_e"],
                                                              dict_param["brugg_e"])
                           + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                       np.log(C_el_pn2) - np.log(C_el_pn1)))

            f1 = Dphi_spn10 - U_pn1 * (-1) + DV_eta_pn1 * (
                -1) + Dphi_elpn21 + Dphi_elpn32 + Dphi_elpn43 + Dphi_elpn54 - Dphi_elpn
            f2 = Dphi_spn10 + Dphi_spn21 - U_pn2 * (-1) + DV_eta_pn2 * (
                -1) + Dphi_elpn32 + Dphi_elpn43 + Dphi_elpn54 - Dphi_elpn
            f3 = Dphi_spn10 + Dphi_spn21 + Dphi_spn32 - U_pn3 * (-1) + DV_eta_pn3 * (
                -1) + Dphi_elpn43 + Dphi_elpn54 - Dphi_elpn
            f4 = Dphi_spn10 + Dphi_spn21 + Dphi_spn32 + Dphi_spn43 - U_pn4 * (-1) + DV_eta_pn4 * (
                -1) + Dphi_elpn54 - Dphi_elpn
            f5 = Dphi_spn10 + Dphi_spn21 + Dphi_spn32 + Dphi_spn43 + Dphi_spn54 - U_pn5 * (-1) + DV_eta_pn5 * (
                -1) - Dphi_elpn
            f6 = I_pn1 + I_pn2 + I_pn3 + I_pn4 + I_pn5 - I * (-1)

            return (f1, f2, f3, f4, f5, f6)

        I_n1, I_n2, I_n3, I_n4, I_n5, Dphi_eln = fsolve(equations, (I / 5, I / 5, I / 5, I / 5, I / 5, 0))

        df_sim["I_n1"][tt] = I_n1
        df_sim["I_n2"][tt] = I_n2
        df_sim["I_n3"][tt] = I_n3
        df_sim["I_n4"][tt] = I_n4
        df_sim["I_n5"][tt] = I_n5
        df_sim["Dphi_eln"][tt] = Dphi_eln

        return df_sim

    def update_CT_current_p(self, tt, df_sim, dict_param, df_cell, mode="discharge"):

        I = dict_param["I"]
        R_s_pn = dict_param["R_s_p"]
        mode_k = 1 if mode == "discharge" else -1

        C_el_pn1 = df_sim["C_el_p1"][tt - 1]
        C_s_max_pn1 = dict_param["C_s_max_p"]
        C_s_pn1_surface = df_sim["C_s_p1_surface"][tt - 1]
        U_pn1 = df_sim["U_p1"][tt - 1]

        C_el_pn2 = df_sim["C_el_p2"][tt - 1]
        C_s_max_pn2 = dict_param["C_s_max_p"]
        C_s_pn2_surface = df_sim["C_s_p2_surface"][tt - 1]
        U_pn2 = df_sim["U_p2"][tt - 1]

        C_el_pn3 = df_sim["C_el_p3"][tt - 1]
        C_s_max_pn3 = dict_param["C_s_max_p"]
        C_s_pn3_surface = df_sim["C_s_p3_surface"][tt - 1]
        U_pn3 = df_sim["U_p3"][tt - 1]

        C_el_pn4 = df_sim["C_el_p4"][tt - 1]
        C_s_max_pn4 = dict_param["C_s_max_p"]
        C_s_pn4_surface = df_sim["C_s_p4_surface"][tt - 1]
        U_pn4 = df_sim["U_p4"][tt - 1]

        C_el_pn5 = df_sim["C_el_p5"][tt - 1]
        C_s_max_pn5 = dict_param["C_s_max_p"]
        C_s_pn5_surface = df_sim["C_s_p5_surface"][tt - 1]
        U_pn5 = df_sim["U_p5"][tt - 1]

        def equations(p,
                      I=I,
                      S_pn=dict_param["S_p"],
                      k_o_pn=dict_param["k_o_p"],
                      dx=dict_param["X_p"] / 5,
                      C_el_pn1=C_el_pn1, C_el_pn2=C_el_pn2, C_el_pn3=C_el_pn3,
                      C_el_pn4=C_el_pn4, C_el_pn5=C_el_pn5,
                      C_s_max_pn1=C_s_max_pn1, C_s_max_pn2=C_s_max_pn2, C_s_max_pn3=C_s_max_pn3,
                      C_s_max_pn4=C_s_max_pn4, C_s_max_pn5=C_s_max_pn5,
                      C_s_pn1_surface=C_s_pn1_surface, C_s_pn2_surface=C_s_pn2_surface, C_s_pn3_surface=C_s_pn3_surface,
                      C_s_pn4_surface=C_s_pn4_surface, C_s_pn5_surface=C_s_pn5_surface,
                      R_s_pn=R_s_pn,
                      df_cell=df_cell,
                      U_pn1=U_pn1, U_pn2=U_pn2, U_pn3=U_pn3,
                      U_pn4=U_pn4, U_pn5=U_pn5,
                      z=dict_param["z"], F=dict_param["F"], R=dict_param["R"],
                      T=dict_param["T"], alpha=dict_param["alpha"],
                      epsilon_e=dict_param["epsilon_e"], brugg_e=dict_param["brugg_e"],
                      t_plus=dict_param["t_plus"]):
            I_pn1, I_pn2, I_pn3, I_pn4, I_pn5, Dphi_elpn = p
            j_pn1 = (I_pn1) / S_pn
            j_pn2 = (I_pn2) / S_pn
            j_pn3 = (I_pn3) / S_pn
            j_pn4 = (I_pn4) / S_pn
            j_pn5 = (I_pn5) / S_pn

            j_0_pn1 = z * F * k_o_pn * C_el_pn1 ** alpha * (C_s_max_pn1 - C_s_pn1_surface) ** alpha * (
                C_s_pn1_surface) ** alpha  # [A/m2]
            j_0_pn2 = z * F * k_o_pn * C_el_pn2 ** alpha * (C_s_max_pn2 - C_s_pn2_surface) ** alpha * (
                C_s_pn2_surface) ** alpha  # [A/m2]
            j_0_pn3 = z * F * k_o_pn * C_el_pn3 ** alpha * (C_s_max_pn3 - C_s_pn3_surface) ** alpha * (
                C_s_pn3_surface) ** alpha  # [A/m2]
            j_0_pn4 = z * F * k_o_pn * C_el_pn4 ** alpha * (C_s_max_pn4 - C_s_pn4_surface) ** alpha * (
                C_s_pn4_surface) ** alpha  # [A/m2]
            j_0_pn5 = z * F * k_o_pn * C_el_pn5 ** alpha * (C_s_max_pn5 - C_s_pn5_surface) ** alpha * (
                C_s_pn5_surface) ** alpha  # [A/m2]

            DV_eta_pn1 = (R * T) / (alpha * z * F) * math.log(
                j_pn1 / (2 * j_0_pn1) + ((j_pn1 / (2 * j_0_pn1)) ** 2 + 1) ** 0.5)
            DV_eta_pn2 = (R * T) / (alpha * z * F) * math.log(
                j_pn2 / (2 * j_0_pn2) + ((j_pn2 / (2 * j_0_pn2)) ** 2 + 1) ** 0.5)
            DV_eta_pn3 = (R * T) / (alpha * z * F) * math.log(
                j_pn3 / (2 * j_0_pn3) + ((j_pn3 / (2 * j_0_pn3)) ** 2 + 1) ** 0.5)
            DV_eta_pn4 = (R * T) / (alpha * z * F) * math.log(
                j_pn4 / (2 * j_0_pn4) + ((j_pn4 / (2 * j_0_pn4)) ** 2 + 1) ** 0.5)
            DV_eta_pn5 = (R * T) / (alpha * z * F) * math.log(
                j_pn5 / (2 * j_0_pn5) + ((j_pn5 / (2 * j_0_pn5)) ** 2 + 1) ** 0.5)

            Dphi_spn54 = R_s_pn * dx * (I_pn5)
            Dphi_spn43 = R_s_pn * dx * (I_pn5 + I_pn4)
            Dphi_spn32 = R_s_pn * dx * (I_pn5 + I_pn4 + I_pn3)
            Dphi_spn21 = R_s_pn * dx * (I_pn5 + I_pn4 + I_pn3 + I_pn2)
            Dphi_spn10 = R_s_pn * dx * (I_pn5 + I_pn4 + I_pn3 + I_pn2 + I_pn1)

            Dphi_elpn54 = (-(I_pn1 + I_pn2 + I_pn3 + I_pn4) * dx / CellDesign.kappa_e((C_el_pn5 + C_el_pn4) / 2,
                                                                                      dict_param["epsilon_e"],
                                                                                      dict_param["brugg_e"])
                           + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                       np.log(C_el_pn5) - np.log(C_el_pn4)))
            Dphi_elpn43 = (-(I_pn1 + I_pn2 + I_pn3) * dx / CellDesign.kappa_e((C_el_pn4 + C_el_pn3) / 2,
                                                                              dict_param["epsilon_e"],
                                                                              dict_param["brugg_e"])
                           + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                       np.log(C_el_pn4) - np.log(C_el_pn3)))
            Dphi_elpn32 = (
                        -(I_pn1 + I_pn2) * dx / CellDesign.kappa_e((C_el_pn3 + C_el_pn2) / 2, dict_param["epsilon_e"],
                                                                   dict_param["brugg_e"])
                        + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                    np.log(C_el_pn3) - np.log(C_el_pn2)))
            Dphi_elpn21 = (-(I_pn1) * dx / CellDesign.kappa_e((C_el_pn2 + C_el_pn1) / 2, dict_param["epsilon_e"],
                                                              dict_param["brugg_e"])
                           + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                       np.log(C_el_pn2) - np.log(C_el_pn1)))

            f1 = Dphi_spn10 - U_pn1 * mode_k + DV_eta_pn1 * mode_k + Dphi_elpn21 + Dphi_elpn32 + Dphi_elpn43 + Dphi_elpn54 + Dphi_elpn
            f2 = Dphi_spn10 + Dphi_spn21 - U_pn2 * mode_k + DV_eta_pn2 * mode_k + Dphi_elpn32 + Dphi_elpn43 + Dphi_elpn54 + Dphi_elpn
            f3 = Dphi_spn10 + Dphi_spn21 + Dphi_spn32 - U_pn3 * mode_k + DV_eta_pn3 * mode_k + Dphi_elpn43 + Dphi_elpn54 + Dphi_elpn
            f4 = Dphi_spn10 + Dphi_spn21 + Dphi_spn32 + Dphi_spn43 - U_pn4 * mode_k + DV_eta_pn4 * mode_k + Dphi_elpn54 + Dphi_elpn
            f5 = Dphi_spn10 + Dphi_spn21 + Dphi_spn32 + Dphi_spn43 + Dphi_spn54 - U_pn5 * mode_k + DV_eta_pn5 * mode_k + Dphi_elpn
            f6 = I_pn1 + I_pn2 + I_pn3 + I_pn4 + I_pn5 - I * mode_k

            return (f1, f2, f3, f4, f5, f6)

        I_p1, I_p2, I_p3, I_p4, I_p5, Dphi_elp = fsolve(equations, (I / 5, I / 5, I / 5, I / 5, I / 5, 0))
        df_sim["I_p1"][tt] = I_p1
        df_sim["I_p2"][tt] = I_p2
        df_sim["I_p3"][tt] = I_p3
        df_sim["I_p4"][tt] = I_p4
        df_sim["I_p5"][tt] = I_p5
        df_sim["Dphi_elp"][tt] = Dphi_elp

        return df_sim

    def update_CT_current_n(self, tt, df_sim, dict_param, df_cell, mode="discharge"):

        I = dict_param["I"]
        R_s_pn = dict_param["R_s_n"]
        # mode_k = -1 if mode == "discharge" else 1

        C_el_pn1 = df_sim["C_el_n1"][tt - 1]
        C_s_max_pn1 = dict_param["C_s_max_n"]
        C_s_pn1_surface = df_sim["C_s_n1_surface"][tt - 1]
        U_pn1 = df_sim["U_n1"][tt - 1]

        C_el_pn2 = df_sim["C_el_n2"][tt - 1]
        C_s_max_pn2 = dict_param["C_s_max_n"]
        C_s_pn2_surface = df_sim["C_s_n2_surface"][tt - 1]
        U_pn2 = df_sim["U_n2"][tt - 1]

        C_el_pn3 = df_sim["C_el_n3"][tt - 1]
        C_s_max_pn3 = dict_param["C_s_max_n"]
        C_s_pn3_surface = df_sim["C_s_n3_surface"][tt - 1]
        U_pn3 = df_sim["U_n3"][tt - 1]

        C_el_pn4 = df_sim["C_el_n4"][tt - 1]
        C_s_max_pn4 = dict_param["C_s_max_n"]
        C_s_pn4_surface = df_sim["C_s_n4_surface"][tt - 1]
        U_pn4 = df_sim["U_n4"][tt - 1]

        C_el_pn5 = df_sim["C_el_n5"][tt - 1]
        C_s_max_pn5 = dict_param["C_s_max_n"]
        C_s_pn5_surface = df_sim["C_s_n5_surface"][tt - 1]
        U_pn5 = df_sim["U_n5"][tt - 1]

        def equations(p,
                      I=I,
                      S_pn=dict_param["S_n"],
                      k_o_pn=dict_param["k_o_n"],
                      dx=dict_param["X_n"] / 5,
                      C_el_pn1=C_el_pn1, C_el_pn2=C_el_pn2, C_el_pn3=C_el_pn3,
                      C_el_pn4=C_el_pn4, C_el_pn5=C_el_pn5,
                      C_s_max_pn1=C_s_max_pn1, C_s_max_pn2=C_s_max_pn2, C_s_max_pn3=C_s_max_pn3,
                      C_s_max_pn4=C_s_max_pn4, C_s_max_pn5=C_s_max_pn5,
                      C_s_pn1_surface=C_s_pn1_surface, C_s_pn2_surface=C_s_pn2_surface, C_s_pn3_surface=C_s_pn3_surface,
                      C_s_pn4_surface=C_s_pn4_surface, C_s_pn5_surface=C_s_pn5_surface,
                      R_s_pn=R_s_pn,
                      df_cell=df_cell,
                      U_pn1=U_pn1, U_pn2=U_pn2, U_pn3=U_pn3,
                      U_pn4=U_pn4, U_pn5=U_pn5,
                      z=dict_param["z"], F=dict_param["F"], R=dict_param["R"],
                      T=dict_param["T"], alpha=dict_param["alpha"],
                      epsilon_e=dict_param["epsilon_e"], brugg_e=dict_param["brugg_e"],
                      t_plus=dict_param["t_plus"]):
            I_pn1, I_pn2, I_pn3, I_pn4, I_pn5, Dphi_elpn = p
            j_pn1 = (I_pn1) / S_pn
            j_pn2 = (I_pn2) / S_pn
            j_pn3 = (I_pn3) / S_pn
            j_pn4 = (I_pn4) / S_pn
            j_pn5 = (I_pn5) / S_pn

            j_0_pn1 = z * F * k_o_pn * C_el_pn1 ** alpha * (C_s_max_pn1 - C_s_pn1_surface) ** alpha * (
                C_s_pn1_surface) ** alpha  # [A/m2]
            j_0_pn2 = z * F * k_o_pn * C_el_pn2 ** alpha * (C_s_max_pn2 - C_s_pn2_surface) ** alpha * (
                C_s_pn2_surface) ** alpha  # [A/m2]
            j_0_pn3 = z * F * k_o_pn * C_el_pn3 ** alpha * (C_s_max_pn3 - C_s_pn3_surface) ** alpha * (
                C_s_pn3_surface) ** alpha  # [A/m2]
            j_0_pn4 = z * F * k_o_pn * C_el_pn4 ** alpha * (C_s_max_pn4 - C_s_pn4_surface) ** alpha * (
                C_s_pn4_surface) ** alpha  # [A/m2]
            j_0_pn5 = z * F * k_o_pn * C_el_pn5 ** alpha * (C_s_max_pn5 - C_s_pn5_surface) ** alpha * (
                C_s_pn5_surface) ** alpha  # [A/m2]

            DV_eta_pn1 = (R * T) / (alpha * z * F) * math.log(
                j_pn1 / (2 * j_0_pn1) + ((j_pn1 / (2 * j_0_pn1)) ** 2 + 1) ** 0.5)
            DV_eta_pn2 = (R * T) / (alpha * z * F) * math.log(
                j_pn2 / (2 * j_0_pn2) + ((j_pn2 / (2 * j_0_pn2)) ** 2 + 1) ** 0.5)
            DV_eta_pn3 = (R * T) / (alpha * z * F) * math.log(
                j_pn3 / (2 * j_0_pn3) + ((j_pn3 / (2 * j_0_pn3)) ** 2 + 1) ** 0.5)
            DV_eta_pn4 = (R * T) / (alpha * z * F) * math.log(
                j_pn4 / (2 * j_0_pn4) + ((j_pn4 / (2 * j_0_pn4)) ** 2 + 1) ** 0.5)
            DV_eta_pn5 = (R * T) / (alpha * z * F) * math.log(
                j_pn5 / (2 * j_0_pn5) + ((j_pn5 / (2 * j_0_pn5)) ** 2 + 1) ** 0.5)

            Dphi_spn54 = R_s_pn * dx * (I_pn5)
            Dphi_spn43 = R_s_pn * dx * (I_pn5 + I_pn4)
            Dphi_spn32 = R_s_pn * dx * (I_pn5 + I_pn4 + I_pn3)
            Dphi_spn21 = R_s_pn * dx * (I_pn5 + I_pn4 + I_pn3 + I_pn2)
            Dphi_spn10 = R_s_pn * dx * (I_pn5 + I_pn4 + I_pn3 + I_pn2 + I_pn1)

            Dphi_elpn54 = (-(I_pn1 + I_pn2 + I_pn3 + I_pn4) * dx / CellDesign.kappa_e((C_el_pn5 + C_el_pn4) / 2,
                                                                                      dict_param["epsilon_e"],
                                                                                      dict_param["brugg_e"])
                           + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                       np.log(C_el_pn5) - np.log(C_el_pn4)))
            Dphi_elpn43 = (-(I_pn1 + I_pn2 + I_pn3) * dx / CellDesign.kappa_e((C_el_pn4 + C_el_pn3) / 2,
                                                                              dict_param["epsilon_e"],
                                                                              dict_param["brugg_e"])
                           + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                       np.log(C_el_pn4) - np.log(C_el_pn3)))
            Dphi_elpn32 = (
                        -(I_pn1 + I_pn2) * dx / CellDesign.kappa_e((C_el_pn3 + C_el_pn2) / 2, dict_param["epsilon_e"],
                                                                   dict_param["brugg_e"])
                        + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                    np.log(C_el_pn3) - np.log(C_el_pn2)))
            Dphi_elpn21 = (-(I_pn1) * dx / CellDesign.kappa_e((C_el_pn2 + C_el_pn1) / 2, dict_param["epsilon_e"],
                                                              dict_param["brugg_e"])
                           + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                                       np.log(C_el_pn2) - np.log(C_el_pn1)))

            f1 = Dphi_spn10 - U_pn1 * (+1) + DV_eta_pn1 * (
                +1) + Dphi_elpn21 + Dphi_elpn32 + Dphi_elpn43 + Dphi_elpn54 + Dphi_elpn
            f2 = Dphi_spn10 + Dphi_spn21 - U_pn2 * (+1) + DV_eta_pn2 * (
                +1) + Dphi_elpn32 + Dphi_elpn43 + Dphi_elpn54 + Dphi_elpn
            f3 = Dphi_spn10 + Dphi_spn21 + Dphi_spn32 - U_pn3 * (+1) + DV_eta_pn3 * (
                +1) + Dphi_elpn43 + Dphi_elpn54 + Dphi_elpn
            f4 = Dphi_spn10 + Dphi_spn21 + Dphi_spn32 + Dphi_spn43 - U_pn4 * (+1) + DV_eta_pn4 * (
                +1) + Dphi_elpn54 + Dphi_elpn
            f5 = Dphi_spn10 + Dphi_spn21 + Dphi_spn32 + Dphi_spn43 + Dphi_spn54 - U_pn5 * (+1) + DV_eta_pn5 * (
                +1) + Dphi_elpn
            f6 = I_pn1 + I_pn2 + I_pn3 + I_pn4 + I_pn5 - I * (-1)

            return (f1, f2, f3, f4, f5, f6)

        I_n1, I_n2, I_n3, I_n4, I_n5, Dphi_eln = fsolve(equations, (I / 5, I / 5, I / 5, I / 5, I / 5, 0))

        df_sim["I_n1"][tt] = I_n1
        df_sim["I_n2"][tt] = I_n2
        df_sim["I_n3"][tt] = I_n3
        df_sim["I_n4"][tt] = I_n4
        df_sim["I_n5"][tt] = I_n5
        df_sim["Dphi_eln"][tt] = Dphi_eln

        return df_sim

    # Calculation of Li concentration inside active material particle.
    # n=10 # Number of grid insed particle

    def init_df_s_pn(self, L_pn, V_pn, C_s_pn_0, dict_param, tt=0, n=10):

        dx = L_pn / n
        t = np.arange(0, dict_param["t_total"] + dict_param["dt"], dict_param["dt"])
        df_pn_sim = pd.DataFrame(t)
        df_pn_sim.columns = ['Time (sec)']

        for ii in range(n):
            kwargs = {"L_%d" % ii: lambda x: np.nan}
            df_pn_sim = df_pn_sim.assign(**kwargs)

        x = np.linspace(dx / 2, L_pn - dx / 2, n)
        C = np.ones(len(x)) * C_s_pn_0 * V_pn / L_pn

        df_pn_sim.iloc[tt, 1:] = C

        df_pn2_sim = df_pn_sim.copy()
        df_pn3_sim = df_pn_sim.copy()
        df_pn4_sim = df_pn_sim.copy()
        df_pn5_sim = df_pn_sim.copy()

        return x, df_pn_sim, df_pn2_sim, df_pn3_sim, df_pn4_sim, df_pn5_sim

    def update_df_s_pn(self, df_pn_sim, particle_id, electrode_id, x, df_sim, dict_param, tt, D_pn, L_pn, S_pn, V_pn,
                       df_LCO_OCV, df_LiC6_OCV, C_s_max_pn):

        n = len(x)
        dx = L_pn / n
        dt = dict_param["dt"]
        dCdt = np.empty(n)
        C = np.array(df_pn_sim.iloc[tt - 1, 1:])
        j_pn = df_sim[("I_" + particle_id)][tt] / S_pn  # .iloc[tt]

        for i in range(1, n - 1):
            # Applying discrete definition of second derivative
            dCdt[i] = D_pn * ((C[i + 1] - C[i]) / dx - (C[i] - C[i - 1]) / dx) / dx

        # Taking into account boundary condition. ie. T[0-1] DNE
        dCdt[0] = D_pn * ((C[1] - C[0]) / dx) / dx
        dCdt[n - 1] = D_pn * (j_pn * S_pn / dict_param["F"] / D_pn - (C[n - 1] - C[n - 2]) / dx) / dx

        # Update temperature data for rod
        C = C + dCdt * dt

        df_pn_sim.iloc[tt, 1:] = C
        df_sim[("C_s_" + particle_id + "_surface")][tt] = C[-1] / V_pn * L_pn  # (mol/m3)
        if electrode_id == "p":
            # df_sim["U_"+particle_id][tt] = df_cell['Cathode OCV (V)'][abs(df_cell['Cathode x (-)'] - df_sim["C_s_"+particle_id+"_surface"][tt]/C_s_max_pn).idxmin()]
            df_sim["U_" + particle_id][tt] = df_LCO_OCV['Potential(V)'][
                abs(df_LCO_OCV['x'] - df_sim["C_s_" + particle_id + "_surface"][tt] / C_s_max_pn).idxmin()]
        else:
            # df_sim["U_"+particle_id][tt] = df_cell['Anode OCV (V)'][abs(df_cell['Anode x (-)'] - 1 + df_sim["C_s_"+particle_id+"_surface"][tt]/C_s_max_pn).idxmin()]
            df_sim["U_" + particle_id][tt] = df_LiC6_OCV['Potential(V)'][
                abs(df_LiC6_OCV['x'] - 1 + df_sim["C_s_" + particle_id + "_surface"][tt] / C_s_max_pn).idxmin()]

        return df_pn_sim, df_sim

    def init_df_el_pn(self, df_sim, X_pn, dict_param, tt=0, n=5):

        C_e_0 = dict_param["C_e_0"]
        S_el = dict_param["S_el"]
        dx = X_pn / n
        V_pn = S_el * X_pn
        t = np.arange(0, dict_param["t_total"] + dict_param["dt"], dict_param["dt"])
        df_el_pn_sim = pd.DataFrame(t)
        df_el_pn_sim.columns = ['Time (sec)']

        for ii in range(n):
            kwargs = {"X_%d" % ii: lambda x: np.nan}
            df_el_pn_sim = df_el_pn_sim.assign(**kwargs)
        x = np.linspace(dx / 2, X_pn - dx / 2, n)
        C = np.ones(len(x)) * C_e_0 * S_el

        df_el_pn_sim.iloc[tt, 1:] = C

        return x, df_el_pn_sim

    def init_df_el_blk(self, df_sim, dict_param, tt=0, n=5):

        C_e_0 = dict_param["C_e_0"]
        L_el = dict_param["L_el"]
        S_el = dict_param["S_el"]
        dx = L_el / n
        V_el = S_el * L_el
        t = np.arange(0, dict_param["t_total"] + dict_param["dt"], dict_param["dt"])
        df_el_blk_sim = pd.DataFrame(t)
        df_el_blk_sim.columns = ['Time (sec)']

        for ii in range(n):
            kwargs = {"X_%d" % ii: lambda x: np.nan}
            df_el_blk_sim = df_el_blk_sim.assign(**kwargs)

        x = np.linspace(dx / 2, L_el - dx / 2, n)
        C = np.ones(len(x)) * C_e_0 * S_el

        df_el_blk_sim.iloc[tt, 1:] = C

        return x, df_el_blk_sim

    def init_df_DVel_blk(self, df_el_blk_sim, dict_param, tt=0, n=5):

        L_el = dict_param["L_el"]
        dx = L_el / n
        x = np.linspace(dx, L_el - dx, n - 1)
        df_DVel_blk_sim = np.zeros((n - 1))
        t = np.arange(0, dict_param["t_total"] + dict_param["dt"], dict_param["dt"])
        df_DVel_blk_sim = pd.DataFrame(t)
        df_DVel_blk_sim.columns = ['Time (sec)']

        for ii in range(0, n):
            kwargs = {"X_%d" % ii: lambda x: np.nan}
            df_DVel_blk_sim = df_DVel_blk_sim.assign(**kwargs)

        # DV= (-(dict_param["I"])*dx/CellDesign.kappa_e((df_el_blk_sim.iloc[tt, 2:].values+df_el_blk_sim.iloc[tt, 1:-1].values)/2, dict_param["epsilon_e"], dict_param["brugg_e"])
        #                           + 2*dict_param["R"]*dict_param["T"]/dict_param["F"]*(0.5 - dict_param["t_plus"])*(np.log(df_el_blk_sim.iloc[tt, 2:].values) - np.log(df_el_blk_sim.iloc[tt, 1:-1].values)))
        # DV= (-(dict_param["I"])*dx/CellDesign.kappa_e((df_el_blk_sim.iloc[tt, 1:].values+df_el_blk_sim.iloc[tt, 1])/2, dict_param["epsilon_e"], dict_param["brugg_e"])
        #                           + 2*dict_param["R"]*dict_param["T"]/dict_param["F"]*(0.5 - dict_param["t_plus"])*(np.log(df_el_blk_sim.iloc[tt, 1:].values) - np.log(df_el_blk_sim.iloc[tt, 1])))
        DV = (-(dict_param["I"]) * dx / CellDesign.kappa_e(
            (df_el_blk_sim.iloc[tt, 1:].values / dict_param["S_el"] + dict_param["C_e_0"]) / 2, dict_param["epsilon_e"],
            dict_param["brugg_e"])
              + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                          np.log(df_el_blk_sim.iloc[tt, 1:].values / dict_param["S_el"]) - np.log(dict_param["C_e_0"])))

        df_DVel_blk_sim.iloc[tt, 1:] = DV

        return x, df_DVel_blk_sim

    def update_df_DVel_blk(self, df_el_blk_sim, df_DVel_blk_sim, dict_param, tt, n=5):

        L_el = dict_param["L_el"]
        dx = L_el / n
        # DV= (-(dict_param["I"])*dx/CellDesign.kappa_e((df_el_blk_sim.iloc[tt, 2:].values+df_el_blk_sim.iloc[tt, 1:-1].values)/2, dict_param["epsilon_e"], dict_param["brugg_e"])
        #                           + 2*dict_param["R"]*dict_param["T"]/dict_param["F"]*(0.5 - dict_param["t_plus"])*(np.log(df_el_blk_sim.iloc[tt, 2:].values) - np.log(df_el_blk_sim.iloc[tt, 1:-1].values)))
        # DV= (-(dict_param["I"])*dx/CellDesign.kappa_e((df_el_blk_sim.iloc[tt, 1:].values+df_el_blk_sim.iloc[tt, 1])/2, dict_param["epsilon_e"], dict_param["brugg_e"])
        #                           + 2*dict_param["R"]*dict_param["T"]/dict_param["F"]*(0.5 - dict_param["t_plus"])*(np.log(df_el_blk_sim.iloc[tt, 1:].values) - np.log(df_el_blk_sim.iloc[tt, 1])))
        DV = (-(dict_param["I"]) * dx / CellDesign.kappa_e(
            (df_el_blk_sim.iloc[tt, 1:].values / dict_param["S_el"] + dict_param["C_e_0"]) / 2, dict_param["epsilon_e"],
            dict_param["brugg_e"])
              + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (0.5 - dict_param["t_plus"]) * (
                          np.log(df_el_blk_sim.iloc[tt, 1:].values / dict_param["S_el"]) - np.log(dict_param["C_e_0"])))
        df_DVel_blk_sim.iloc[tt, 1:] = DV

        return df_DVel_blk_sim

    def update_df_el_pn(self, df_el_pn_sim, df_el_blk_sim, electrode_id, x, df_sim, dict_param, tt, df_cell):

        if electrode_id == "p":
            C_e_blk = df_el_blk_sim.iloc[tt - 1, 1]
        else:
            C_e_blk = df_el_blk_sim.iloc[tt - 1, -1]
        X_pn = dict_param["X_" + electrode_id]
        C_s_max_pn = dict_param["C_s_max_" + electrode_id]
        n = len(x)
        dx = X_pn / n
        dCdt = np.empty(n)
        C = np.array(df_el_pn_sim.iloc[tt - 1, 1:])
        dt = dict_param["dt"]

        # j_pn=df_sim[("I_"+particle_id)][tt]/S_pn#.iloc[tt]1

        for i in range(1, n - 1):
            dCdt[i] = (1 / dict_param["epsilon"] * (
                        dict_param["Deff"] * ((C[i + 1] - C[i]) / dx - (C[i] - C[i - 1]) / dx) / dx)
                       - 1 / dx * (1 - dict_param["t_plus"]) / dict_param["F"] *
                       df_sim[("I_" + electrode_id + "{}".format(i + 1))][tt])

        dCdt[0] = (1 / dict_param["epsilon"] * (dict_param["Deff"] * ((C[1] - C[0]) / dx) / dx)
                   - 1 / dx * (1 - dict_param["t_plus"]) / dict_param["F"] *
                   df_sim[("I_" + electrode_id + "{}".format(1))][tt])

        i = n - 1
        # dCdt[i] = 1/dict_param["epsilon"]*(dict_param["Deff"]*((C_e_blk*dict_param["S_el"]  - C[i])/dx - (C[i] - C[i-1])/dx)/dx)
        dCdt[i] = (1 / dict_param["epsilon"] * (
                    dict_param["Deff"] * ((C_e_blk - C[i]) / dx - (C[i] - C[i - 1]) / dx) / dx)
                   - 1 / dx * (1 - dict_param["t_plus"]) / dict_param["F"] *
                   df_sim[("I_" + electrode_id + "{}".format(i + 1))][tt])

        # Update temperature data for rod
        C = C + dCdt * dt

        # ???? 要修正
        C = np.where(C <= 0, 1E-10, C)

        df_el_pn_sim.iloc[tt, 1:] = C
        for ii in range(n):
            df_sim["C_el_" + electrode_id + "{}".format(ii + 1)][tt] = df_el_pn_sim["X_" + "{}".format(ii)].loc[tt] / \
                                                                       dict_param["S_el"]

        # df_sim[("C_s_"+particle_id+"_surface")][tt] = C[-1]/V_pn*L_pn #(mol/m3)
        # df_sim["U_"+particle_id][tt] = df_cell['Cathode OCV (V)'][abs(df_cell['Cathode x (-)'] - df_sim["C_s_"+particle_id+"_surface"][tt]/C_s_max_pn).idxmin()]
        return df_el_pn_sim, df_sim

    def update_df_el_n(self, df_el_pn_sim, df_el_blk_sim, x, df_sim, dict_param, tt, df_cell):

        C_e_blk = df_el_blk_sim.iloc[tt - 1, -1]
        X_pn = dict_param["X_n"]
        C_s_max_pn = dict_param["C_s_max_n"]
        n = len(x)
        dx = X_pn / n
        dCdt = np.empty(n)
        C = np.array(df_el_pn_sim.iloc[tt - 1, 1:])
        dt = dict_param["dt"]

        for i in range(1, n - 1):
            dCdt[i] = 1 / dict_param["epsilon"] * (
                        dict_param["Deff"] * ((C[i + 1] - C[i]) / dx - (C[i] - C[i - 1]) / dx) / dx) - 1 / dx * (
                                  1 - dict_param["t_plus"]) / dict_param["F"] * df_sim[("I_n{}".format(i + 1))][tt]

        dCdt[0] = 1 / dict_param["epsilon"] * (dict_param["Deff"] * ((C[1] - C[0]) / dx) / dx) - 1 / dx * (
                    1 - dict_param["t_plus"]) / dict_param["F"] * df_sim[("I_n{}".format(1))][tt]

        i = n - 1
        # dCdt[i] = 1/dict_param["epsilon"]*(dict_param["Deff"]*((C_e_blk*dict_param["S_el"]  - C[i])/dx - (C[i] - C[i-1])/dx)/dx)
        dCdt[i] = 1 / dict_param["epsilon"] * (
                    dict_param["Deff"] * ((C_e_blk - C[i]) / dx - (C[i] - C[i - 1]) / dx) / dx) - 1 / dx * (
                              1 - dict_param["t_plus"]) / dict_param["F"] * df_sim[("I_n{}".format(i + 1))][tt]

        # Update temperature data for rod
        C = C + dCdt * dt

        df_el_pn_sim.iloc[tt, 1:] = C
        for ii in range(n):
            df_sim["C_el_n{}".format(ii + 1)][tt] = df_el_pn_sim["X_{}".format(ii)].loc[tt] / dict_param["S_el"]

        # df_sim[("C_s_"+particle_id+"_surface")][tt] = C[-1]/V_pn*L_pn #(mol/m3)
        # df_sim["U_"+particle_id][tt] = df_cell['Cathode OCV (V)'][abs(df_cell['Cathode x (-)'] - df_sim["C_s_"+particle_id+"_surface"][tt]/C_s_max_pn).idxmin()]
        return df_el_pn_sim, df_sim

    def update_df_el_blk(self, df_el_p_sim, df_el_n_sim, df_el_blk_sim, x, df_sim, dict_param, tt, df_cell):

        n = len(x)
        dx = dict_param["L_el"] / n
        C = np.array(df_el_blk_sim.iloc[tt - 1, 1:])
        dt = dict_param["dt"]
        dCdt = np.empty(n)
        C_e_p = df_el_p_sim.iloc[tt - 1, -1]
        C_e_n = df_el_n_sim.iloc[tt - 1, -1]

        for i in range(1, n - 1):
            dCdt[i] = 1 / dict_param["epsilon"] * (
                        dict_param["Deff"] * ((C[i + 1] - C[i]) / dx - (C[i] - C[i - 1]) / dx) / dx)

        dCdt[0] = 1 / dict_param["epsilon"] * (dict_param["Deff"] * ((C[1] - C[0]) / dx - (C[0] - C_e_p) / dx) / dx)
        # dCdt[0] = 1/dict_param["epsilon"]*(dict_param["Deff"]*((C[1] - C[0])/dx - (C[0] - C_e_p*dict_param["S_el"])/dx)/dx)
        i = n - 1
        dCdt[i] = 1 / dict_param["epsilon"] * (dict_param["Deff"] * ((C_e_n - C[i]) / dx - (C[i] - C[i - 1]) / dx) / dx)
        # dCdt[i] = 1/dict_param["epsilon"]*(dict_param["Deff"]*((C_e_n*dict_param["S_el"] - C[i])/dx - (C[i] - C[i-1])/dx)/dx)

        # Update temperature data for rod
        C = C + dCdt * dt

        df_el_blk_sim.iloc[tt, 1:] = C
        return df_el_blk_sim  # , df_sim
