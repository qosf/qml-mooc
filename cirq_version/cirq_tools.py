import cmath
import matplotlib.pyplot as plt
import numpy as np
import shutil
import subprocess
from cirq.contrib.qcircuit.qcircuit_diagram import circuit_to_latex_using_qcircuit
from pylatex import Document, NoEscape, Package
from qutip import Bloch
from tempfile import mkdtemp

def plot_circuit(circuit):
    tex = circuit_to_latex_using_qcircuit(circuit)
    doc = Document(documentclass='standalone',
                   document_options=NoEscape('border=25pt,convert={density=300,outext=.png}'))
    doc.packages.append(Package('amsmath'))
    doc.packages.append(Package('qcircuit'))
    doc.append(NoEscape(tex))
    tmp_folder = mkdtemp()
    doc.generate_tex(tmp_folder + '/circuit')
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


def plot_histogram(counts):
    x = np.arange(len(counts))
    plt.bar(x, counts.values())
    plt.xticks(x, counts.keys())
    plt.show()
