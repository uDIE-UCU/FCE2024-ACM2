import subprocess
from spyci import spyci
import numpy as np
import matplotlib.pyplot as plt


def run_spice(og_path, dest_path, og_params, dest_params, verbose=False):
    with open(og_path, "r") as f:
        spice_content = f.read()
        spice_content = spice_content.replace(og_params, dest_params)
        spice_content = spice_content.replace("plot", "gnuplot", 2)
        spice_content = spice_content.replace("gnuplot", "plot", 1)
    with open(dest_path, "w") as f:
        f.write(spice_content)

    result = subprocess.run(
        f"ngspice -b {dest_path}", shell=True, capture_output=True, text=True
    )
    if verbose:
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)


def get_idx(raw_data, var_name):
    for var in raw_data["vars"]:
        if var["name"] == var_name:
            return var["idx"]


def get_values(raw_data, var_name):
    idx = int(get_idx(raw_data, var_name))
    values = []
    for i in raw_data["values"]:
        values.append(i[idx])
    return values


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx], idx


def ex_param(w=5, l=0.18, Vg_max=3, Vs_max=3, Vdd=1.2, step=0.01, phi_t=0.0258):
    S = w / l

    og_path_VTH = "./Parametros_Psp/VTH_test.spice"
    dest_path_VTH = "./Parametros_Psp/VTH_test_new.spice"
    og_params_VTH = ".param vg = 3\n.param step = 0.01\n.param phi_t = 0.0258\n.param w = 5.0u\n.param l = 0.18u"
    dest_params_VTH = f".param vg = {Vg_max}\n.param step = {step}\n.param phi_t = {phi_t}\n.param w = {w}u\n.param l = {l}u"

    run_spice(og_path_VTH, dest_path_VTH, og_params_VTH, dest_params_VTH, True)

    # Load the raw file
    data_vth = spyci.load_raw("dcsweep.raw")

    Id = -np.array(get_values(data_vth, "i(v2)"))
    Vg = np.array(get_values(data_vth, "v(vg)"))

    sim_len = len(Id)

    gm = (Id[1:] - Id[: sim_len - 1]) / (Vg[1:] - Vg[: sim_len - 1])
    gm_Id = gm / Id[1:]
    gm_Id_max = max(gm_Id)
    nearest, idx = find_nearest(gm_Id, gm_Id_max / 2)
    err_Vth = abs(gm_Id_max / 2 - nearest)
    Vth = Vg[idx + 1]
    Ish = Id[idx + 1] / S
    print(f"{Vth}, {err_Vth}, {Ish.real*np.power(10,9)}n")
    Is = 3 * Ish.real * S * np.power(10, 6)
    print(Is)

    # og_path_n = "./Parametros_Psp/n_test.spice"
    # dest_path_n = "./Parametros_Psp/n_test_new.spice"
    # og_params_n = ".param vs = 3\n.param step = 0.01\n.param Vdd = 1.8\n.param is = 0.173u\n.param w = 5.0u\n.param l = 0.18u"
    # dest_params_n = f".param vs = {Vs_max}\n.param step = {step}\n.param Vdd = {Vdd}\n.param is = {Is}u\n.param w = {w}u\n.param l = {l}u"

    # run_spice(og_path_n, dest_path_n, og_params_n, dest_params_n)

    # data_n = spyci.load_raw("dcsweep.raw")

    # Vs = np.array(get_values(data_n, "v(vs)"))
    # Vg_n = np.array(get_values(data_n, "v(vg)"))
    # sim_len = len(Vs)

    # n = (Vs[1:] - Vs[: sim_len - 1]) / (Vg_n[1:] - Vg_n[: sim_len - 1])
    # n = 1 / n
    # plt.figure(figsize=(14, 4))
    # plt.plot(Vg_n[1:].real, n.real)
    # plt.show()
    # plt.plot(Vg_n.real, Vs.real)
    # plt.show()


ex_param()
ex_param(w=1, l=1)
