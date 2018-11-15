import numpy as np
import matplotlib.pyplot as plt

from qiskit import QuantumRegister, QuantumCircuit, ClassicalRegister
from qiskit.wrapper import execute as q_execute
from qiskit.tools.qi.pauli import Pauli
from qiskit.tools.apps.optimization import eval_hamiltonian
from qiskit_aqua.operator import Operator
from qiskit_aqua import get_initial_state_instance
from qiskit import Aer
from qiskit.tools.qi.qi import state_fidelity

from scipy.optimize import minimize
from functools import reduce
import itertools


class QAOA:
    def __init__(self, mixer_hamiltonian, cost_hamiltonian, quantum_register, 
                 circuit_init, n_gamma_nu=2):
        self.n_qubits = mixer_hamiltonian.num_qubits
        self.Hm = mixer_hamiltonian
        self.Hc = cost_hamiltonian
        self.circuit_init = circuit_init
        self.n_gamma_nu = n_gamma_nu
        self.qr = quantum_register
        
        self.nu_init = np.random.uniform(0, np.pi*2, n_gamma_nu)  # initial nu
        self.gamma_init = np.random.uniform(0, np.pi*2, n_gamma_nu)  # initial gamma
        
    def evolve(self, hamiltonian, angle):
        return hamiltonian.evolve(None, angle, 'circuit', 1,
                              quantum_registers=self.qr,
                              expansion_mode='suzuki',
                              expansion_order=3)
                              
    def create_circuit(self, gamma, nu):
        circuit_evolv = reduce(lambda x,y: x+y, 
                               [self.evolve(self.Hm, nu[i]) + \
                                self.evolve(self.Hc, gamma[i])
                                for i in range(self.n_gamma_nu)])
        circuit = self.circuit_init + circuit_evolv
        return circuit
        
    def optimize(self, maxiter=20):
        def evaluate_circuit(gamma_nu):
            n = len(gamma_nu)//2
            circuit = self.create_circuit(gamma_nu[:n], gamma_nu[n:])
            
            return np.real(self.Hc.eval("matrix", circuit, 'statevector_simulator')[0]) # the value should always be real in theory, but for numerical reasons the imaginary part can be a very small number
        
        gamma_nu = np.concatenate([self.gamma_init, self.nu_init])
        result = minimize(evaluate_circuit, gamma_nu, method='Nelder-Mead', options={'maxiter':maxiter})
        
        circuit = self.create_circuit(result['x'][:self.n_gamma_nu], result['x'][self.n_gamma_nu:])
        
        return circuit, result
