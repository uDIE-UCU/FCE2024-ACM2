import subprocess
from spyci import spyci
from scipy.special import lambertw
import numpy as np
import matplotlib.pyplot as plt


def run_spice(og_path, dest_path, og_params, dest_params, dcname, verbose=False):
    with open(og_path, "r") as f:
        spice_content = f.read()
        spice_content = spice_content.replace(og_params, dest_params)
        spice_content = spice_content.replace("plot", "gnuplot", 2)
        spice_content = spice_content.replace("gnuplot", "plot", 1)
        spice_content = spice_content.replace("dcsweep", dcname)
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
    exp = (Vdd - Vth + sigma * Vdd) / (n * phi_t)
    w = np.exp(exp + 1)
    qs = lambertw(w)
    return qs


def solve_zeta(qs, id, Ish):
    idsat = id / Ish
    zeta = 2 * (qs + 1 - np.sqrt(1 + idsat)) / idsat
    return zeta


def ex_param(
    w=1.0,
    l=1.0,
    Vg_max=3.0,
    Vs_max=3.0,
    Vd_max=3.0,
    Vdd=1.2,
    step=0.01,
    phi_t=0.0258,
    Ibias=1.0,
    hand=False,
    spice=False,
    graph=False,
):
    S = w / l

    og_path_VTH = "./Parametros_Vaf/VTH_tets.spice"
    dest_path_VTH = "./Parametros_Vaf/VTH_test_new.spice"
    og_params_VTH = ".param vg = 3\n.param step = 0.01\n.param phi_t = 0.0258\n.param w = 5.0u\n.param l = 0.18u"
    dest_params_VTH = f".param vg = {Vg_max}\n.param step = {step}\n.param phi_t = {phi_t}\n.param w = {w}u\n.param l = {l}u"

    run_spice(og_path_VTH, dest_path_VTH, og_params_VTH, dest_params_VTH, "VTH_sweep")

    # Load the raw file
    data_vth = spyci.load_raw("VTH_sweep.raw")

    gm_vaf = np.array(get_values(data_vth, "@n1[gm_op]"))
    Vg = np.array(get_values(data_vth, "v(vg)"))
    Id = -np.array(get_values(data_vth, "i(v2)"))

    sim_len = len(Vg)

    gm_Id_vaf = gm_vaf / Id
    gm_Id_vaf_max = max(gm_Id_vaf)
    print(1 / (gm_Id_vaf_max * phi_t))
    nearest_vaf, idx_vaf = find_nearest(gm_Id_vaf, gm_Id_vaf_max / 2)
    err_Vth_vaf = abs(gm_Id_vaf_max / 2 - nearest_vaf)
    Vth_vaf = find_nearest_2(Vg, gm_Id_vaf, gm_Id_vaf_max * 0.531)  # Vg[idx_vaf]
    Ish_vaf = (
        find_nearest_2(Id, gm_Id_vaf, gm_Id_vaf_max * 0.531) * 0.88
    )  # Id[idx_vaf] / S
    Is_vaf = 3 * Ish_vaf.real * S * np.power(10, 6)
    Is_list = [Is_vaf]
    if graph:
        print(
            f"Vth={Vth_vaf.real}, con una diferencia de {err_Vth_vaf}\nIsh={Ish_vaf.real*np.power(10,9)}n\nIs={Is_vaf}"
        )

    if spice:
        gm_Id_ngs = np.array(get_values(data_vth, "gm_id"))
        gm_Id_ngs_max = max(gm_Id_ngs)
        nearest_ngs, idx_ngs = find_nearest(gm_Id_ngs, gm_Id_ngs_max / 2)
        err_Vth_ngs = abs(gm_Id_ngs_max / 2 - nearest_ngs)
        Vth_ngs = find_nearest_2(Vg, gm_Id_ngs, gm_Id_ngs_max / 2)  # Vg[idx_ngs]
        Ish_ngs = (
            find_nearest_2(Id, gm_Id_ngs, gm_Id_ngs_max / 2) / S
        )  # Id[idx_ngs] / S
        Is_ngs = 3 * Ish_ngs.real * S * np.power(10, 6)
        Is_list.append(Is_ngs)
        if graph:
            print(
                f"Vth={Vth_ngs.real}, con una diferencia de {err_Vth_ngs}\nIsh={Ish_ngs.real*np.power(10,9)}n\nIs={Is_ngs}"
            )

    if hand:
        gm = (Id[1:] - Id[: sim_len - 1]) / (Vg[1:] - Vg[: sim_len - 1])
        gm_Id = gm / Id[1:]
        gm_Id_max = max(gm_Id)
        nearest, idx = find_nearest(gm_Id, gm_Id_max / 2)
        err_Vth = abs(gm_Id_max / 2 - nearest)
        Vth = find_nearest_2(Vg[1:], gm_Id, gm_Id_max / 2)  # Vg[idx]
        Ish = find_nearest_2(Id[1:], gm_Id, gm_Id_max / 2) / S  # Id[idx] / S
        Is = 3 * Ish.real * S * np.power(10, 6)
        Is_list.append(Is)
        if graph:
            print(
                f"Vth={Vth.real}, con una diferencia de {err_Vth}\nIsh={Ish.real*np.power(10,9)}n\nIs={Is}"
            )

    n_tuple = ()
    n_list = []

    for i in Is_list:
        og_path_n = "./Parametros_Vaf/n_test.spice"
        dest_path_n = "./Parametros_Vaf/n_test_new.spice"
        og_params_n = ".param vs = 3\n.param step = 0.01\n.param Vdd = 1.8\n.param is = 0.173u\n.param w = 5.0u\n.param l = 0.18u"
        dest_params_n = f".param vs = {Vs_max}\n.param step = {step}\n.param Vdd = {Vdd}\n.param is = {i}u\n.param w = {w}u\n.param l = {l}u"

        run_spice(og_path_n, dest_path_n, og_params_n, dest_params_n, "n_sweep")

        data_n = spyci.load_raw("n_sweep.raw")

        Vs = np.array(get_values(data_n, "v(vs)"))
        Vg_n = np.array(get_values(data_n, "v(vg)"))
        sim_len_n = len(Vs)

        n = (Vs[1:] - Vs[: sim_len_n - 1]) / (Vg_n[1:] - Vg_n[: sim_len_n - 1])
        n = 1 / n
        n_list.append(n)
        n_tuple += (n[-1].real,)
        if graph:
            print(f"n={n[-1].real}")
            plt.plot(Vg_n.real, Vs.real)
            plt.show()

    og_path_sigma = "./Parametros_Vaf/sigma_test.spice"
    dest_path_sigma = "./Parametros_Vaf/sigma_test_new.spice"
    og_params_sigma = ".param vd = 3\n.param vdd = 1.2\n.param Ibias = 1m\n.param step = 0.01\n.param w = 5.0u\n.param l = 0.18u"
    dest_params_sigma = f".param vd = {Vd_max}\n.param vdd = {Vdd}\n.param Ibias = {Ibias}m\n.param step = {step}\n.param w = {w}u\n.param l = {l}u"

    run_spice(
        og_path_sigma,
        dest_path_sigma,
        og_params_sigma,
        dest_params_sigma,
        "sigma_sweep",
    )

    data_sigma = spyci.load_raw("sigma_sweep.raw")
    sigma_graph = np.array(get_values(data_sigma, "sigma"))
    Vd = np.array(get_values(data_sigma, "v(v-sweep)"))
    sigma = sigma_graph[-1].real
    if graph:
        print(f"sigma={sigma}")

    og_path_zeta = "./Parametros_Vaf/zeta_test.spice"
    dest_path_zeta = "./Parametros_Vaf/zeta_test_new.spice"
    og_params_zeta = ".param vdd = 1.2\n.param w = 5.0u\n.param l = 0.18u"
    dest_params_zeta = f".param vdd = {Vdd}\n.param w = {w}u\n.param l = {l}u"

    run_spice(og_path_zeta, dest_path_zeta, og_params_zeta, dest_params_zeta, "zeta_op")
    data_zeta = spyci.load_raw("zeta_op.raw")
    id = get_values(data_zeta, "i(vd)")[0].real
    qs = solve_qs(Vdd, Vth_vaf.real, sigma, n_tuple[0].real, phi_t)
    print(f"qs={qs}")
    print(f"id={id}")
    zeta = solve_zeta(qs, id, Ish_vaf.real).real

    if graph:
        print(f"zeta={zeta}")
        plt.plot(Vg.real, gm_Id_vaf.real)
        if spice:
            plt.plot(Vg.real, gm_Id_ngs.real)
        if hand:
            plt.plot(Vg.real, np.insert(gm_Id, 0, gm_Id[0]))
        plt.show()
        for n in n_list:
            plt.plot(Vg_n[1:].real, n.real)
        plt.show()
        plt.plot(Vd.real, sigma_graph.real)
        plt.show()

    output = (Vth_vaf.real, Ish_vaf.real, n_tuple[0])
    if spice:
        output += (Vth_ngs.real, Ish_ngs.real, n_tuple[1])
        if hand:
            output += (Vth.real, Ish.real, n_tuple[2])
    if hand and not spice:
        output += (Vth.real, Ish.real, n_tuple[1])
    output += (sigma, zeta)
    return output


