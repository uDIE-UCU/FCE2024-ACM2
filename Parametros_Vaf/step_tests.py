import ex_param
import numpy as np
import matplotlib.pyplot as plt

V_steps = np.arange(0.00025, 0.2001, 0.00025)
(
    Vth_res_vaf,
    Ish_res_vaf,
    n_res_vaf,
    Vth_res_ngs,
    Ish_res_ngs,
    n_res_ngs,
    Vth_res_h,
    Ish_res_h,
    n_res_h,
) = [], [], [], [], [], [], [], [], []
for V in V_steps:
    print(V)
    Vth_vaf, Ish_vaf, n_vaf, Vth_ngs, Ish_ngs, n_ngs, Vth_h, Ish_h, n_h, *extra = (
        ex_param.ex_param(Vg_max=2, step=V, spice=True, hand=True)
    )
    Vth_res_vaf.append(Vth_vaf)
    Ish_res_vaf.append(Ish_vaf)
    n_res_vaf.append(n_vaf)
    Vth_res_ngs.append(Vth_ngs)
    Ish_res_ngs.append(Ish_ngs)
    n_res_ngs.append(n_ngs)
    Vth_res_h.append(Vth_h)
    Ish_res_h.append(Ish_h)
    n_res_h.append(n_h)
plt.figure(figsize=(14, 4))
plt.plot(V_steps, Vth_res_vaf)
plt.plot(V_steps, Vth_res_ngs)
plt.plot(V_steps, Vth_res_h)
plt.show()
plt.plot(V_steps, Ish_res_vaf)
plt.plot(V_steps, Ish_res_ngs)
plt.plot(V_steps, Ish_res_h)
plt.show()
plt.plot(V_steps, n_res_vaf)
plt.plot(V_steps, n_res_ngs)
plt.plot(V_steps, n_res_h)
plt.show()
