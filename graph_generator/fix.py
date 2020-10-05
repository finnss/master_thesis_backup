import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def fix():
    print('rho\tphi\tpsi')
    for rho in [0.01, 0.5, 1]:
        for phi in [0.01, 0.5, 1]:
            den = phi + rho
            psi = str(round(rho / (1/phi + rho), 3)) if den > 0 else ' '
            # print('%s & %s & %s \\\\' % (phi if rho == 0.1 else '', rho, psi))
            print('%s\t%s\t%s' % (rho, phi, psi))
        # print('\Xhline{1pt}')


def smith_kraemer(rho, phi):
    return round(rho / (1/phi + rho), 3)


def viz():
    max_phi = 2
    n_values_to_test = 100
    total_matrix = np.array([np.zeros(n_values_to_test)
                             for i in range(n_values_to_test)])

    for i in range(1, n_values_to_test + 1):
        rho = i / n_values_to_test
        for j in range(1, n_values_to_test + 1):
            phi = j * max_phi / n_values_to_test

            psi = smith_kraemer(rho, phi)
            total_matrix[i - 1][j - 1] = psi
    fig = plt.figure()
    ax = fig.add_subplot(111)
    total_matrix_2 = np.flip(total_matrix, 0)
    plt.style.use('bmh')
    print('plt.style.available')
    print(plt.style.available)
    toshow = ax.matshow(total_matrix_2, extent=[
                        0, max_phi, 0, 1], aspect=1.5, cmap=plt.cm.get_cmap('afmhot'))
    colorbar = fig.colorbar(toshow, fraction=0.03, shrink=1)
    colorbar.set_label('ψ', rotation=0)
    plt.gca().xaxis.tick_bottom()
    # ax.set_xticklabels(['']+alpha)
    # ax.set_yticklabels(['']+alpha)
    ax.set_ylabel('ρ', rotation=0)
    ax.set_xlabel('ϕ')

    plt.show()


def viz2():
    plt.style.use('seaborn-whitegrid')
    phi_1 = 0.02
    phi_2 = 1.86

    x = np.arange(0, 1, 0.01)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    psi_1 = [smith_kraemer(k, phi_1) for k in x]
    psi_2 = [smith_kraemer(k, phi_2) for k in x]
    plt.plot(x, psi_1, label="ϕ = 0.02")
    plt.plot(x, psi_2, label="ϕ = 1.86")
    ax.set_ylabel('ψ', rotation=0)
    ax.set_xlabel('ρ')
    plt.legend()
    plt.show()


# fix()
# viz()
viz2()
