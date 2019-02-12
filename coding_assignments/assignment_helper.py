import itertools
import numpy as np
import socket
import subprocess
from pyquil.api import ForestConnection


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


def get_amplitudes(circuit):
    if isinstance(circuit, qiskit.circuit.quantumcircuit.QuantumCircuit):
        backend = BasicAer.get_backend('statevector_simulator')
        job = execute(circuit, backend)
        amplitudes = job.result().get_statevector(circuit)
    elif isinstance(circuit, pyquil.quil.Program):
        wf_sim = WavefunctionSimulator(connection=fc)
        wavefunction = wf_sim.wavefunction(circuit)
        amplitudes = wavefunction.amplitudes
    else:
        raise ValueError("Unknown circuit type")
    return amplitudes


def get_counts(circuit, num_shots=100):
    if isinstance(circuit, qiskit.circuit.quantumcircuit.QuantumCircuit):
        backend = BasicAer.get_backend('qasm_simulator')
        job = execute(circuit, backend, shots=num_shots)
        result = job.result()
        counts = result.get_counts(circuit)
    elif isinstance(circuit, pyquil.quil.Program):
        n_qubits = len(circuit.get_qubits())
        circuit.wrap_in_numshots_loop(num_shots)
        qc = get_qc(str(n_qubits) + 'q-qvm', connection=fc)
        executable = qc.compile(circuit)
        result = qc.run(executable)
        classical_bits = get_classical_bits(circuit)
        counts = {}
        for bitstring in itertools.product(*[{1, 0} for _ in range(classical_bits)]):
            key = "".join(str(i) for i in bitstring)
            value = sum([tuple(d.tolist()) == bitstring for d in result])
            counts[key] = value
    else:
        raise ValueError("Unknown circuit type")
    return counts


def get_single_measurement_counts(circuit, num_shots=100):
    if isinstance(circuit, qiskit.circuit.quantumcircuit.QuantumCircuit):
        backend = BasicAer.get_backend('qasm_simulator')
        job = execute(circuit, backend, shots=num_shots)
        result = job.result()
        counts = result.get_counts(circuit)
    elif isinstance(circuit, pyquil.quil.Program):
        n_qubits = len(circuit.get_qubits())
        circuit.wrap_in_numshots_loop(num_shots)
        qc = get_qc(str(n_qubits) + 'q-qvm', connection=fc)
        executable = qc.compile(circuit)
        result = qc.run(executable)
        classical_bits = get_classical_bits(circuit)
        counts = {}
        for bitstring in itertools.product(*[{1, 0} for _ in range(classical_bits)]):
            key = "".join(str(i) for i in bitstring)
            counts[key] = 0
        counts["0" * classical_bits] = (result == 0).sum()
        counts["0" * (classical_bits-1) + "1"] = (result == 1).sum()
    else:
        raise ValueError("Unknown circuit type")
    return counts


def get_classical_bits(circuit):
    if isinstance(circuit, qiskit.circuit.quantumcircuit.QuantumCircuit):
        classical_bits = circuit.cregs[0].size
    elif isinstance(circuit, pyquil.quil.Program):
        for instruction in circuit.instructions:
            if isinstance(instruction, pyquil.quilbase.Declare):
                classical_bits = instruction.memory_size
                break
    else:
        raise ValueError("Unknown circuit type")
    return classical_bits


def get_circuit_length(circuit):
    if isinstance(circuit, qiskit.circuit.quantumcircuit.QuantumCircuit):
        program_length = sum(circuit.count_ops().values())
    elif isinstance(circuit, pyquil.quil.Program):
        program_length = len(circuit.instructions)
    else:
        raise ValueError("Unknown circuit type")
    return program_length


if __name__ == "__main__":
    try:
        import grove
        import pyquil
        from grove.pyvqe import vqe
        from pyquil import Program, get_qc
        from pyquil.paulis import PauliSum, PauliTerm, exponential_map, sZ
        from pyquil.api import WavefunctionSimulator
        from pyquil.gates import *
        try:
            qvm_server, quilc_server, fc = init_qvm_and_quilc()
            is_forest = True
        except FileNotFoundError:
            try:
                prefix = "/home/local/bin/"
                qvm_server, quilc_server, fc = init_qvm_and_quilc(prefix+"qvm",
                                                                  prefix + "quilc")
                is_forest = True
            except FileNotFoundError:
                is_forest = False
    except ImportError:
        is_forest = False
    try:
        import qiskit
        from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
        from qiskit import execute, BasicAer
        from qiskit.quantum_info import Pauli
        from qiskit_aqua import Operator, get_aer_backend
        from qiskit_aqua.components.initial_states import Custom
        is_qiskit = True
    except ImportError:
        is_qiskit = False
    try:
        import dimod
        import dwave_networkx
        import minorminer
        is_dwave = True
    except ImportError:
        is_dwave = False
    if not (is_qiskit or is_forest):
        raise RuntimeError("No quantum computing framework available!")
    if not is_dwave:
        raise RuntimeError("D-Wave Ocean is not available!")
    print("Available frameworks:")
    if is_forest:
        print("Forest SDK")
    if is_qiskit:
        print("Qiskit")
    if is_dwave:
        print("D-Wave Ocean")
