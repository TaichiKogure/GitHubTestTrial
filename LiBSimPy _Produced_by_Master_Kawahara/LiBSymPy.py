# X_p, X_el, X_nが同じ前提の計算。　gridもすべて同じ場合のみに動作する。
# ELのLiイオン濃度差による濃度過電圧を(1-t+)ではなく(0.5-t+)としている。
# EL中のLiイオン濃度が0に近づくと計算時間が非常に大きくなってしまう。


import math

import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
# import matplotlib.animation as animation
from matplotlib import animation
from scipy.optimize import fsolve


class LiBSym():

    def __init__(self):
        self.new_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                           '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                           '#bcbd22', '#17becf']

    def init_result(self, dict_param, df_cell, tt=0):
        # Parameter setting

        tt_total = int(dict_param["tt_total"])
        self.x_p = np.arange(dict_param["x_grid_num_p"]) * dict_param["dx_p"] * 1E6 + dict_param["dx_p"] / 2 * 1E6
        self.x_blk = np.arange(dict_param["x_grid_num_sep"]) * dict_param["dx_el"] * 1E6 + dict_param["dx_el"] / 2 * 1E6
        self.x_n = np.arange(dict_param["x_grid_num_n"]) * dict_param["dx_n"] * 1E6 + dict_param["dx_n"] / 2 * 1E6

        self.t_count = np.zeros(tt_total)
        self.t_count[tt] = tt

        tt_p1 = dict_param["x_grid_num_p"] * tt
        tt_p2 = dict_param["x_grid_num_p"] * (tt + 1)
        tt_el1 = dict_param["x_grid_num_sep"] * tt
        tt_el2 = dict_param["x_grid_num_sep"] * (tt + 1)
        tt_n1 = dict_param["x_grid_num_n"] * tt
        tt_n2 = dict_param["x_grid_num_n"] * (tt + 1)

        self.C_el_p = np.zeros(tt_total * dict_param["x_grid_num_p"])
        self.C_el_p[tt_p1:tt_p2] = dict_param["C_e_0"]
        self.C_el_blk = np.zeros(tt_total * dict_param["x_grid_num_sep"])
        self.C_el_blk[tt_el1:tt_el2] = dict_param["C_e_0"]
        self.C_el_n = np.zeros(tt_total * dict_param["x_grid_num_n"])
        self.C_el_n[tt_n1:tt_n2] = dict_param["C_e_0"]

        self.Phi_el_p = np.zeros(tt_total * dict_param["x_grid_num_p"])
        self.Phi_el_blk = np.zeros(tt_total * dict_param["x_grid_num_sep"])
        self.Phi_el_n = np.zeros(tt_total * dict_param["x_grid_num_n"])

        self.I_ct_p = np.zeros(tt_total * dict_param["x_grid_num_p"])
        self.I_ct_blk = np.zeros(tt_total * dict_param["x_grid_num_sep"])
        self.I_ct_n = np.zeros(tt_total * dict_param["x_grid_num_n"])

        self.U_p = np.zeros(tt_total * dict_param["x_grid_num_p"])
        self.U_p[tt_p1:tt_p2] = df_cell['Cathode OCV (V)'][0]
        self.U_n = np.zeros(tt_total * dict_param["x_grid_num_n"])
        self.U_n[tt_n1:tt_n2] = df_cell['Anode OCV (V)'][0]

        self.C_s_surface_p = np.zeros(tt_total * dict_param["x_grid_num_p"])
        self.C_s_surface_p[tt_p1:tt_p2] = dict_param['C_s_p_0']
        self.C_s_surface_n = np.zeros(tt_total * dict_param["x_grid_num_n"])
        self.C_s_surface_n[tt_n1:tt_n2] = dict_param['C_s_n_0']

        self.DV_eta_p = np.zeros(tt_total * dict_param["x_grid_num_p"])
        self.DV_eta_n = np.zeros(tt_total * dict_param["x_grid_num_n"])

        self.Phi_s_p = np.zeros(tt_total * dict_param["x_grid_num_p"])
        self.Phi_s_n = np.zeros(tt_total * dict_param["x_grid_num_n"])

        self.Phi_s_p[tt_p1:tt_p2] = self.Phi_el_p[tt_p1:tt_p2] + self.U_p[tt_p1:tt_p2] + self.DV_eta_p[tt_p1:tt_p2]
        self.Phi_s_n[tt_n1:tt_n2] = self.Phi_el_n[tt_n1:tt_n2] + self.U_n[tt_n1:tt_n2] + self.DV_eta_n[tt_n1:tt_n2]
        self.r_p = np.arange(dict_param["r_grid_num_p"]) * dict_param["dr_p"] * 1E6 + dict_param["dr_p"] / 2 * 1E6
        self.r_n = np.arange(dict_param["r_grid_num_n"]) * dict_param["dr_n"] * 1E6 + dict_param["dr_n"] / 2 * 1E6

        self.C_s_p = np.zeros((dict_param["x_grid_num_p"], tt_total * dict_param["r_grid_num_p"]))
        self.C_s_p[:, (tt) * dict_param["r_grid_num_p"]: (tt + 1) * dict_param["r_grid_num_p"]] = dict_param['C_s_p_0']

        self.C_s_n = np.zeros((dict_param["x_grid_num_n"], tt_total * dict_param["r_grid_num_n"]))
        self.C_s_n[:, (tt) * dict_param["r_grid_num_n"]: (tt + 1) * dict_param["r_grid_num_n"]] = dict_param['C_s_n_0']

        self.DV_Al = np.zeros(tt_total)
        self.DV_Cu = np.zeros(tt_total)

    def update_CT_current(self, tt, dict_param, df_cell, C_el_pn, C_s_surface_pn, U_pn, electrode_id, mode="discharge"):
        # Charge transfer current calculation

        I = dict_param["I"]
        if I == 0:
            I_pn = np.zeros(dict_param["x_grid_num_" + electrode_id])
        else:
            R_s_pn = dict_param["R_s_" + electrode_id]
            C_s_max_pn = dict_param["C_s_max_" + electrode_id]
            S_pn = dict_param["S_" + electrode_id]
            k_o_pn = dict_param["k_o_" + electrode_id]
            dx = dict_param["dx_" + electrode_id]
            C_el_pn_tt = C_el_pn[(tt - 1) * dict_param["x_grid_num_" + electrode_id]:tt * dict_param[
                "x_grid_num_" + electrode_id]]
            C_s_pn_surface_tt = C_s_surface_pn[(tt - 1) * dict_param["x_grid_num_" + electrode_id]: tt * dict_param[
                "x_grid_num_" + electrode_id]]
            U_pn_tt = U_pn[
                      (tt - 1) * dict_param["x_grid_num_" + electrode_id]:tt * dict_param["x_grid_num_" + electrode_id]]

            if electrode_id == "p":
                mode_k = 1 if mode == "discharge" else -1
            else:
                mode_k = -1 if mode == "discharge" else 1

            def equations(p,
                          I=I,
                          S_pn=S_pn,
                          k_o_pn=k_o_pn,
                          dx=dx,
                          C_el_pn1=C_el_pn_tt[0],
                          C_el_pn2=C_el_pn_tt[1],
                          C_el_pn3=C_el_pn_tt[2],
                          C_el_pn4=C_el_pn_tt[3],
                          C_el_pn5=C_el_pn_tt[4],
                          C_s_max_pn=C_s_max_pn,
                          C_s_pn1_surface=C_s_pn_surface_tt[0],
                          C_s_pn2_surface=C_s_pn_surface_tt[1],
                          C_s_pn3_surface=C_s_pn_surface_tt[2],
                          C_s_pn4_surface=C_s_pn_surface_tt[3],
                          C_s_pn5_surface=C_s_pn_surface_tt[4],
                          R_s_pn=R_s_pn,
                          df_cell=df_cell,
                          U_pn1=U_pn_tt[0],
                          U_pn2=U_pn_tt[1],
                          U_pn3=U_pn_tt[2],
                          U_pn4=U_pn_tt[3],
                          U_pn5=U_pn_tt[4],
                          z=dict_param["z"],
                          F=dict_param["F"],
                          R=dict_param["R"],
                          T=dict_param["T"],
                          alpha=dict_param["alpha"],
                          epsilon_e=dict_param["epsilon_e"],
                          brugg_e=dict_param["brugg_e"],
                          t_plus=dict_param["t_plus"]):

                I_pn1, I_pn2, I_pn3, I_pn4, I_pn5, Dphi_elpn = p

                j_pn1 = (I_pn1) / S_pn
                j_pn2 = (I_pn2) / S_pn
                j_pn3 = (I_pn3) / S_pn
                j_pn4 = (I_pn4) / S_pn
                j_pn5 = (I_pn5) / S_pn

                j_0_pn1 = z * F * k_o_pn * C_el_pn1 ** alpha * (C_s_max_pn - C_s_pn1_surface) ** alpha * (
                    C_s_pn1_surface) ** alpha  # [A/m2]
                j_0_pn2 = z * F * k_o_pn * C_el_pn2 ** alpha * (C_s_max_pn - C_s_pn2_surface) ** alpha * (
                    C_s_pn2_surface) ** alpha  # [A/m2]
                j_0_pn3 = z * F * k_o_pn * C_el_pn3 ** alpha * (C_s_max_pn - C_s_pn3_surface) ** alpha * (
                    C_s_pn3_surface) ** alpha  # [A/m2]
                j_0_pn4 = z * F * k_o_pn * C_el_pn4 ** alpha * (C_s_max_pn - C_s_pn4_surface) ** alpha * (
                    C_s_pn4_surface) ** alpha  # [A/m2]
                j_0_pn5 = z * F * k_o_pn * C_el_pn5 ** alpha * (C_s_max_pn - C_s_pn5_surface) ** alpha * (
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
                               + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (
                                           0.5 - dict_param["t_plus"]) * (np.log(C_el_pn5) - np.log(C_el_pn4)))
                Dphi_elpn43 = (-(I_pn1 + I_pn2 + I_pn3) * dx / CellDesign.kappa_e((C_el_pn4 + C_el_pn3) / 2,
                                                                                  dict_param["epsilon_e"],
                                                                                  dict_param["brugg_e"])
                               + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (
                                           0.5 - dict_param["t_plus"]) * (np.log(C_el_pn4) - np.log(C_el_pn3)))
                Dphi_elpn32 = (-(I_pn1 + I_pn2) * dx / CellDesign.kappa_e((C_el_pn3 + C_el_pn2) / 2,
                                                                          dict_param["epsilon_e"],
                                                                          dict_param["brugg_e"])
                               + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (
                                           0.5 - dict_param["t_plus"]) * (np.log(C_el_pn3) - np.log(C_el_pn2)))
                Dphi_elpn21 = (-(I_pn1) * dx / CellDesign.kappa_e((C_el_pn2 + C_el_pn1) / 2, dict_param["epsilon_e"],
                                                                  dict_param["brugg_e"])
                               + 2 * dict_param["R"] * dict_param["T"] / dict_param["F"] * (
                                           0.5 - dict_param["t_plus"]) * (np.log(C_el_pn2) - np.log(C_el_pn1)))

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
                f6 = I_pn1 + I_pn2 + I_pn3 + I_pn4 + I_pn5 - I * mode_k

                return (f1, f2, f3, f4, f5, f6)

            I_pn1, I_pn2, I_pn3, I_pn4, I_pn5, Dphi_elpn = fsolve(equations, (0, 0, 0, 0, 0, 0))
            I_pn = np.array([I_pn1, I_pn2, I_pn3, I_pn4, I_pn5])

        return I_pn

    def update_result4(self, tt, C_s_pn, I_ct_pn, dict_param, electrode_id):
        # Update Li concentraion inside active matrial.

        x_grid_num = dict_param["x_grid_num_" + electrode_id]
        r_grid_num = dict_param["r_grid_num_" + electrode_id]
        S_pn = dict_param["S_" + electrode_id]
        D_pn = dict_param["D_" + electrode_id]
        V_pn = dict_param["V_" + electrode_id]
        L_pn = dict_param["L_" + electrode_id]
        tt_1 = r_grid_num * tt
        tt_2 = r_grid_num * (tt + 1)
        dx = dict_param["dr_" + electrode_id]
        dt = dict_param["dt"]

        aa = dt / (dx) ** 2 * D_pn
        pp = 1 / 2
        qq = 1 - pp

        Amat = np.zeros([r_grid_num, r_grid_num])
        for i in range(r_grid_num):
            Amat[i, i] = 1 + 2 * aa * pp
            if i < r_grid_num - 1:
                Amat[i, i + 1] = -1 * aa * pp
                Amat[i + 1, i] = -1 * aa * pp
        Amat[0, 0] = 1 + 1 * aa * pp
        Amat[r_grid_num - 1, r_grid_num - 1] = 1 + 1 * aa * pp

        Bmat = np.zeros([r_grid_num, r_grid_num])
        for i in range(r_grid_num):
            Bmat[i, i] = 1 - 2 * aa * qq
            if i < r_grid_num - 1:
                Bmat[i, i + 1] = aa * qq
                Bmat[i + 1, i] = aa * qq

        Bmat[0, 0] = 1 - 1 * aa * qq
        Bmat[r_grid_num - 1, r_grid_num - 1] = 1 - 1 * aa * qq

        Ivec_t2 = np.zeros([r_grid_num])

        for ii in range(x_grid_num):
            Ivec_t2[-1] = (I_ct_pn[(tt) * x_grid_num:(tt + 1) * x_grid_num] / dict_param["F"] / dx * dt)[ii]
            Cvec_t1 = C_s_pn[ii, (tt - 1) * r_grid_num:(tt) * r_grid_num] * V_pn / L_pn
            Cvec_t2 = np.dot(np.linalg.inv(Amat), np.dot(Bmat, Cvec_t1) + Ivec_t2)
            C_s_pn[ii, tt_1:tt_2] = Cvec_t2 * L_pn / V_pn

        return C_s_pn

    def update_result5(self, tt, dict_param, df_cell, df_LCO_OCV, df_LiC6_OCV):
        # Update Li concentraion inside electrolyte.
        # Crank–Nicolson method.

        tt_p1 = dict_param["x_grid_num_p"] * tt
        tt_p2 = dict_param["x_grid_num_p"] * (tt + 1)
        tt_el1 = dict_param["x_grid_num_sep"] * tt
        tt_el2 = dict_param["x_grid_num_sep"] * (tt + 1)
        tt_n1 = dict_param["x_grid_num_n"] * tt
        tt_n2 = dict_param["x_grid_num_n"] * (tt + 1)

        self.t_count[tt] = tt
        self.I_ct_p[tt_p1:tt_p2] = self.update_CT_current(tt=tt, dict_param=dict_param, df_cell=df_cell,
                                                          C_el_pn=self.C_el_p,
                                                          C_s_surface_pn=self.C_s_surface_p, U_pn=self.U_p,
                                                          electrode_id="p", mode="discharge")
        self.I_ct_n[tt_n1:tt_n2] = self.update_CT_current(tt=tt, dict_param=dict_param, df_cell=df_cell,
                                                          C_el_pn=self.C_el_n,
                                                          C_s_surface_pn=self.C_s_surface_n, U_pn=self.U_n,
                                                          electrode_id="n", mode="discharge")

        self.C_s_p = self.update_result4(tt=tt, C_s_pn=self.C_s_p, I_ct_pn=self.I_ct_p, dict_param=dict_param,
                                         electrode_id="p")
        self.C_s_n = self.update_result4(tt=tt, C_s_pn=self.C_s_n, I_ct_pn=self.I_ct_n, dict_param=dict_param,
                                         electrode_id="n")

        self.C_s_surface_p[tt_p1:tt_p2] = self.C_s_p[:, dict_param["r_grid_num_p"] * (tt + 1) - 1].flatten()
        self.C_s_surface_n[tt_n1:tt_n2] = self.C_s_n[:, dict_param["r_grid_num_n"] * (tt + 1) - 1].flatten()

        x_grid_num = dict_param["x_grid_num_p"]
        for ii in range(x_grid_num):
            self.U_p[tt_p1 + ii] = (np.array(df_LCO_OCV["Potential(V)"])
                .flat[np.argmin(abs(np.array(df_LCO_OCV['x'])
                                    - (self.C_s_surface_p[(tt) * x_grid_num:(tt + 1) * x_grid_num] / dict_param[
                "C_s_max_p"])[ii]))])

        x_grid_num = dict_param["x_grid_num_n"]
        for ii in range(x_grid_num):
            self.U_n[tt_n1 + ii] = (np.array(df_LiC6_OCV["Potential(V)"])
                .flat[np.argmin(abs(np.array(df_LiC6_OCV['x'])
                                    - (1 - self.C_s_surface_n[(tt) * x_grid_num:(tt + 1) * x_grid_num] / dict_param[
                "C_s_max_n"])[ii]))])
            # "1-" needed. Li1-xC6.

        dt = dict_param["dt"]
        F = dict_param["F"]
        epsilon = dict_param["epsilon"]
        t_plus = dict_param["t_plus"]
        Deff = dict_param["Deff"]
        S_el = dict_param["S_el"]

        x_grid_num = dict_param["x_grid_num_p"] + dict_param["x_grid_num_sep"] + dict_param["x_grid_num_n"]
        dx = dict_param["dx_p"]
        if dict_param["dx_p"] != dict_param["dx_n"]:
            print("ERROR")

        tt1_p1 = dict_param["x_grid_num_p"] * (tt - 1)
        tt1_p2 = dict_param["x_grid_num_p"] * (tt)
        tt1_sep1 = dict_param["x_grid_num_sep"] * (tt - 1)
        tt1_sep2 = dict_param["x_grid_num_sep"] * (tt)
        tt1_n1 = dict_param["x_grid_num_n"] * (tt - 1)
        tt1_n2 = dict_param["x_grid_num_n"] * (tt)

        tt2_p1 = dict_param["x_grid_num_p"] * tt
        tt2_p2 = dict_param["x_grid_num_p"] * (tt + 1)
        tt2_sep1 = dict_param["x_grid_num_sep"] * tt
        tt2_sep2 = dict_param["x_grid_num_sep"] * (tt + 1)
        tt2_n1 = dict_param["x_grid_num_n"] * tt
        tt2_n2 = dict_param["x_grid_num_n"] * (tt + 1)

        Ivec_t2 = np.hstack(
            (self.I_ct_p[tt2_p1:tt2_p2], np.zeros([dict_param["x_grid_num_sep"]]), self.I_ct_n[tt2_n1:tt2_n2][::-1]))
        Cvec_t1 = np.hstack(
            (self.C_el_p[tt1_p1:tt1_p2], self.C_el_blk[tt1_sep1:tt1_sep2], self.C_el_n[tt1_n1:tt1_n2][::-1])) * S_el

        aa = dt / (dx) ** 2 * Deff / epsilon
        # bb = -1*dt*1/dx*(1-t_plus)/F/epsilon
        bb = -1 * dt / (dict_param["S_el"] * dict_param["dx_p"]) * (1 - t_plus) / F / epsilon * dict_param[
            "S_el"]  # mol/mに変換するため*Sel
        # 比表面積

        pp = 1 / 2
        qq = 1 - pp

        Ivec_t2 = Ivec_t2 * bb

        Amat = np.zeros([x_grid_num, x_grid_num])
        for i in range(x_grid_num):
            Amat[i, i] = 1 + 2 * aa * pp

            if i < x_grid_num - 1:
                Amat[i, i + 1] = -1 * aa * pp
                Amat[i + 1, i] = -1 * aa * pp
        Amat[0, 0] = 1 + 1 * aa * pp
        Amat[x_grid_num - 1, x_grid_num - 1] = 1 + 1 * aa * pp

        Bmat = np.zeros([x_grid_num, x_grid_num])
        for i in range(x_grid_num):
            Bmat[i, i] = 1 - 2 * aa * qq

            if i < x_grid_num - 1:
                Bmat[i, i + 1] = aa * qq
                Bmat[i + 1, i] = aa * qq

        Bmat[0, 0] = 1 - 1 * aa * qq
        Bmat[x_grid_num - 1, x_grid_num - 1] = 1 - 1 * aa * qq

        Cmat = np.zeros([x_grid_num, x_grid_num])
        for i in range(x_grid_num):
            Cmat[i, i] = 1

        Cvec_t2 = np.dot(np.linalg.inv(Amat), np.dot(Bmat, Cvec_t1) + np.dot(Cmat, Ivec_t2))

        return Cvec_t2

    def update_result6(self, tt, dict_param, df_cell, df_LCO_OCV, df_LiC6_OCV):
        # Update Li concentraion inside electrolyte.
        # Crank–Nicolson method.

        S_el = dict_param["S_el"]
        tt2_p1 = dict_param["x_grid_num_p"] * tt
        tt2_p2 = dict_param["x_grid_num_p"] * (tt + 1)
        tt2_sep1 = dict_param["x_grid_num_sep"] * tt
        tt2_sep2 = dict_param["x_grid_num_sep"] * (tt + 1)
        tt2_n1 = dict_param["x_grid_num_n"] * tt
        tt2_n2 = dict_param["x_grid_num_n"] * (tt + 1)

        I = dict_param["I"]
        C_e_0 = dict_param["C_e_0"]
        epsilon_e = dict_param["epsilon_e"]
        brugg_e = dict_param["brugg_e"]
        t_plus = dict_param["t_plus"]
        F = dict_param["F"]
        R = dict_param["R"]
        T = dict_param["T"]
        x_grid_num = dict_param["x_grid_num_p"] + dict_param["x_grid_num_sep"] + dict_param["x_grid_num_n"]
        dx = dict_param["dx_p"]
        if dict_param["dx_p"] != dict_param["dx_n"]:
            print("ERROR")

        Cvec_t2 = self.update_result5(tt, dict_param=dict_param, df_cell=df_cell, df_LCO_OCV=df_LCO_OCV,
                                      df_LiC6_OCV=df_LiC6_OCV)
        if min(Cvec_t2) <= 0:
            dict_param["dt"] = dict_param["dt"] * 0.5
            Cvec_t2 = self.update_result5(tt, dict_param=dict_param, df_cell=df_cell, df_LCO_OCV=df_LCO_OCV,
                                          df_LiC6_OCV=df_LiC6_OCV)
        self.C_el_p[tt2_p1:tt2_p2] = (
            (Cvec_t2 / S_el)[0: dict_param["x_grid_num_p"]])
        self.C_el_blk[tt2_sep1:tt2_sep2] = (
            (Cvec_t2 / S_el)[dict_param["x_grid_num_p"]:dict_param["x_grid_num_p"] + dict_param["x_grid_num_sep"]])
        self.C_el_n[tt2_n1:tt2_n2] = (
            (Cvec_t2 / S_el)[dict_param["x_grid_num_p"] + dict_param["x_grid_num_sep"]:][::-1])

        Phi_el_tt = (-I * dx / CellDesign.kappa_e((Cvec_t2 / dict_param["S_el"] + C_e_0) / 2, epsilon_e, brugg_e)
                     + 2 * R * T / F * (0.5 - t_plus) * (np.log(Cvec_t2 / dict_param["S_el"]) - np.log(C_e_0)))
        self.Phi_el[x_grid_num * tt: x_grid_num * (tt + 1)] = Phi_el_tt

    def update_result7(self, tt, dict_param):
        # Calculation of  charge transfer over-potential,  electrolyte potential and over-potential of foil.

        tt1_p1 = dict_param["x_grid_num_p"] * (tt - 1)
        tt1_p2 = dict_param["x_grid_num_p"] * (tt)
        tt1_sep1 = dict_param["x_grid_num_sep"] * (tt - 1)
        tt1_sep2 = dict_param["x_grid_num_sep"] * (tt)
        tt1_n1 = dict_param["x_grid_num_n"] * (tt - 1)
        tt1_n2 = dict_param["x_grid_num_n"] * (tt)
        tt2_p1 = dict_param["x_grid_num_p"] * tt
        tt2_p2 = dict_param["x_grid_num_p"] * (tt + 1)
        tt2_sep1 = dict_param["x_grid_num_sep"] * tt
        tt2_sep2 = dict_param["x_grid_num_sep"] * (tt + 1)
        tt2_n1 = dict_param["x_grid_num_n"] * tt
        tt2_n2 = dict_param["x_grid_num_n"] * (tt + 1)
        dt = dict_param["dt"]
        R_s_p = dict_param["R_s_p"]
        R_s_n = dict_param["R_s_n"]
        z = dict_param["z"]
        F = dict_param["F"]
        R = dict_param["R"]
        T = dict_param["T"]
        alpha = dict_param["alpha"]
        k_o_p = dict_param["k_o_p"]
        k_o_n = dict_param["k_o_n"]
        C_s_max_p = dict_param["C_s_max_p"]
        C_s_max_n = dict_param["C_s_max_n"]
        S_p = dict_param["S_p"]
        S_n = dict_param["S_n"]
        I = dict_param["I"]
        x_grid_num = dict_param["x_grid_num_p"] + dict_param["x_grid_num_sep"] + dict_param["x_grid_num_n"]
        dx = dict_param["dx_p"]
        if dict_param["dx_p"] != dict_param["dx_n"]:
            print("ERROR")

        I_ct_p_tt = self.I_ct_p[tt2_p1:tt2_p2]
        I_ct_n_tt = self.I_ct_n[tt2_n1:tt2_n2]

        j_p = I_ct_p_tt / S_p
        j_n = I_ct_n_tt / S_n

        C_s_p_surface_tt = self.C_s_surface_p[tt1_p1:tt1_p2]
        C_s_n_surface_tt = self.C_s_surface_n[tt1_n1:tt1_n2]

        C_el_p_tt = self.C_el_p[tt1_p1:tt1_p2]
        C_el_n_tt = self.C_el_n[tt1_n1:tt1_n2]

        j_0_p = z * F * k_o_p * C_el_p_tt ** alpha * (C_s_max_p - C_s_p_surface_tt) ** alpha * (
            C_s_p_surface_tt) ** alpha  # [A/m2]
        j_0_n = z * F * k_o_n * C_el_n_tt ** alpha * (C_s_max_n - C_s_n_surface_tt) ** alpha * (
            C_s_n_surface_tt) ** alpha  # [A/m2]

        DV_eta_p_tt = -1 * (R * T) / (alpha * z * F) * np.log(j_p / (2 * j_0_p) + ((j_p / (2 * j_0_p)) ** 2 + 1) ** 0.5)
        DV_eta_n_tt = -1 * (R * T) / (alpha * z * F) * np.log(j_n / (2 * j_0_n) + ((j_n / (2 * j_0_n)) ** 2 + 1) ** 0.5)

        self.DV_eta_p[tt2_p1:tt2_p2] = DV_eta_p_tt
        self.DV_eta_n[tt2_n1:tt2_n2] = DV_eta_n_tt

        # [Dphi_spn10, Dphi_spn21, Dphi_spn32, Dphi_spn43, Dphi_spn54]
        self.Dphi_sp = -1 * R_s_p * dx * np.array(
            [sum(I_ct_p_tt[-5:]), sum(I_ct_p_tt[-4:]), sum(I_ct_p_tt[-3:]), sum(I_ct_p_tt[-2:]), sum(I_ct_p_tt[-1:])])
        self.Dphi_sn = -1 * R_s_n * dx * np.array(
            [sum(I_ct_n_tt[-5:]), sum(I_ct_n_tt[-4:]), sum(I_ct_n_tt[-3:]), sum(I_ct_n_tt[-2:]), sum(I_ct_n_tt[-1:])])

        self.Phi_s_p[tt2_p1:tt2_p2] = self.Phi_el[x_grid_num * tt: x_grid_num * (tt + 1)][
                                      0:dict_param["x_grid_num_p"]] + self.DV_eta_p[tt2_p1:tt2_p2] + self.U_p[
                                                                                                     tt2_p1:tt2_p2]
        self.Phi_s_n[tt2_n1:tt2_n2] = self.Phi_el[x_grid_num * tt: x_grid_num * (tt + 1)][-dict_param["x_grid_num_n"]:][
                                      ::-1] + self.DV_eta_n[tt2_n1:tt2_n2] + self.U_n[tt2_n1:tt2_n2]

        self.DV_Al[tt] = np.array(-1 * (dict_param["rho_0_Al"]
                                        * (1 + dict_param["alpha_Al"] * (dict_param["T"] - 296.15))
                                        * dict_param["L_Al"] / dict_param["S_Al"] * dict_param["I"]))

        self.DV_Cu[tt] = np.array(-1 * (dict_param["rho_0_Cu"]
                                        * (1 + dict_param["alpha_Cu"] * (dict_param["T"] - 296.15))
                                        * dict_param["L_Cu"] / dict_param["S_Cu"] * dict_param["I"]))

    def output_result(self, tt_end, t_sec, DOD, dict_param, OCV, CCV, Cathode_OCV, Cathode_CCV, Anode_OCV, Anode_CCV,
                      n_line=100, interval=200):
        fig = plt.figure(figsize=(15, 28))

        ax11 = fig.add_subplot(7, 3, 1)
        ax12 = fig.add_subplot(7, 3, 2)
        ax13 = fig.add_subplot(7, 3, 3)
        ax21 = fig.add_subplot(7, 3, 4)
        ax22 = fig.add_subplot(7, 3, 5)
        ax23 = fig.add_subplot(7, 3, 6)
        ax31 = fig.add_subplot(7, 3, 7)
        ax33 = fig.add_subplot(7, 3, 9)
        ax41 = fig.add_subplot(7, 3, 10)
        ax43 = fig.add_subplot(7, 3, 12)
        ax53 = fig.add_subplot(7, 1, 5)
        ax61 = fig.add_subplot(7, 3, 16)
        ax63 = fig.add_subplot(7, 3, 18)
        ax73 = fig.add_subplot(7, 1, 7)

        ims = []
        ax11.plot(DOD[:tt_end], Cathode_OCV[:tt_end], color="gray")
        ax11.plot(DOD[:tt_end], Cathode_CCV[:tt_end], color="gray")
        ax12.plot(DOD[:tt_end], OCV[:tt_end], color="gray")
        ax12.plot(DOD[:tt_end], CCV[:tt_end], color="gray")
        ax13.plot(DOD[:tt_end], Anode_OCV[:tt_end], color="gray")
        ax13.plot(DOD[:tt_end], Anode_CCV[:tt_end], color="gray")

        ax21.plot(t_sec[:tt_end] / 60, Cathode_OCV[:tt_end], color="gray")
        ax21.plot(t_sec[:tt_end] / 60, Cathode_CCV[:tt_end], color="gray")
        ax22.plot(t_sec[:tt_end] / 60, OCV[:tt_end], color="gray")
        ax22.plot(t_sec[:tt_end] / 60, CCV[:tt_end], color="gray")
        ax23.plot(t_sec[:tt_end] / 60, Anode_OCV[:tt_end], color="gray")
        ax23.plot(t_sec[:tt_end] / 60, Anode_CCV[:tt_end], color="gray")

        for ii in range(n_line):
            # for ii in range(1):
            # kk = int(ii*tt_end/n_line)

            kk = np.abs(t_sec[:tt_end] / 60 - max(t_sec[:tt_end] / 60) / n_line * ii).argmin()
            x_grid_num = dict_param["x_grid_num_p"] + dict_param["x_grid_num_sep"] + dict_param["x_grid_num_n"]

            pt111 = ax11.plot(DOD[:kk], Cathode_CCV[:kk], color=self.new_colors[1])
            pt112 = ax11.plot(DOD[:kk], Cathode_OCV[:kk], color="black")
            pt121 = ax12.plot(DOD[:kk], CCV[:kk], color=self.new_colors[1])
            pt122 = ax12.plot(DOD[:kk], OCV[:kk], color="black")
            pt131 = ax13.plot(DOD[:kk], Anode_CCV[:kk], color=self.new_colors[1])
            pt132 = ax13.plot(DOD[:kk], Anode_OCV[:kk], color="black")

            pt211 = ax21.plot(t_sec[:kk] / 60, Cathode_CCV[:kk], color=self.new_colors[1])
            pt212 = ax21.plot(t_sec[:kk] / 60, Cathode_OCV[:kk], color="black")
            pt221 = ax22.plot(t_sec[:kk] / 60, CCV[:kk], color=self.new_colors[1])
            pt222 = ax22.plot(t_sec[:kk] / 60, OCV[:kk], color="black")
            pt231 = ax23.plot(t_sec[:kk] / 60, Anode_CCV[:kk], color=self.new_colors[1])
            pt232 = ax23.plot(t_sec[:kk] / 60, Anode_OCV[:kk], color="black")

            pt311 = ax31.plot(
                (np.arange(dict_param["x_grid_num_p"]) + 0.5) / dict_param["x_grid_num_p"] * dict_param["X_p"] * 1E6,
                np.hstack((self.I_ct_p[0::5][kk], self.I_ct_p[1::5][kk], self.I_ct_p[2::5][kk], self.I_ct_p[3::5][kk],
                           self.I_ct_p[4::5][kk])) * 1E6, color="black")

            pt331 = ax33.plot(
                (np.arange(dict_param["x_grid_num_n"]) + 0.5) / dict_param["x_grid_num_n"] * dict_param["X_n"] * 1E6,
                np.hstack((self.I_ct_n[0::5][kk], self.I_ct_n[1::5][kk], self.I_ct_n[2::5][kk], self.I_ct_n[3::5][kk],
                           self.I_ct_n[4::5][kk])) * 1E6, color="black")

            # pt211 = ax21.bar((np.arange(dict_param["x_grid_num_p"])+0.5)/dict_param["x_grid_num_p"]*dict_param["X_p"]*1E6,
            #                 np.hstack((self.I_ct_p[0::5][kk], self.I_ct_p[1::5][kk], self.I_ct_p[2::5][kk], self.I_ct_p[3::5][kk], self.I_ct_p[4::5][kk]))*1E6,
            #                 width=0.5/dict_param["x_grid_num_p"]*dict_param["X_p"]*1E6, align="center", color=([cm.jet(0/4),cm.jet(1/4),
            #                                                                                                     cm.jet(2/4),cm.jet(3/4),cm.jet(4/4)]))

            # pt231 = ax23.bar((np.arange(dict_param["x_grid_num_n"])+0.5)/dict_param["x_grid_num_n"]*dict_param["X_n"]*1E6,
            #                 np.hstack((self.I_ct_n[0::5][kk], self.I_ct_n[1::5][kk], self.I_ct_n[2::5][kk], self.I_ct_n[3::5][kk], self.I_ct_n[4::5][kk]))*1E6,
            #                 width=0.5/dict_param["x_grid_num_n"]*dict_param["X_n"]*1E6, align="center", color=([cm.jet(0/4),cm.jet(1/4),
            #                                                                                                     cm.jet(2/4),cm.jet(3/4),cm.jet(4/4)]))

            pt411 = ax41.plot(
                (np.arange(dict_param["x_grid_num_p"]) + 0.5) / dict_param["x_grid_num_p"] * dict_param["X_p"] * 1E6,
                np.hstack((self.U_p[0::5][kk], self.U_p[1::5][kk], self.U_p[2::5][kk], self.U_p[3::5][kk],
                           self.U_p[4::5][kk])), color="black")
            pt412 = ax41.plot(
                (np.arange(dict_param["x_grid_num_p"]) + 0.5) / dict_param["x_grid_num_p"] * dict_param["X_p"] * 1E6,
                np.hstack((self.Phi_s_p[0::5][kk], self.Phi_s_p[1::5][kk], self.Phi_s_p[2::5][kk],
                           self.Phi_s_p[3::5][kk], self.Phi_s_p[4::5][kk])), color="red")

            pt431 = ax43.plot(
                (np.arange(dict_param["x_grid_num_n"]) + 0.5) / dict_param["x_grid_num_n"] * dict_param["X_n"] * 1E6,
                np.hstack((self.U_n[0::5][kk], self.U_n[1::5][kk], self.U_n[2::5][kk], self.U_n[3::5][kk],
                           self.U_n[4::5][kk]))[::-1], color=cm.jet(0 / 4))
            pt432 = ax43.plot(
                (np.arange(dict_param["x_grid_num_n"]) + 0.5) / dict_param["x_grid_num_n"] * dict_param["X_n"] * 1E6,
                np.hstack((self.Phi_s_n[0::5][kk], self.Phi_s_n[1::5][kk], self.Phi_s_n[2::5][kk],
                           self.Phi_s_n[3::5][kk], self.Phi_s_n[4::5][kk])), color="red")

            Phi_el_tmp = self.Phi_el[0 + x_grid_num * kk: dict_param["x_grid_num_p"] + x_grid_num * kk]
            Phi_el_tmp = np.hstack((Phi_el_tmp, self.Phi_el[dict_param["x_grid_num_p"] + x_grid_num * kk:dict_param[
                                                                                                             "x_grid_num_p"] +
                                                                                                         dict_param[
                                                                                                             "x_grid_num_sep"] + x_grid_num * kk]))
            Phi_el_tmp = np.hstack((Phi_el_tmp, self.Phi_el[dict_param["x_grid_num_p"] + dict_param[
                "x_grid_num_sep"] + x_grid_num * kk:x_grid_num + x_grid_num * kk]))
            if dict_param["X_p"] != dict_param["X_n"]:
                print("ERROR")
            if dict_param["X_p"] != dict_param["X_el"]:
                print("ERROR")

            pt513 = ax53.plot((np.arange(x_grid_num) + 0.5) * dict_param["X_p"] * 1E6 / dict_param["x_grid_num_n"],
                              Phi_el_tmp, color="black")  # ,color=cm.jet(ii/n_line))

            pt611 = ax61.plot(
                (np.arange(dict_param["r_grid_num_p"]) + 0.5) / dict_param["r_grid_num_p"] * dict_param["L_p"] * 1E6,
                self.C_s_p[0][0 + dict_param["r_grid_num_p"] * kk:10 + dict_param["r_grid_num_p"] * kk],
                color=cm.jet(0 / 4))
            pt612 = ax61.plot(
                (np.arange(dict_param["r_grid_num_p"]) + 0.5) / dict_param["r_grid_num_p"] * dict_param["L_p"] * 1E6,
                self.C_s_p[1][0 + dict_param["r_grid_num_p"] * kk:10 + dict_param["r_grid_num_p"] * kk],
                color=cm.jet(1 / 4))
            pt613 = ax61.plot(
                (np.arange(dict_param["r_grid_num_p"]) + 0.5) / dict_param["r_grid_num_p"] * dict_param["L_p"] * 1E6,
                self.C_s_p[2][0 + dict_param["r_grid_num_p"] * kk:10 + dict_param["r_grid_num_p"] * kk],
                color=cm.jet(2 / 4))
            pt614 = ax61.plot(
                (np.arange(dict_param["r_grid_num_p"]) + 0.5) / dict_param["r_grid_num_p"] * dict_param["L_p"] * 1E6,
                self.C_s_p[3][0 + dict_param["r_grid_num_p"] * kk:10 + dict_param["r_grid_num_p"] * kk],
                color=cm.jet(3 / 4))
            pt615 = ax61.plot(
                (np.arange(dict_param["r_grid_num_p"]) + 0.5) / dict_param["r_grid_num_p"] * dict_param["L_p"] * 1E6,
                self.C_s_p[4][0 + dict_param["r_grid_num_p"] * kk:10 + dict_param["r_grid_num_p"] * kk],
                color=cm.jet(4 / 4))

            pt631 = ax63.plot(
                (np.arange(dict_param["r_grid_num_n"]) + 0.5) / dict_param["r_grid_num_n"] * dict_param["L_n"] * 1E6,
                self.C_s_n[0][0 + dict_param["r_grid_num_n"] * kk:10 + dict_param["r_grid_num_n"] * kk],
                color=cm.jet(0 / 4))
            pt632 = ax63.plot(
                (np.arange(dict_param["r_grid_num_n"]) + 0.5) / dict_param["r_grid_num_n"] * dict_param["L_n"] * 1E6,
                self.C_s_n[1][0 + dict_param["r_grid_num_n"] * kk:10 + dict_param["r_grid_num_n"] * kk],
                color=cm.jet(1 / 4))
            pt633 = ax63.plot(
                (np.arange(dict_param["r_grid_num_n"]) + 0.5) / dict_param["r_grid_num_n"] * dict_param["L_n"] * 1E6,
                self.C_s_n[2][0 + dict_param["r_grid_num_n"] * kk:10 + dict_param["r_grid_num_n"] * kk],
                color=cm.jet(2 / 4))
            pt634 = ax63.plot(
                (np.arange(dict_param["r_grid_num_n"]) + 0.5) / dict_param["r_grid_num_n"] * dict_param["L_n"] * 1E6,
                self.C_s_n[3][0 + dict_param["r_grid_num_n"] * kk:10 + dict_param["r_grid_num_n"] * kk],
                color=cm.jet(3 / 4))
            pt635 = ax63.plot(
                (np.arange(dict_param["r_grid_num_n"]) + 0.5) / dict_param["r_grid_num_n"] * dict_param["L_n"] * 1E6,
                self.C_s_n[4][0 + dict_param["r_grid_num_n"] * kk:10 + dict_param["r_grid_num_n"] * kk],
                color=cm.jet(4 / 4))

            C_el_tmp = self.C_el_p[0 + dict_param["x_grid_num_p"] * kk:5 + dict_param["x_grid_num_p"] * kk]
            C_el_tmp = np.hstack(
                (C_el_tmp, self.C_el_blk[0 + dict_param["x_grid_num_sep"] * kk:5 + dict_param["x_grid_num_sep"] * kk]))
            C_el_tmp = np.hstack(
                (C_el_tmp, self.C_el_n[0 + dict_param["x_grid_num_n"] * kk:5 + dict_param["x_grid_num_n"] * kk][::-1]))

            pt73 = ax73.plot((np.arange(
                dict_param["x_grid_num_p"] + dict_param["x_grid_num_sep"] + dict_param["x_grid_num_n"]) + 0.5) *
                             dict_param["X_p"] * 1E6 / dict_param["x_grid_num_p"],
                             C_el_tmp, color="black")  # ,color=cm.jet(ii/n_line))

            ax11.set_ylabel('Cathode potential [V]', fontsize=12)
            ax12.set_ylabel('Cell voltage [V]', fontsize=12)
            ax13.set_ylabel('Anode potential [V]', fontsize=12)
            ax21.set_ylabel('Cathode potential [V]', fontsize=12)
            ax22.set_ylabel('Cell voltage [V]', fontsize=12)
            ax23.set_ylabel('Anode potential [V]', fontsize=12)
            ax31.set_ylabel('I_ct_p [μA]', fontsize=12)
            ax33.set_ylabel('I_ct_n, [μA]', fontsize=12)
            ax41.set_ylabel('U_p, Phi_s_p [V]', fontsize=12)
            ax43.set_ylabel('U_n, Phi_s_n [V]', fontsize=12)
            ax53.set_ylabel('Electrolyte Potential (0V initial Cel) [V]', fontsize=12)
            ax61.set_ylabel('Concentration of Li [mol/m3]', fontsize=12)
            ax63.set_ylabel('Concentration of Li [mol/m3]', fontsize=12)
            ax73.set_ylabel('Concentration of Li [mol/m3]', fontsize=12)

            ax11.set_xlabel('DOD [%]', fontsize=12)
            ax12.set_xlabel('DOD [%]', fontsize=12)
            ax13.set_xlabel('DOD [%]', fontsize=12)
            ax21.set_xlabel('Time [min]', fontsize=12)
            ax22.set_xlabel('Time [min]', fontsize=12)
            ax23.set_xlabel('Time [min]', fontsize=12)
            ax31.set_xlabel('Distance [μm]', fontsize=12)
            ax33.set_xlabel('Distance [μm]', fontsize=12)
            ax41.set_xlabel('Distance [μm]', fontsize=12)
            ax43.set_xlabel('Distance [μm]', fontsize=12)
            ax53.set_xlabel('Distance [μm]', fontsize=12)
            ax61.set_xlabel('Distance [μm]', fontsize=12)
            ax63.set_xlabel('Distance [μm]', fontsize=12)
            ax73.set_xlabel('Distance [μm]', fontsize=12)

            ax31.set_xlim(0, (dict_param["X_p"]) * 1E6)
            ax33.set_xlim((dict_param["X_n"]) * 1E6, 0)
            ax41.set_xlim(0, (dict_param["X_p"]) * 1E6)
            ax43.set_xlim((dict_param["X_n"]) * 1E6, 0)
            ax61.set_xlim(0, dict_param["L_p"] * 1E6)
            ax63.set_xlim(dict_param["L_p"] * 1E6, 0)
            ax73.set_xlim(0, (dict_param["X_p"] + dict_param["X_el"] + dict_param["X_n"]) * 1E6)

            ax11.set_ylim(3, 4.6)
            ax12.set_ylim(3, 4.6)
            ax13.set_ylim(0, 1.6)
            ax21.set_ylim(3, 4.6)
            ax22.set_ylim(3, 4.6)
            ax23.set_ylim(0, 1.6)
            ax31.set_ylim(-0.2, 0.2)
            ax33.set_ylim(-0.2, 0.2)
            ax41.set_ylim(3, 4.6)
            ax43.set_ylim(0, 1.6)
            ax53.set_ylim(-0.05, 0.05)
            ax73.set_ylim(-500, 2500)

            ax11.tick_params(labelsize=10)
            ax12.tick_params(labelsize=10)
            ax13.tick_params(labelsize=10)
            ax21.tick_params(labelsize=10)
            ax22.tick_params(labelsize=10)
            ax23.tick_params(labelsize=10)
            ax31.tick_params(labelsize=10)
            ax33.tick_params(labelsize=10)
            ax41.tick_params(labelsize=10)
            ax43.tick_params(labelsize=10)
            ax53.tick_params(labelsize=10)
            ax61.tick_params(labelsize=10)
            ax63.tick_params(labelsize=10)
            ax73.tick_params(labelsize=10)

            ax11.grid(True)
            ax12.grid(True)
            ax13.grid(True)
            ax21.grid(True)
            ax22.grid(True)
            ax23.grid(True)
            ax31.grid(True)
            ax33.grid(True)
            ax41.grid(True)
            ax43.grid(True)
            ax53.grid(True)
            ax61.grid(True)
            ax63.grid(True)
            ax73.grid(True)

            pt = (pt111 + pt112 + pt121 + pt122 + pt131 + pt132 +
                  pt211 + pt212 + pt221 + pt222 + pt231 + pt232 +
                  pt311 + pt331 +
                  pt411 + pt412 + pt431 + pt432 +
                  pt513 +
                  pt611 + pt612 + pt613 + pt614 + pt615 + pt631 + pt632 + pt633 + pt634 + pt635 +
                  pt73)
            ims.append(pt)
        ani = animation.ArtistAnimation(fig, ims, interval=interval, blit=True)  # アニメ関数
        ani.save("SimulationResult.mp4", writer="ffmpeg")
        # ani.save('SimulationResult.gif', writer="imagemagick")

    def output_result2(self, tt_end, t_sec, DOD, dict_param, OCV, CCV, Cathode_OCV, Cathode_CCV, Anode_OCV, Anode_CCV,
                       n_line=100, interval=200):
        fig = plt.figure(figsize=(32, 20))

        ax1 = fig.add_subplot(4, 4, 1)
        ax2 = fig.add_subplot(4, 4, 2)
        ax3 = fig.add_subplot(4, 4, 5)
        ax4 = fig.add_subplot(4, 4, 6)
        ax5 = fig.add_subplot(4, 4, 9)
        ax6 = fig.add_subplot(4, 4, 10)
        ax7 = fig.add_subplot(4, 4, 13)
        ax8 = fig.add_subplot(4, 4, 14)

        ax9 = fig.add_subplot(5, 4, 3)
        ax10 = fig.add_subplot(5, 4, 4)
        ax11 = fig.add_subplot(5, 4, 7)
        ax12 = fig.add_subplot(5, 4, 8)
        ax13 = fig.add_subplot(5, 2, 6)
        ax14 = fig.add_subplot(5, 4, 15)
        ax15 = fig.add_subplot(5, 4, 16)
        ax16 = fig.add_subplot(5, 2, 10)

        ims = []
        ax1.plot(t_sec[:tt_end] / 60, OCV[:tt_end], color="gray")
        ax1.plot(t_sec[:tt_end] / 60, CCV[:tt_end], color="gray")
        ax2.plot(DOD[:tt_end], OCV[:tt_end], color="gray")
        ax2.plot(DOD[:tt_end], CCV[:tt_end], color="gray")
        ax3.plot(t_sec[:tt_end] / 60, Cathode_OCV[:tt_end], color="gray")
        ax3.plot(t_sec[:tt_end] / 60, Cathode_CCV[:tt_end], color="gray")
        ax4.plot(DOD[:tt_end], Cathode_OCV[:tt_end], color="gray")
        ax4.plot(DOD[:tt_end], Cathode_CCV[:tt_end], color="gray")
        ax5.plot(t_sec[:tt_end] / 60, Anode_OCV[:tt_end], color="gray")
        ax5.plot(t_sec[:tt_end] / 60, Anode_CCV[:tt_end], color="gray")
        ax6.plot(DOD[:tt_end], Anode_OCV[:tt_end], color="gray")
        ax6.plot(DOD[:tt_end], Anode_CCV[:tt_end], color="gray")
        ax7.plot(t_sec[:tt_end] / 60,
                 (self.I_ct_p[0::5][:tt_end] + self.I_ct_p[1::5][:tt_end] + self.I_ct_p[2::5][:tt_end] + self.I_ct_p[
                                                                                                         3::5][
                                                                                                         :tt_end] + self.I_ct_p[
                                                                                                                    4::5][
                                                                                                                    :tt_end]) * 1E6,
                 color="gray")
        ax8.plot(DOD[:tt_end],
                 (self.I_ct_p[0::5][:tt_end] + self.I_ct_p[1::5][:tt_end] + self.I_ct_p[2::5][:tt_end] + self.I_ct_p[
                                                                                                         3::5][
                                                                                                         :tt_end] + self.I_ct_p[
                                                                                                                    4::5][
                                                                                                                    :tt_end]) * 1E6,
                 color="gray")

        for ii in range(n_line):

            kk = np.abs(t_sec[:tt_end] / 60 - max(t_sec[:tt_end] / 60) / n_line * ii).argmin()
            x_grid_num = dict_param["x_grid_num_p"] + dict_param["x_grid_num_sep"] + dict_param["x_grid_num_n"]

            pt1_1 = ax1.plot(t_sec[:kk] / 60, CCV[:kk], color=self.new_colors[1])
            pt1_2 = ax1.plot(t_sec[:kk] / 60, OCV[:kk], color="black")
            pt2_1 = ax2.plot(DOD[:kk], CCV[:kk], color=self.new_colors[1])
            pt2_2 = ax2.plot(DOD[:kk], OCV[:kk], color="black")

            pt3_1 = ax3.plot(t_sec[:kk] / 60, Cathode_CCV[:kk], color=self.new_colors[1])
            pt3_2 = ax3.plot(t_sec[:kk] / 60, Cathode_OCV[:kk], color="black")
            pt4_1 = ax4.plot(DOD[:kk], Cathode_CCV[:kk], color=self.new_colors[1])
            pt4_2 = ax4.plot(DOD[:kk], Cathode_OCV[:kk], color="black")

            pt5_1 = ax5.plot(t_sec[:kk] / 60, Anode_CCV[:kk], color=self.new_colors[1])
            pt5_2 = ax5.plot(t_sec[:kk] / 60, Anode_OCV[:kk], color="black")
            pt6_1 = ax6.plot(DOD[:kk], Anode_CCV[:kk], color=self.new_colors[1])
            pt6_2 = ax6.plot(DOD[:kk], Anode_OCV[:kk], color="black")

            pt7 = ax7.plot(t_sec[:kk] / 60, (
                    self.I_ct_p[0::5][:kk] + self.I_ct_p[1::5][:kk] + self.I_ct_p[2::5][:kk] + self.I_ct_p[3::5][
                                                                                               :kk] + self.I_ct_p[4::5][
                                                                                                      :kk]) * 1E6,
                           color=self.new_colors[1])
            pt8 = ax8.plot(DOD[:kk], (
                    self.I_ct_p[0::5][:kk] + self.I_ct_p[1::5][:kk] + self.I_ct_p[2::5][:kk] + self.I_ct_p[3::5][
                                                                                               :kk] + self.I_ct_p[4::5][
                                                                                                      :kk]) * 1E6,
                           color=self.new_colors[1])

            # pt8　=　ax8.plot(DOD[:kk],(
            #    self.I_ct_p[0::5][:kk]+self.I_ct_p[1::5][:kk]+self.I_ct_p[2::5][:kk]+self.I_ct_p[3::5][:kk]+self.I_ct_p[4::5][:kk]),color=self.new_colors[1])

            pt9 = ax9.plot(
                (np.arange(dict_param["x_grid_num_p"]) + 0.5) / dict_param["x_grid_num_p"] * dict_param["X_p"] * 1E6,
                np.hstack((self.I_ct_p[0::5][kk], self.I_ct_p[1::5][kk], self.I_ct_p[2::5][kk], self.I_ct_p[3::5][kk],
                           self.I_ct_p[4::5][kk])) * 1E6, color="black")

            pt10 = ax10.plot(
                (np.arange(dict_param["x_grid_num_n"]) + 0.5) / dict_param["x_grid_num_n"] * dict_param["X_n"] * 1E6,
                np.hstack((self.I_ct_n[0::5][kk], self.I_ct_n[1::5][kk], self.I_ct_n[2::5][kk], self.I_ct_n[3::5][kk],
                           self.I_ct_n[4::5][kk])) * 1E6, color="black")

            pt11_1 = ax11.plot(
                (np.arange(dict_param["x_grid_num_p"]) + 0.5) / dict_param["x_grid_num_p"] * dict_param["X_p"] * 1E6,
                np.hstack((self.U_p[0::5][kk], self.U_p[1::5][kk], self.U_p[2::5][kk], self.U_p[3::5][kk],
                           self.U_p[4::5][kk])), color="black")
            pt11_2 = ax11.plot(
                (np.arange(dict_param["x_grid_num_p"]) + 0.5) / dict_param["x_grid_num_p"] * dict_param["X_p"] * 1E6,
                np.hstack((self.Phi_s_p[0::5][kk], self.Phi_s_p[1::5][kk], self.Phi_s_p[2::5][kk],
                           self.Phi_s_p[3::5][kk], self.Phi_s_p[4::5][kk])), color="red")

            pt12_1 = ax12.plot(
                (np.arange(dict_param["x_grid_num_n"]) + 0.5) / dict_param["x_grid_num_n"] * dict_param["X_n"] * 1E6,
                np.hstack((self.U_n[0::5][kk], self.U_n[1::5][kk], self.U_n[2::5][kk], self.U_n[3::5][kk],
                           self.U_n[4::5][kk]))[::-1], color=cm.jet(0 / 4))
            pt12_2 = ax12.plot(
                (np.arange(dict_param["x_grid_num_n"]) + 0.5) / dict_param["x_grid_num_n"] * dict_param["X_n"] * 1E6,
                np.hstack((self.Phi_s_n[0::5][kk], self.Phi_s_n[1::5][kk], self.Phi_s_n[2::5][kk],
                           self.Phi_s_n[3::5][kk], self.Phi_s_n[4::5][kk])), color="red")

            Phi_el_tmp = self.Phi_el[0 + x_grid_num * kk: dict_param["x_grid_num_p"] + x_grid_num * kk]
            Phi_el_tmp = np.hstack((Phi_el_tmp, self.Phi_el[dict_param["x_grid_num_p"] + x_grid_num * kk:dict_param[
                                                                                                             "x_grid_num_p"] +
                                                                                                         dict_param[
                                                                                                             "x_grid_num_sep"] + x_grid_num * kk]))
            Phi_el_tmp = np.hstack((Phi_el_tmp, self.Phi_el[dict_param["x_grid_num_p"] + dict_param[
                "x_grid_num_sep"] + x_grid_num * kk:x_grid_num + x_grid_num * kk]))
            if dict_param["X_p"] != dict_param["X_n"]:
                print("ERROR")
            if dict_param["X_p"] != dict_param["X_el"]:
                print("ERROR")

            pt13 = ax13.plot((np.arange(x_grid_num) + 0.5) * dict_param["X_p"] * 1E6 / dict_param["x_grid_num_n"],
                             Phi_el_tmp, color="black")  # ,color=cm.jet(ii/n_line))

            pt14_1 = ax14.plot(
                (np.arange(dict_param["r_grid_num_p"]) + 0.5) / dict_param["r_grid_num_p"] * dict_param["L_p"] * 1E6,
                self.C_s_p[0][0 + dict_param["r_grid_num_p"] * kk:10 + dict_param["r_grid_num_p"] * kk],
                color=cm.jet(0 / 4))
            pt14_2 = ax14.plot(
                (np.arange(dict_param["r_grid_num_p"]) + 0.5) / dict_param["r_grid_num_p"] * dict_param["L_p"] * 1E6,
                self.C_s_p[1][0 + dict_param["r_grid_num_p"] * kk:10 + dict_param["r_grid_num_p"] * kk],
                color=cm.jet(1 / 4))
            pt14_3 = ax14.plot(
                (np.arange(dict_param["r_grid_num_p"]) + 0.5) / dict_param["r_grid_num_p"] * dict_param["L_p"] * 1E6,
                self.C_s_p[2][0 + dict_param["r_grid_num_p"] * kk:10 + dict_param["r_grid_num_p"] * kk],
                color=cm.jet(2 / 4))
            pt14_4 = ax14.plot(
                (np.arange(dict_param["r_grid_num_p"]) + 0.5) / dict_param["r_grid_num_p"] * dict_param["L_p"] * 1E6,
                self.C_s_p[3][0 + dict_param["r_grid_num_p"] * kk:10 + dict_param["r_grid_num_p"] * kk],
                color=cm.jet(3 / 4))
            pt14_5 = ax14.plot(
                (np.arange(dict_param["r_grid_num_p"]) + 0.5) / dict_param["r_grid_num_p"] * dict_param["L_p"] * 1E6,
                self.C_s_p[4][0 + dict_param["r_grid_num_p"] * kk:10 + dict_param["r_grid_num_p"] * kk],
                color=cm.jet(4 / 4))

            pt15_1 = ax15.plot(
                (np.arange(dict_param["r_grid_num_n"]) + 0.5) / dict_param["r_grid_num_n"] * dict_param["L_n"] * 1E6,
                self.C_s_n[0][0 + dict_param["r_grid_num_n"] * kk:10 + dict_param["r_grid_num_n"] * kk],
                color=cm.jet(0 / 4))
            pt15_2 = ax15.plot(
                (np.arange(dict_param["r_grid_num_n"]) + 0.5) / dict_param["r_grid_num_n"] * dict_param["L_n"] * 1E6,
                self.C_s_n[1][0 + dict_param["r_grid_num_n"] * kk:10 + dict_param["r_grid_num_n"] * kk],
                color=cm.jet(1 / 4))
            pt15_3 = ax15.plot(
                (np.arange(dict_param["r_grid_num_n"]) + 0.5) / dict_param["r_grid_num_n"] * dict_param["L_n"] * 1E6,
                self.C_s_n[2][0 + dict_param["r_grid_num_n"] * kk:10 + dict_param["r_grid_num_n"] * kk],
                color=cm.jet(2 / 4))
            pt15_4 = ax15.plot(
                (np.arange(dict_param["r_grid_num_n"]) + 0.5) / dict_param["r_grid_num_n"] * dict_param["L_n"] * 1E6,
                self.C_s_n[3][0 + dict_param["r_grid_num_n"] * kk:10 + dict_param["r_grid_num_n"] * kk],
                color=cm.jet(3 / 4))
            pt15_5 = ax15.plot(
                (np.arange(dict_param["r_grid_num_n"]) + 0.5) / dict_param["r_grid_num_n"] * dict_param["L_n"] * 1E6,
                self.C_s_n[4][0 + dict_param["r_grid_num_n"] * kk:10 + dict_param["r_grid_num_n"] * kk],
                color=cm.jet(4 / 4))

            C_el_tmp = self.C_el_p[0 + dict_param["x_grid_num_p"] * kk:5 + dict_param["x_grid_num_p"] * kk]
            C_el_tmp = np.hstack(
                (C_el_tmp, self.C_el_blk[0 + dict_param["x_grid_num_sep"] * kk:5 + dict_param["x_grid_num_sep"] * kk]))
            C_el_tmp = np.hstack(
                (C_el_tmp, self.C_el_n[0 + dict_param["x_grid_num_n"] * kk:5 + dict_param["x_grid_num_n"] * kk][::-1]))

            pt16 = ax16.plot((np.arange(
                dict_param["x_grid_num_p"] + dict_param["x_grid_num_sep"] + dict_param["x_grid_num_n"]) + 0.5) *
                             dict_param["X_p"] * 1E6 / dict_param["x_grid_num_p"],
                             C_el_tmp, color="black")  # ,color=cm.jet(ii/n_line))

            ax1.set_ylabel('Cell voltage [V]', fontsize=12)
            ax2.set_ylabel('Cell voltage [V]', fontsize=12)
            ax3.set_ylabel('Cathode potential [V]', fontsize=12)
            ax4.set_ylabel('Cathode potential [V]', fontsize=12)
            ax5.set_ylabel('Anode potential [V]', fontsize=12)
            ax6.set_ylabel('Anode potential [V]', fontsize=12)
            ax7.set_ylabel('I [μA]', fontsize=12)
            ax8.set_ylabel('I [μA]', fontsize=12)
            ax9.set_ylabel('I_ct_p [μA]', fontsize=12)
            ax10.set_ylabel('I_ct_p [μA]', fontsize=12)
            ax11.set_ylabel('U_p, Phi_s_p [V]', fontsize=12)
            ax12.set_ylabel('U_n, Phi_s_n [V]', fontsize=12)
            ax13.set_ylabel('Electrolyte Potential [V]', fontsize=12)
            ax14.set_ylabel('Concentration of Li [mol/m3]', fontsize=12)
            ax15.set_ylabel('Concentration of Li [mol/m3]', fontsize=12)
            ax16.set_ylabel('Concentration of Li [mol/m3]', fontsize=12)

            ax1.set_xlabel('Time [min]', fontsize=12)
            ax2.set_xlabel('DOD [%]', fontsize=12)
            ax3.set_xlabel('Time [min]', fontsize=12)
            ax4.set_xlabel('DOD [%]', fontsize=12)
            ax5.set_xlabel('Time [min]', fontsize=12)
            ax6.set_xlabel('DOD [%]', fontsize=12)
            ax7.set_xlabel('Time [min]', fontsize=12)
            ax8.set_xlabel('DOD [%]', fontsize=12)
            ax9.set_xlabel('Distance [μm]', fontsize=12)
            ax10.set_xlabel('Distance [μm]', fontsize=12)
            ax11.set_xlabel('Distance [μm]', fontsize=12)
            ax12.set_xlabel('Distance [μm]', fontsize=12)
            ax13.set_xlabel('Distance [μm]', fontsize=12)
            ax14.set_xlabel('Distance [μm]', fontsize=12)
            ax15.set_xlabel('Distance [μm]', fontsize=12)
            ax16.set_xlabel('Distance [μm]', fontsize=12)

            ax9.set_xlim(0, (dict_param["X_p"]) * 1E6)
            ax10.set_xlim((dict_param["X_n"]) * 1E6, 0)
            ax11.set_xlim(0, (dict_param["X_p"]) * 1E6)
            ax12.set_xlim((dict_param["X_n"]) * 1E6, 0)
            ax13.set_xlim(0, (dict_param["X_p"] + dict_param["X_el"] + dict_param["X_n"]) * 1E6)
            ax14.set_xlim(0, (dict_param["L_p"]) * 1E6)
            ax15.set_xlim((dict_param["L_n"]) * 1E6, 0)
            ax16.set_xlim(0, (dict_param["X_p"] + dict_param["X_el"] + dict_param["X_n"]) * 1E6)

            ax1.set_ylim(3, 4.6)
            ax2.set_ylim(3, 4.6)
            ax3.set_ylim(3, 4.6)
            ax4.set_ylim(3, 4.6)
            ax5.set_ylim(0, 1.6)
            ax6.set_ylim(0, 1.6)
            ax7.set_ylim(0, max(
                self.I_ct_p[0::5][:tt_end] + self.I_ct_p[1::5][:tt_end] + self.I_ct_p[2::5][:tt_end] + self.I_ct_p[
                                                                                                       3::5][
                                                                                                       :tt_end] + self.I_ct_p[
                                                                                                                  4::5][
                                                                                                                  :tt_end]) * 1.1 * 1E6)
            ax8.set_ylim(0, max(
                self.I_ct_p[0::5][:tt_end] + self.I_ct_p[1::5][:tt_end] + self.I_ct_p[2::5][:tt_end] + self.I_ct_p[
                                                                                                       3::5][
                                                                                                       :tt_end] + self.I_ct_p[
                                                                                                                  4::5][
                                                                                                                  :tt_end]) * 1.1 * 1E6)
            ax9.set_ylim(-1 * max(
                self.I_ct_p[0::5][:tt_end] + self.I_ct_p[1::5][:tt_end] + self.I_ct_p[2::5][:tt_end] + self.I_ct_p[
                                                                                                       3::5][
                                                                                                       :tt_end] + self.I_ct_p[
                                                                                                                  4::5][
                                                                                                                  :tt_end]) * 1.1 * 1E6,
                         max(self.I_ct_p[0::5][:tt_end] + self.I_ct_p[1::5][:tt_end] + self.I_ct_p[2::5][
                                                                                       :tt_end] + self.I_ct_p[3::5][
                                                                                                  :tt_end] + self.I_ct_p[
                                                                                                             4::5][
                                                                                                             :tt_end]) * 1.1 * 1E6)
            ax10.set_ylim(-1 * max(
                self.I_ct_p[0::5][:tt_end] + self.I_ct_p[1::5][:tt_end] + self.I_ct_p[2::5][:tt_end] + self.I_ct_p[
                                                                                                       3::5][
                                                                                                       :tt_end] + self.I_ct_p[
                                                                                                                  4::5][
                                                                                                                  :tt_end]) * 1.1 * 1E6,
                          max(self.I_ct_p[0::5][:tt_end] + self.I_ct_p[1::5][:tt_end] + self.I_ct_p[2::5][
                                                                                        :tt_end] + self.I_ct_p[3::5][
                                                                                                   :tt_end] + self.I_ct_p[
                                                                                                              4::5][
                                                                                                              :tt_end]) * 1.1 * 1E6)

            ax11.set_ylim(3, 4.6)
            ax12.set_ylim(0, 1.6)
            ax16.set_ylim(-500, 2500)

            ax1.tick_params(labelsize=10)
            ax2.tick_params(labelsize=10)
            ax3.tick_params(labelsize=10)
            ax4.tick_params(labelsize=10)
            ax5.tick_params(labelsize=10)
            ax6.tick_params(labelsize=10)
            ax7.tick_params(labelsize=10)
            ax8.tick_params(labelsize=10)
            ax9.tick_params(labelsize=10)
            ax10.tick_params(labelsize=10)
            ax11.tick_params(labelsize=10)
            ax12.tick_params(labelsize=10)
            ax13.tick_params(labelsize=10)
            ax14.tick_params(labelsize=10)
            ax15.tick_params(labelsize=10)
            ax16.tick_params(labelsize=10)

            ax1.grid(True)
            ax2.grid(True)
            ax3.grid(True)
            ax4.grid(True)
            ax5.grid(True)
            ax6.grid(True)
            ax7.grid(True)
            ax8.grid(True)
            ax9.grid(True)
            ax10.grid(True)
            ax11.grid(True)
            ax12.grid(True)
            ax13.grid(True)
            ax14.grid(True)
            ax15.grid(True)
            ax16.grid(True)

            pt = (pt1_1 + pt1_2 + pt2_1 + pt2_2 + pt3_1 + pt3_2 + pt4_1 + pt4_2 + pt5_1 + pt5_2 + pt6_1 + pt6_2 +
                  pt7 + pt8 + pt9 + pt10 + pt11_1 + pt11_2 + pt12_1 + pt12_2 + pt13 +
                  pt14_1 + pt14_2 + pt14_3 + pt14_4 + pt14_5 +
                  pt15_1 + pt15_2 + pt15_3 + pt15_4 + pt15_5 + pt16)
            ims.append(pt)
        ani = animation.ArtistAnimation(fig, ims, interval=interval, blit=True)  # アニメ関数
        ani.save("SimulationResult.mp4", writer="ffmpeg")
        # ani.save('SimulationResult.gif', writer="imagemagick")


