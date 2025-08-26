import ex_param
import numpy as np
import matplotlib.pyplot as plt


def general_test():
    V_steps = np.arange(0.00025, 0.2001, 0.00025)
    (
        Vth_res_va,
        Ish_res_va,
        n_res_va,
        Vth_res_ngs,
        Ish_res_ngs,
        n_res_ngs,
        Vth_res_h,
        Ish_res_h,
        n_res_h,
        ceros,
    ) = [], [], [], [], [], [], [], [], [], []
    for V in V_steps:
        print(V)
        (
            Vth_va,
            Ish_va,
            n_va,
            Vth_ngs,
            Ish_ngs,
            n_ngs,
            Vth_h,
            Ish_h,
            n_h,
            *extra,
        ) = ex_param.ex_param(Vg_max=2, step=V, spice=True, hand=True)
        Vth_res_va.append(Vth_va)
        Ish_res_va.append(Ish_va)
        n_res_va.append(n_va)
        Vth_res_ngs.append(Vth_ngs)
        Ish_res_ngs.append(Ish_ngs)
        n_res_ngs.append(n_ngs)
        Vth_res_h.append(Vth_h)
        Ish_res_h.append(Ish_h)
        n_res_h.append(n_h)
        if Vth_ngs <= 0.25:
            ceros.append([V, Vth_ngs])
    print(ceros)
    plt.figure(figsize=(14, 4))
    plt.plot(V_steps, Vth_res_va, label="Vth va")
    plt.plot(V_steps, Vth_res_ngs, label="Vth ngs")
    plt.plot(V_steps, Vth_res_h, label="Vth hand")
    plt.legend()
    plt.show()
    plt.plot(V_steps, Ish_res_va, label="Ish va")
    plt.plot(V_steps, Ish_res_ngs, label="Ish ngs")
    plt.plot(V_steps, Ish_res_h, label="Ish hand")
    plt.legend()
    plt.show()
    plt.plot(V_steps, n_res_va, label="n va")
    plt.plot(V_steps, n_res_ngs, label="n ngs")
    plt.plot(V_steps, n_res_h, label="n hand")
    plt.legend()
    plt.show()


def hand_test(max_compare=False):
    V_steps = np.arange(0.00025, 0.2001, 0.00025)
    Vth_res, Ish_res, n_res, id_res, vg_res = [], [], [], [], []
    Vth_max, Ish_max, n_max, Vth_min, Ish_min, n_min = [], [], [], [], [], []
    for V in V_steps:
        print(V)
        resultados = ex_param.ex_param(Vg_max=2, step=V, hand=True)
        Vth_res.append(resultados[3])
        Ish_res.append(resultados[4])
        n_res.append(resultados[5])
        id_res.append(resultados[8])
        vg_res.append(resultados[9])
    for i in range(len(V_steps) - 1):
        if Vth_res[i - 1] < Vth_res[i] and Vth_res[i + 1] < Vth_res[i]:
            Vth_max.append(V_steps[i])
            latest_max = i
        if Vth_res[i - 1] > Vth_res[i] and Vth_res[i + 1] > Vth_res[i]:
            Vth_min.append(V_steps[i])
            latest_min = i
        if Ish_res[i - 1] < Ish_res[i] and Ish_res[i + 1] < Ish_res[i]:
            Ish_max.append(V_steps[i])
        if Ish_res[i - 1] > Ish_res[i] and Ish_res[i + 1] > Ish_res[i]:
            Ish_min.append(V_steps[i])
        if n_res[i - 1] < n_res[i] and n_res[i + 1] < n_res[i]:
            n_max.append(V_steps[i])
        if n_res[i - 1] > n_res[i] and n_res[i + 1] > n_res[i]:
            n_min.append(V_steps[i])
    if max_compare:
        if Vth_max == Ish_max:
            print("Los máximos de Vth y Ish coinciden")
        else:
            print("Los máximos de Vth y Ish coinciden por:")
            for i in Vth_max:
                if i not in Ish_max:
                    print(f"Máximo de Vth en {i}, pero no en Ish")
            for i in Ish_max:
                if i not in Vth_max:
                    print(f"Máximo de Ish en {i}, pero no en Vth")
        if Vth_min == Ish_min:
            print("Los mínimo de Vth y Ish coinciden")
        else:
            print("Los mínimo de Vth y Ish coinciden por:")
            for i in Vth_min:
                if i not in Ish_min:
                    print(f"Mínimo de Vth en {i}, pero no en Ish")
            for i in Ish_min:
                if i not in Vth_min:
                    print(f"Mínimo de Ish en {i}, pero no en Vth")
        if Vth_max == n_max:
            print("Los máximos de Vth y n coinciden")
        else:
            print("Los máximos de Vth y n coinciden por:")
            for i in Vth_max:
                if i not in n_max:
                    print(f"Máximo de Vth en {i}, pero no en n")
            for i in n_max:
                if i not in Vth_max:
                    print(f"Máximo de n en {i}, pero no en Vth")
        if Vth_min == n_min:
            print("Los mínimo de Vth y n coinciden")
        else:
            print("Los mínimo de Vth y n coinciden por:")
            for i in Vth_min:
                if i not in n_min:
                    print(f"Mínimo de Vth en {i}, pero no en n")
            for i in n_min:
                if i not in Vth_min:
                    print(f"Mínimo de n en {i}, pero no en Vth")
        if n_max == Ish_max:
            print("Los máximos de n y Ish coinciden")
        else:
            print("Los máximos de n y Ish coinciden por:")
            for i in n_max:
                if i not in Ish_max:
                    print(f"Máximo de n en {i}, pero no en Ish")
            for i in Ish_max:
                if i not in n_max:
                    print(f"Máximo de Ish en {i}, pero no en n")
        if n_min == Ish_min:
            print("Los mínimo de n y Ish coinciden")
        else:
            print("Los mínimo de n y Ish coinciden por:")
            for i in n_min:
                if i not in Ish_min:
                    print(f"Mínimo de Vth en {i}, pero no en Ish")
            for i in Ish_min:
                if i not in n_min:
                    print(f"Mínimo de Ish en {i}, pero no en Vth")
    plt.plot(np.arange(0, 3.01, V_steps[latest_max]), vg_res[latest_max])
    plt.plot(np.arange(0, 3.01, V_steps[latest_min]), vg_res[latest_min])
    plt.legend()
    plt.show()
    plt.plot(np.arange(0, 3.01, V_steps[latest_max]), id_res[latest_max])
    plt.plot(np.arange(0, 3.01, V_steps[latest_max]), id_res[latest_min])
    plt.legend()
    plt.show()
    plt.plot(V_steps, Vth_res)
    plt.show()
    plt.plot(V_steps, Ish_res)
    plt.show()
    plt.plot(V_steps, n_res)
    plt.show()


if __name__ == "__main__":
    general_test()
