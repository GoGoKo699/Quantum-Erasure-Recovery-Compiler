# Quantum Erasure Recovery Compiler

**How many CNOTs does it take to recover an unknown encoded qubit after known losses?** Given a one-qubit stabilizer encoding, a loss pattern and a hardware graph, the compiler returns a minimum-cost recovery to a designated physical site. It preserves entanglement with an untouched reference.

For each surviving pair of logical Pauli representatives, let $`A`$ be the sites where they anticommute locally. If $`o`$ is the output site, find a cheapest edge set whose odd-degree vertices are $`A\triangle\{o\}`$. Such an edge set is called a *T-join*. Minimizing its cost over the representative pairs gives the exact answer.

```math
\mathrm{Opt}(o)
=\min_{P,Q} c_G\bigl(A(P,Q)\triangle\{o\}\bigr).
```

The compiler applies one CNOT per selected edge, followed by single-qubit measurements and output corrections. The converse tracks the same local anticommutation through every nonzero branch of an adaptive stabilizer decoder. Edge weights are nonnegative. Single-qubit stabilizer operations, resets and classical feedforward are free. The cost counts post-erasure CNOTs, with no preshared ancillary entanglement.

| Recovery instance | Minimum CNOT count at unit edge cost |
|---|---:|
| A representative pair anticommutes just at the output | 0 |
| Five-qubit code after two flagged losses, all-to-all graph, output at a survivor | 1 |
| Same code, three survivors at $`0,L,2L`$ on a line and output at $`0`$ | $`L`$ |
| Projective-plane CSS code after a full line of $`q+1`$ sites survives, all-to-all survivor graph | $`q/2`$ |

Finding a cheapest T-join for a fixed pair is a polynomial-time matching problem. Choosing the best pair is NP-complete in its decision form, even on an all-to-all graph. The [reference compiler](verification/README.md) is intended for exact small-instance studies.

For projective-line erasures, the same cost rule gives an optimal static hardware design. When erased sites are unavailable, exactly $`(q^2+q+1)q/2`$ installed couplers suffice to recover on every full line with $`q/2`$ active CNOTs and a survivor output chosen from the flag. See [projective-line recovery](science/benchmarks.md#projective-line-recovery) for the hardware result and [Correlated Erasure Capacity](https://github.com/GoGoKo699/Correlated-Erasure-Capacity) for the channel.

## Run the recovery

1. **Compile from the flag.** Supply the [signed stabilizer tableau](verification/README.md#inputs) of the one-qubit encoding, the erased sites, the available weighted couplers and the output site. The compiler finds the surviving logical Pauli pairs, computes the cheapest parity join for each, and selects a pair and join before any quantum measurement. If no feasible pair and join exist, it reports `NoRecovery`.
2. **Run the selected gates.** Apply local Cliffords and one CNOT per selected edge, following the [forest from leaves to roots](science/theorem.md#from-an-edge-set-to-a-circuit). Prepare or reset relay qubits only where the hardware input and tracked operators permit it. Erased sites require explicitly available replacement qubits and couplers.
3. **Read and correct.** Measure the specified Pauli on each needed non-output site, XOR the specified outcome bits with the recorded sign offset for each correction, and apply the conditional single-qubit corrections on the output. Every measurement record of nonzero probability returns the unknown qubit with its reference correlations.

The [worked recovery](learning/WORKED_EXAMPLE.md) follows the gates, measurements and output correction. The weighted objective counts CNOTs after the erasure. Classical compilation and local operations have separate implementation costs. The [reference solver](verification/README.md) is for exact small instances.

## Read the science

| Question | Where to start |
|---|---|
| What does recovery return, and which operations are available? | [Model](science/model.md) |
| How do local commutation and graph parity give the exact cost? | [Compiler and converse](science/theorem.md) |
| Which part of the classical search is hard? | [Complexity](science/complexity.md) |
| How do losses and placement affect familiar codes? | [Benchmarks](science/benchmarks.md) |
| Which ingredients come from earlier work? | [Related work](science/related-work.md) and [bibliography](references/bibliography.bib) |

## Learn and reproduce

The educational anchor is Nielsen and Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition. Start with the [source bridge](learning/ANCHOR_AND_BRIDGE.md), then follow the [30-milestone map](learning/MILESTONES.md) or the [worked recovery](learning/WORKED_EXAMPLE.md). Run the [compiler and verification suite](verification/README.md) for finite checks of the proofs and examples.

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).
