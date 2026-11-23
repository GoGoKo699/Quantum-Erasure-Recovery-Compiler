# Learning milestones

The first 12 milestones establish the stabilizer, erasure and hardware model. The next 18 connect local commutation to the graph compiler, its converse and its limits. Use the [Nielsen and Chuang source bridge](ANCHOR_AND_BRIDGE.md) for the selected reading sections.

## Background and preliminaries

### M01 Pauli labels

**Question.** How are one-site Pauli axes represented by two bits?

**Understanding target.** Read the phase-free label and keep the sign as separate data.

**Builds on.** [Bridge](ANCHOR_AND_BRIDGE.md)

### M02 Local commutation

**Question.** When do two Pauli factors conflict on one qubit?

**Understanding target.** Calculate the binary symplectic product of a local pair.

**Builds on.** [Bridge](ANCHOR_AND_BRIDGE.md)

### M03 Global commutation

**Question.** How can globally commuting strings conflict locally?

**Understanding target.** Add the local contributions modulo two and keep their individual values.

**Builds on.** M02, [Model](../science/model.md)

### M04 Stabilizer states

**Question.** How does a signed commuting group specify a state?

**Understanding target.** Distinguish a pure maximal group from a mixed stabilizer projector.

**Builds on.** M03, [Model](../science/model.md)

### M05 Encoded Paulis

**Question.** Why can a single logical Pauli have many physical representatives?

**Understanding target.** Relate the code normalizer to multiplication by code stabilizers.

**Builds on.** M04, [Model](../science/model.md)

### M06 Reference test

**Question.** Why is a Bell reference enough to test exact arbitrary-input recovery?

**Understanding target.** Identify the normalized Choi state and the two Bell stabilizers.

**Builds on.** M04–05, [Model](../science/model.md)

### M07 Encoded correlations

**Question.** Which stabilizers contain the logical information in the Choi state?

**Understanding target.** Separate code-only stabilizers from the reference X and Z cosets.

**Builds on.** M05–06, [Model](../science/model.md)

### M08 Flagged loss

**Question.** What information does the loss flag reveal?

**Understanding target.** Distinguish known unavailable sites from any measurement on the surviving data.

**Builds on.** M06, [Model](../science/model.md)

### M09 Shortening

**Question.** Which encoded correlations survive a partial trace?

**Understanding target.** Form products that are identity on the erased sites, then restrict them.

**Builds on.** M04, M07–08, [Model](../science/model.md)

### M10 Local measurement

**Question.** What can an ideal single-site Pauli measurement change?

**Understanding target.** Track the compatible subgroup and the new signed local generator.

**Builds on.** M03–04, [Theorem](../science/theorem.md)

### M11 CNOT conjugation

**Question.** How does a CNOT move X and Z factors between its sites?

**Understanding target.** Predict both local factors and signs under conjugation.

**Builds on.** M02–03, [Example](WORKED_EXAMPLE.md)

### M12 Recovery model

**Question.** Which operations and resources define the optimization?

**Understanding target.** Combine the exact-channel target, hardware, loss, reset and gate-cost rules.

**Builds on.** M06–11, [Model](../science/model.md)

## Compiler and scientific results

### M13 Anticommutation set

**Question.** Why do surviving reference pairs have an odd physical support of local anticommutation?

**Understanding target.** Account for the reference site in the global parity sum.

**Builds on.** M03, M07, M09, [Theorem](../science/theorem.md)

### M14 Bell objective

**Question.** Which physical parity pattern permits local readout to finish recovery?

**Understanding target.** Explain why the target has a single anticommutation at the output.

**Builds on.** M06–07, M10, [Theorem](../science/theorem.md)

### M15 Terminal set

**Question.** Which hardware vertices must change parity?

**Understanding target.** Form the symmetric difference of the original anticommutation set and the output.

**Builds on.** M13–14, [Theorem](../science/theorem.md)

### M16 Feasible edges

**Question.** When can a fixed hardware graph realize the desired parity change?