def new_sigma(w=1.0, l=1.0, Vg_max=0.5, Vdd=1.2, step=0.01, vd_1=0.05, graph=False):
    S = w / l

    og_path_VTH = "./Parametros_Vaf/VTH_tets.spice"
    dest_path_VTH = "./Parametros_Vaf/VTH_test_new.spice"
    og_params_VTH = ".param vg = 3\n.param step = 0.01\n.param phi_t = 0.0258\n.param w = 5.0u\n.param l = 0.18u"
    dest_params_VTH = f".param vg = {Vg_max}\n.param step = {step}\n.param phi_t = {vd_1*2}\n.param w = {w}u\n.param l = {l}u"

    run_spice(og_path_VTH, dest_path_VTH, og_params_VTH, dest_params_VTH, "VTH_sweep")

    # Load the raw file
    data_vth = spyci.load_raw("VTH_sweep.raw")

    Vg = np.array(get_values(data_vth, "v(vg)"))
    Vd_1 = np.array(get_values(data_vth, "v(vd)"))[0]
    Id_1 = -np.array(get_values(data_vth, "i(v2)"))
    lnId_1 = np.log(Id_1)
    sim_len = len(Vg)
    n_array = (
        (1 / 0.026)
        * (Vg[1:] - Vg[: sim_len - 1])
        / (lnId_1[1:] - lnId_1[: sim_len - 1])
    )
    plt.plot(Vg[1:].real, n_array.real)
    plt.xlabel("Vg (V)")
    plt.ylabel("n")
    plt.title("n vs Vg")
    plt.show()
    print(f"n: {min(n_array.real)}")

    for vd in np.arange(0.1, 2.1, 0.1):
        og_path_VTH = "./Parametros_Vaf/VTH_tets.spice"
        dest_path_VTH = "./Parametros_Vaf/VTH_test_new.spice"
        og_params_VTH = ".param vg = 3\n.param step = 0.01\n.param phi_t = 0.0258\n.param w = 5.0u\n.param l = 0.18u"
        dest_params_VTH = f".param vg = {Vg_max}\n.param step = {step}\n.param phi_t = {2*vd}\n.param w = {w}u\n.param l = {l}u"

        run_spice(
            og_path_VTH, dest_path_VTH, og_params_VTH, dest_params_VTH, "VTH_sweep"
        )

        # Load the raw file
        data_vth = spyci.load_raw("VTH_sweep.raw")

        Vd_2 = np.array(get_values(data_vth, "v(vd)"))[0]
        Id_2 = -np.array(get_values(data_vth, "i(v2)"))

        idx = (10e-9) * S
        Vg_1 = find_nearest_2(Vg, Id_1, idx)
        Vg_2 = find_nearest_2(Vg, Id_2, idx)
        new_sigma = (Vg_1 - Vg_2) / (Vd_2.real - Vd_1.real)
        print(
            f"Nuevo valor de sigma: {new_sigma}, con VD1={Vd_1.real}, VD2={Vd_2.real}"
        )
    if graph:
        print(
            f"Para un Id de {idx}A, Vg con phi_t=0.0258 es {Vg_1} y con phi_t=0.5 es {Vg_2}"
        )
        print(f"Nuevo valor de sigma: {new_sigma}")
        plt.plot(Vg.real, Id_1.real, label="phi_t=0.0258")
        plt.plot(Vg.real, Id_2.real, label="phi_t=0.5")
        plt.yscale("log")
        plt.xlabel("Vg (V)")
        plt.ylabel("Id (A)")
        plt.title("Id vs Vg for different phi_t values")
        plt.legend()
        plt.show()
    return Vg, Id_1, Id_2


if __name__ == "__main__":
    # print(ex_param(Vdd=5))
    ex_param(graph=True)
    # new_sigma(vd_1=0.05)
