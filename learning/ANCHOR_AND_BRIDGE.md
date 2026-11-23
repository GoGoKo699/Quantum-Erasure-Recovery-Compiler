# From stabilizer error correction to graph-constrained recovery

The educational anchor is **Michael A. Nielsen and Isaac L. Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition** (Cambridge University Press, 2010, ISBN 9781107002173). Read the [publisher's edition and contents](https://www.cambridge.org/highereducation/books/quantum-computation-and-quantum-information/01E10196D0A682A6AEFFEA52D53BE9AE/contents/729A1063B8E18926B2B83C43A9D3F892) using the section numbers below.

| Read in Nielsen and Chuang | Use in this project |
|---|---|
| §§2.1.9, 2.2.8 and 2.4.3 | Compute local Pauli commutators and reduce the encoded Bell state to the reference and surviving sites. |
| §§8.2.2–8.2.4 and 10.3.1 | Treat recovery as a channel on an unknown input and separate perfect correctability from the resources required to implement it. |
| §§10.4.2 and 10.5.1–10.5.3 | Read the CSS and stabilizer descriptions, track Clifford conjugation and retain the signs contributed by Pauli measurements. |
| §§10.5.6–10.5.8 | Compare the benchmark codes and standard decoding circuits with a graph-constrained decoder after losses. |
| §§3.2.2–3.2.3 | Distinguish routing for a supplied representative pair from the complexity of choosing the pair. |

## Translate the notation

The reference $`R`$ is half of a Bell pair. Encode the other half. A code stabilizer acts trivially on $`R`$, while encoded logical $`X`$ and $`Z`$ become Choi stabilizers when paired with $`X_R`$ and $`Z_R`$. On losing a site, retain the stabilizer products with identity at that site before restricting to the survivors. A product can survive even when its individual generators have nonidentity factors at an erased site.

The phase-free Pauli label at a vertex is $`(x_v,z_v)`$. The commutation contribution for two such labels is

```math
a_v(P,Q)=x_v(P)z_v(Q)+z_v(P)x_v(Q)\pmod 2.
```

Retain the local contributions even when their sum is zero. The reference contributes one, so the graph vertices contribute an odd parity. A CNOT can toggle both endpoints of a graph edge. The exact compiler chooses a cheapest set of toggles that leaves a single anticommutation, at the output. Use the [worked example](WORKED_EXAMPLE.md) to see how compatible Pauli measurements and feedforward finish the recovery.

## Follow the applications

The [30 milestones](MILESTONES.md) develop the circuit and the converse, then return to the benchmarks. The [projective-line example](../science/benchmarks.md#projective-line-recovery) uses the two CSS logical axes to determine exactly which couplers the receiver needs and connects those costs to the filtered-channel capacity.

For research background on stabilizer normal forms, decoding and code examples, see the [Gottesman research supplement](GOTTESMAN_BRIDGE.md).
