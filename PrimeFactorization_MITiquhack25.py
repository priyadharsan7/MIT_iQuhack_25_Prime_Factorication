from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.circuit.library import QFT
import numpy as np
import time

simulator = Aer.get_backend('qasm_simulator')

def shors_algorithm(A, N,n):
    m = N.bit_length()
    qc = QuantumCircuit(n + m, n)
    qc.h(range(n))

    for i in range(n):
        power = pow(A, 2**i, N)
        for j in range(m):
            if (power >> j) & 1:
                qc.cx(i, n + j)
    qc.append(QFT(n).inverse(), range(n))
    qc.measure(range(n), range(n))
    compiled_circuit = transpile(qc, simulator)
    sim_result = simulator.run(compiled_circuit, shots=1024).result()
    counts = sim_result.get_counts()
    y = int(max(counts, key=counts.get), 2)
    if y==0:
        r=0
    else :
        r = 2**n // y  

    return r,qc

N = eval (input("Enter number"))
Stime=time.time()
n=min(int(np.log2(N)/2),24)
A=2
while (True):
    r,q = shors_algorithm(A, N,n)
    print("Using the guess: ",A)
    if r % 2 == 0:
        factor1 = np.gcd(pow(A,r//2)- 1, N)
        factor2 = np.gcd(pow(A,r//2) + 1, N)
        if factor2!=1 and factor1!=1:
            if factor1*factor2==N:
                Etime=time.time()
                print("Time elapsed",Etime-Stime)
                print(factor1,factor2)
                break
    A+=int(np.log2(N)/2)
