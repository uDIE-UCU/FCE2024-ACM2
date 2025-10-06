import subprocess
from spyci import spyci
import scipy.stats as stats
from scipy.special import lambertw
import numpy as np
import matplotlib.pyplot as plt


def run_spice(og_path, dest_path, og_params, dest_params, verbose=False):
    with open(og_path, "r") as f:
        spice_content = f.readlines()
        spice_new = ""
        for line in spice_content:
            if not (line.startswith("setplot") or line.startswith("plot")):
                spice_new += line
        spice_new = spice_new.replace(og_params, dest_params)
    with open(dest_path, "w") as f:
        f.write(spice_new)

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


def find_nearest_2(array_x, array_y, value_y):
    if len(array_y) == len(array_x):
        idx = find_nearest(array_y, value_y)[1]
        if np.abs(value_y - array_y[idx - 1]) > np.abs(value_y - array_y[idx - 1]):
            idx_start, idx_end = idx + 1, idx
        else:
            idx_start, idx_end = idx, idx - 1
        value_diff = value_y - array_y[idx_start]
        linear_diff = array_y[idx_end] - array_y[idx_start]
        value_x = array_x[idx_start] + (array_x[idx_end] - array_x[idx_start]) * (
            value_diff / linear_diff
        )
        return value_x
    else:
        print("arrays must be of same length")
        return 0


def solve_qs(Vdd, Vth, sigma, n, phi_t):
    expon = (Vdd - Vth + sigma * Vdd) / (n * phi_t)
    w = np.exp(expon + 1)
    qs = lambertw(w)
    return qs


def solve_zeta(qs, id, Ish):
    idsat = id / Ish
    zeta = 2 * (qs + 1 - np.sqrt(1 + idsat)) / idsat
    return zeta


def ex_param(
    Vg_max=3,
    Vs_min=2,
    Vs_max=3,
    Vdd=5,
    sVd1=0.05,
    sVd2=1,
    step=0.01,
    phi_t=0.0258,
    graph=False,
):
    w = 138
    l = 7.8
    S = w / l

    og_path_VTH = "./Parametros_ALD/VTH_test_v2.spice"
    dest_path_VTH = "./Parametros_ALD/VTH_test_new_v2.spice"
    og_params_VTH = ".param vg = 3\n.param step = 0.01\n.param phi_t = 0.0258"
    dest_params_VTH = (
        f".param vg = {Vg_max}\n.param step = {step}\n.param phi_t = {phi_t}"
    )

    run_spice(og_path_VTH, dest_path_VTH, og_params_VTH, dest_params_VTH)

    # Load the raw file
    data_vth = spyci.load_raw("dcsweep_v2.raw")

    Id_ALD = np.array(get_values(data_vth, "i(@m.xm1.m1[id])"))
    Id_ALD = Id_ALD.real
    Vg_ALD = np.array(get_values(data_vth, "v(vg)"))
    Vg_ALD = Vg_ALD.real
    sim_len = len(Id_ALD)
    Gm_ALD = (np.log(Id_ALD[2:]) - np.log(Id_ALD[: sim_len - 2])) / (
        Vg_ALD[2:] - Vg_ALD[: sim_len - 2]
    )
    Gm_ALD = np.append(Gm_ALD, Gm_ALD[-1])
    Gm_ALD = np.insert(Gm_ALD, 0, Gm_ALD[0])
    Gm_ALD_max = max(Gm_ALD)
    Vth_ALD = find_nearest_2(Vg_ALD, Gm_ALD, Gm_ALD_max / 2).real
    Ish_ALD = find_nearest_2(Id_ALD, Gm_ALD, Gm_ALD_max / 2).real / S
    Is_ALD = 3 * Ish_ALD.real * S * np.power(10, 6)
    print(f"Vth={Vth_ALD}, Ish={Ish_ALD}")

    if graph:
        plt.plot(Vg_ALD, Gm_ALD)
        plt.show()

    og_path_n = "./Parametros_ALD/n_test.spice"
    dest_path_n = "./Parametros_ALD/n_test_new.spice"
    og_params_n = ".param vsi = 3\n.param vsf = 3\n.param step = 0.01\n.param Vdd = 1.8\n.param is = 0.173u"
    dest_params_n = f".param vsi = {Vs_min}\n.param vsf = {Vs_max}\n.param step = {step}\n.param Vdd = {Vdd}\n.param is = {Is_ALD}u"

    run_spice(og_path_n, dest_path_n, og_params_n, dest_params_n)

    data_n = spyci.load_raw("dcsweep.raw")

    Vs = np.array(get_values(data_n, "v(vs)"))
    Vg_n = np.array(get_values(data_n, "v(vg)"))
    sim_len = len(Vs)

    n = (Vs[1:] - Vs[: sim_len - 1]) / (Vg_n[1:] - Vg_n[: sim_len - 1])
    n = 1 / n
    (n_reg, *rest) = stats.linregress(Vs.real, Vg_n.real)
    print(f"n={n[-1].real}")
    print(f"n_reg={n_reg}")
    straight_n = n_reg * Vs + rest[0]
    if graph:
        plt.figure(figsize=(14, 4))
        plt.plot(Vg_n[1:].real, n.real)
        plt.show()
        plt.plot(Vs.real, Vg_n.real)
        plt.plot(Vs.real, straight_n.real)
        plt.show()

    sigma_Vd = [sVd1, sVd2]
    sigma_Vg = []
    for sVd in sigma_Vd:
        og_path_sigma = "./Parametros_ALD/VTH_test_v2.spice"
        dest_path_sigma = "./Parametros_ALD/VTH_test_new_v2.spice"
        og_params_sigma = ".param vg = 3\n.param step = 0.01\n.param phi_t = 0.0258"
        dest_params_sigma = (
            f".param vg = {Vg_max}\n.param step = {step}\n.param phi_t = {sVd*2}"
        )

        run_spice(og_path_sigma, dest_path_sigma, og_params_sigma, dest_params_sigma)

        # Load the raw file
        data_sigma = spyci.load_raw("dcsweep_v2.raw")
        Vg_sigma = np.array(get_values(data_sigma, "v(vg)"))
        Id_sigma = np.array(get_values(data_sigma, "i(@m.xm1.m1[id])"))
        id_goal = 10e-9 * S
        sVg = find_nearest_2(Vg_sigma, Id_sigma, id_goal).real
        sigma_Vg.append(sVg)
        print(f"sigma_Vd={sVd}, sigma_Vg={sVg}")
    sigma = (sigma_Vg[0] - sigma_Vg[1]) / (sigma_Vd[1] - sigma_Vd[0])
    print(f"sigma={sigma}")

    og_path_zeda = "./Parametros_ALD/zeta_test.spice"
    dest_path_zeda = "./Parametros_ALD/zeta_test_new.spice"
    og_params_zeda = ".param vdd = 5"
    dest_params_zeda = f".param vdd = {Vdd}"

    run_spice(og_path_zeda, dest_path_zeda, og_params_zeda, dest_params_zeda)
    data_zeda = spyci.load_raw("dcsweep.raw")

    Id_zeda = np.array(get_values(data_zeda, "i(@m.xm1.m1[id])"))[0].real
    print(f"Id_zeda={Id_zeda}")

    qs = solve_qs(Vdd, Vth_ALD, sigma, n_reg, phi_t)
    zeta = solve_zeta(qs, Id_zeda, Ish_ALD)
    print(f"qs={qs}, zeta={zeta}")


if __name__ == "__main__":
    ex_param(graph=True)