**Understanding target.** Use even terminal count in each connected component.

**Builds on.** M12, M15, [Theorem](../science/theorem.md)

### M17 Weighted matching

**Question.** How does a cheapest parity edge set reduce to terminal pairing?

**Understanding target.** Use shortest-path distances, matching and cancellation of duplicate edges.

**Builds on.** M15–16, [Complexity](../science/complexity.md)

### M18 Acyclic optimum

**Question.** Why can the chosen parity edge set be a forest?

**Understanding target.** Delete cycles without changing the odd-degree vertices or increasing cost.

**Builds on.** M17, [Theorem](../science/theorem.md)

### M19 Moving across an edge

**Question.** How does one CNOT move anticommutation to a compatible neighbor?

**Understanding target.** Choose local Pauli axes and identify the role of reset on an identity site.

**Builds on.** M10–11, M13, [Theorem](../science/theorem.md)

### M20 Cancelling across an edge

**Question.** How does one CNOT remove two neighboring anticommutations?

**Understanding target.** Conjugate the two matching local Pauli products to compatible factors.

**Builds on.** M11, M13, [Example](WORKED_EXAMPLE.md)

### M21 Forest sweep

**Question.** Why does each leaf-to-root step have a usable active child?

**Understanding target.** Read the current marker from the boundary of the unprocessed edges.

**Builds on.** M16, M18–20, [Theorem](../science/theorem.md)

### M22 Measurement and correction

**Question.** How do local records turn the final correlations into a Bell pair?

**Understanding target.** Measure the compatible tails and convert their outcome parities into output Pauli corrections.

**Builds on.** M10, M14, M21, [Example](WORKED_EXAMPLE.md)

### M23 Adaptive branch

**Question.** Why must every nonzero transcript produce the exact answer?

**Understanding target.** Use purity of the target Choi marginal and positivity of the branch mixture.

**Builds on.** M06, M12, [Theorem](../science/theorem.md)

### M24 Backward lifting

**Question.** Why can measurement and reset contribute no parity change in the converse?

**Understanding target.** Lift through each free operation using compatible old stabilizers or identity factors.

**Builds on.** M09–10, M23, [Theorem](../science/theorem.md)

### M25 Exact optimum

**Question.** How do the proof and compiler certify the same global cost?

**Understanding target.** Read paid edge toggles from a branch, then minimize over all eligible representative pairs.

**Builds on.** M15–24, [Theorem](../science/theorem.md)

### M26 Five-qubit benchmark

**Question.** How does moving three survivors apart change CNOT cost?

**Understanding target.** Use the fixed anticommutation set after two losses and compare graph distances.

**Builds on.** M09, M15, M25, [Benchmarks](../science/benchmarks.md)

### M27 Limits of auxiliary processing

**Question.** Why does the Smolin witness give a stronger converse, and how does Steane differ?

**Understanding target.** Use separability across even cuts for the witness and flexible representatives for Steane.

**Builds on.** M16, M23, M25–26, [Benchmarks](../science/benchmarks.md)

### M28 Classical hardness

**Question.** Why does efficient matching fail to make full compilation polynomial?

**Understanding target.** Explain the reversible reduction from a binary syndrome to supported reference Pauli pairs.

**Builds on.** M05, M09, M17, M25, [Complexity](../science/complexity.md)

### M29 Checking a circuit

**Question.** Which parts of an exact finite result can a circuit certificate verify?

**Understanding target.** Check the surviving generators, parity edge set, gate count and corrected reference correlations.

**Builds on.** M21–25, [Verification](../verification/README.md)

### M30 Physical conclusion

**Question.** How do the surviving correlations determine the cost of restoring one encoded qubit?

**Understanding target.** Connect correctability, the choice of representative and the hardware graph. Use projective lines to distinguish the CNOTs executed per mask from the couplers installed to serve the whole mask law.

**Builds on.** M25–29, [Model](../science/model.md), [Projective-line recovery](../science/benchmarks.md#projective-line-recovery), [Complexity](../science/complexity.md)