class CellDesign():

    def __init__(self):
        self.new_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
                           '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                           '#bcbd22', '#17becf']

    def set_param_dict(self):
        dict_param = dict(C_rate=0.2)

        # Grid parameter
        dict_param.update(x_grid_num_p=5)
        dict_param.update(x_grid_num_sep=5)
        dict_param.update(x_grid_num_n=5)

        dict_param.update(r_grid_num_p=10)
        dict_param.update(r_grid_num_n=10)

        # Grid parameter
        dict_param.update(x_grid_num_p=5)
        dict_param.update(x_grid_num_sep=5)
        dict_param.update(x_grid_num_n=5)

        dict_param.update(r_grid_num_p=10)
        dict_param.update(r_grid_num_n=10)

        dict_param.update(x_p_s=0.2)
        dict_param.update(x_p_e=0.99)
        dict_param.update(x_n_s=0.05)
        dict_param.update(x_n_e=0.999)

        # Time delta
        dict_param.update(dt=0.5)  # [sec]

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
        dict_param.update(X_p=50E-6)  # [m]

        # Electrolyte Dimension
        dict_param.update(L_el=50E-6)  # [m]
        dict_param.update(X_el=50E-6)  # [m]

        # Anode Dimension
        dict_param.update(L_Cu=100E-6)  # [m]
        dict_param.update(X_n=50E-6)  # [m]

        # Charge or Discharge
        # Condition = 'Discharge'
        # if Condition == 'Charge':
        # I = abs(I)*(-1)

        # Diffusion coefficient
        dict_param.update(D_p=0.2E-11)  # [m2/s]
        dict_param.update(D_n=0.2E-11)  # [m2/s]

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
        # Grid
        dict_param.update(dx_el=dict_param["X_el"] / dict_param["x_grid_num_sep"])
        dict_param.update(dx_p=dict_param["X_p"] / dict_param["x_grid_num_p"])
        dict_param.update(dr_p=dict_param["L_p"] / dict_param["r_grid_num_p"])

        # Constant
        dict_param.update(C_s_p_0=dict_param["C_s_max_p"] * df_cell['Cathode x (-)'][0])
        dict_param.update(C_s_n_0=dict_param["C_s_max_n"] * (1 - df_cell['Anode x (-)'][0]))

        # Cathode Dimension
        dict_param.update(V_p=(dict_param["L_p"]) ** 3)
        # 粒子体積

        # Anode Dimension
        dict_param.update(
            V_n=(((max(df_cell['Cathode x (-)']) - min(df_cell['Cathode x (-)'])) * dict_param["C_s_max_p"] *
                  dict_param["V_p"] * dict_param["F"])
                 / ((max(df_cell['Anode x (-)']) - min(df_cell['Anode x (-)'])) * dict_param["C_s_max_n"] * dict_param[
                        "F"])))
        dict_param.update(L_n=(dict_param["V_n"]) ** (1 / 3))  # [m]

        dict_param.update(dx_n=dict_param["X_n"] / dict_param["x_grid_num_n"])
        dict_param.update(dr_n=dict_param["L_n"] / dict_param["r_grid_num_n"])

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
        df_LiC6_OCV = pd.read_csv('LiC6_OCV2.csv')
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
        ax4.set_xticklabels(np.round(CellDesign.re_DOD_norm2(np.array([0, 20, 40, 60, 80, 100]), x_n_s, x_n_e), 3))
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
        ax6.set_xticklabels(np.round(CellDesign.re_DOD_norm2(np.array([0, 20, 40, 60, 80, 100]), x_n_s, x_n_e), 3))
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
