from qiskit import QuantumCircuit

from qiskit.quantum_info.operators import Operator
from qiskit.aqua.algorithms import Grover

from numpy import pi


def config_circuit(circuit, config_file):
    """
    Config quantum circuit.
    Set scaled distances between data points.
    :param circuit: IBM G circuit object
    :param config_file: file to read configurations from
    """
    # counter for quantum bits
    q = 0

    with open(config_file, 'r') as file:
        for line in file.readlines()[1:]:
            comma = line.index(',')
            comma_2 = line.index(',', comma + 1)
            a = float(line[:comma])
            b = float(line[comma + 1:comma_2])
            phi = float(line[comma_2 + 1:])

            print(q)
            circuit.u3(pi * a, pi * b, pi * phi, q)
            q += 1


def distance(circuit, c_bit, a, b):
    """
    Calculate distances between 2 data points denoted as quantum states.

    Based on DistCalc from  Quantum Machine Learning for data scientists.

    :param circuit: IBM Q circuit object
    """
    # controlled swap operator 6x6
    cswap = Operator([[1, 0, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 0, 1],
                      [0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 1, 0, 0]])

    # |s0> = |0, a, b>
    # 0 - control bit
    # a, b - to find dist between

    circuit.h(c_bit)
    circuit.append(cswap, [c_bit, a, b])
    circuit.h(c_bit)

    # distance between a and b on the control bit
    # circuit.measure(c_bit)


def grovers_search(circuit, n_qubits):
    """
    IBM Q implementation of Grover's search algorithm with multiple solutions
    implemented on 3 qubits.
    Needed to construct simplicial complex for data analysis.
    :param circuit: IBM Q circuit object
    :param n_qubits: number of qubits on the circuit
    """
    circuit.x(0)
    circuit.x(1)
    circuit.x(2)

    circuit.h(0)
    circuit.cx(1, 0)
    circuit.cx(2, 0)

    circuit.h(0)
    circuit.id(1)
    circuit.id(2)

    circuit.x(0)
    circuit.x(1)
    circuit.x(2)

    circuit.h(0)
    circuit.h(1)
    circuit.h(2)


def persistence_homology(circuit, n_qubits):
    """
    Perform quantum persistence homology algorithm,
    :param circuit: IBM Q object
    :param n_qubits: number of qubits on the circuit
    """
    grovers_search(circuit, n_qubits)

