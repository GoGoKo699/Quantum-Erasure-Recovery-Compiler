# Gottesman research supplement

Daniel Gottesman, *Stabilizer Codes and Quantum Error Correction*, Caltech PhD thesis, [arXiv:quant-ph/9705052v1](https://arxiv.org/abs/quant-ph/9705052v1), submitted in 1997, gives the stabilizer research background for this project. Section numbers refer to that version. Start the learning route with the [Nielsen and Chuang source bridge](ANCHOR_AND_BRIDGE.md).

| Read in Gottesman | Transfer to this project |
|---|---|
| Sections 2.3–2.4, quantum codes and error models | Correctability concerns the correlations retained after the known erased set is discarded. |
| Sections 3.2 and 3.4, stabilizer codes and alternate languages | Keep binary commutation contributions separately at each site. |
| Sections 4.1–4.3, encoding and decoding | Compare standard-form decoding with a post-loss optimization on a separate hardware graph. |
| Section 5.2 and Appendix A, measurement and gates | Track the generator added by a Pauli measurement and the conjugation of local Paulis by CNOT. |
| Sections 8.2 and 8.6, five-qubit and CSS codes | Use the five-qubit code for the hardware comparison and CSS states for the complexity construction. |

## Translate the notation

Gottesman describes a code by its stabilizer $`S`$ and logical Pauli representatives in the normalizer. Here a reference qubit $`R`$ remains untouched. A code stabilizer acts trivially on $`R`$. An encoded logical $`X`$ or $`Z`$ becomes a state stabilizer when paired with the same Pauli on $`R`$. This turns channel recovery into preservation of two correlations.

The phase-free part of a local Pauli has binary $`(x,z)`$ labels. Global commutation adds the site contributions modulo two. Keep each contribution for the graph argument.

```math
a_v(P,Q)=x_v(P)z_v(Q)+z_v(P)x_v(Q)\pmod{2}.
```

Form the surviving stabilizer by choosing products of generators that are identity on every lost site and then restricting those products. Two original generators with the same nonidentity factor at a lost site may have a product that survives.

## Follow the new step

The reference contributes one local anticommutation, so an odd number of hardware sites contribute the same. A CNOT can toggle both endpoints of its edge. After the graph sweep only the output has a nonzero contribution. The remaining local Pauli factors are compatible and can be measured while retaining both correlations. Their signs determine the output correction.

Use the [worked example](WORKED_EXAMPLE.md) to propagate a pair forward, then [the branch converse](../science/theorem.md) to follow the final Bell correlations backward. The [milestone map](MILESTONES.md) connects the gate rule, graph optimum and complexity result.
