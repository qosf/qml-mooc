import cmath
import itertools
import matplotlib.pyplot as plt
import numpy as np
import shutil
import socket
import subprocess
from pyquil.api import ForestConnection
from pyquil.latex import to_latex
from qutip import Bloch
from tempfile import mkdtemp


def get_free_port():
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port


def init_qvm_and_quilc(qvm_executable="qvm", quilc_executable="quilc"):
    qvm_port = get_free_port()
    quilc_port = get_free_port()
    qvm_server = subprocess.Popen([qvm_executable, "-S", "-p", str(qvm_port)])
    quilc_server = subprocess.Popen([quilc_executable, "-S", "-p", str(quilc_port)])
    fc = ForestConnection(sync_endpoint='http://127.0.0.1:' + str(qvm_port),
                          compiler_endpoint='http://127.0.0.1:' + str(quilc_port))
    return qvm_server, quilc_server, fc


def plot_circuit(circuit):
    latex_diagram = to_latex(circuit)
    tmp_folder = mkdtemp()
    with open(tmp_folder + '/circuit.tex', 'w') as f:
        f.write(latex_diagram)
    proc = subprocess.Popen(['pdflatex', '-shell-escape', tmp_folder + '/circuit.tex'], cwd=tmp_folder)
    proc.communicate()
    image = plt.imread(tmp_folder + '/circuit.png')
    shutil.rmtree(tmp_folder)
    plt.axis('off')
    return plt.imshow(image)


def get_vector(alpha, beta):
    """
    Function to compute 3D Cartesian coordinates
    from 2D qubit vector.
    """

    # get phases
    angle_alpha = cmath.phase(alpha)
    angle_beta = cmath.phase(beta)

    # avoiding wrong normalization due to rounding errors
    if cmath.isclose(angle_alpha, cmath.pi):
        angle_alpha = 0
    if cmath.isclose(angle_beta, cmath.pi):
        angle_beta = 0

    if (angle_beta < 0 and angle_alpha < angle_beta) or (angle_beta > 0 and angle_alpha > angle_beta):
            denominator = cmath.exp(1j*angle_beta)
    else:
            denominator = cmath.exp(1j*angle_alpha)

    # eliminate global phase
    alpha_new = alpha/denominator
    beta_new = beta/denominator

    # special case to avoid division by zero
    if abs(alpha) == 0 or abs(beta) == 0:
        if alpha == 0:
            return [0,0,-1]
        else:
            return [0,0,1]
    else:
        # compute theta and phi from alpha and beta
        theta = 2*cmath.acos(alpha_new)
        phi = -1j*cmath.log(beta_new/cmath.sin(theta/2))

        # compute the Cartesian coordinates
        x = cmath.sin(theta)*cmath.cos(phi)
        y = cmath.sin(theta)*cmath.sin(phi)
        z = cmath.cos(theta)

    return [x.real, y.real, z.real]


def plot_quantum_state(amplitudes):
    """
    Thin function to abstract the plotting on the Bloch sphere.
    """
    bloch_sphere = Bloch()
    vec = get_vector(amplitudes[0], amplitudes[1])
    bloch_sphere.add_vectors(vec)
    bloch_sphere.show()
    bloch_sphere.clear()


def plot_histogram(result):
    if isinstance(result, dict):
        outcomes = np.vstack(result.values()).T
    else:
        outcomes = result
    trials, classical_bits = outcomes.shape
    stats = {}
    for bits in itertools.product('01', repeat=classical_bits):
        stats["".join(str(bit) for bit in bits)] = 0
    for i in range(trials):
        stats["".join(str(bit) for bit in outcomes[i])] += 1
    x = np.arange(len(stats))
    plt.bar(x, stats.values())
    plt.xticks(x, stats.keys())
    plt.show()
