# Recovery after a flagged erasure

A quantum memory encodes one logical qubit into a stabilizer block. After the location of each erased qubit is known, the task is to deliver the original state to a designated physical qubit by using the hardware couplers that remain available. The input may be entangled with an inaccessible reference. The recovery therefore has to implement an identity channel from the logical input to the physical output.

## Physical resources

The instance specifies a stabilizer encoding isometry, an erasure set, an undirected hardware graph, nonnegative edge costs, and a designated output vertex. Each vertex of the graph is an available qubit location. The graph includes the surviving data qubits and any empty locations explicitly supplied for local ancillas. An erased location is usable only if the model includes a replacement qubit there and retains its couplers. A CNOT executed along edge $e$ costs $w_e$ and acts on the two qubits at its endpoints. Either orientation is possible at the same cost by conjugating with single-qubit Hadamards.

Single-qubit Cliffords, single-qubit Pauli measurements, discard, classical processing and feedforward, and reset to a single-qubit stabilizer state are free. Initially empty positions can host product stabilizer ancillas. There is one qubit per vertex, so extra work qubits require specified additional positions. A gate across two positions uses a graph edge even when both positions are in the same device module. The reference has no hardware vertex and is never acted on. There is no additional shared entanglement. The input encoding is supplied and the budget counts only the weighted CNOTs after the erasure is announced.

The cost of a deterministic, possibly adaptive decoder is the maximum transcript cost among outcomes of nonzero probability on the encoded Bell input. Exact recovery makes the measurement transcript independent of the logical state, so this cost also describes the decoder on every logical input. In fact the lower bound below holds individually in each nonzero successful transcript. This is an ideal circuit model with noiseless gates and measurements. No distribution on erasure locations is needed.

## Surviving Choi stabilizers

Let $R$ be the reference, $D$ the encoded block, and $E$ the erased subset of $D$. Write $A=D\setminus E$ for the surviving data locations and $V$ for the hardware vertex set. If the encoder is $W$, the normalized Choi state before loss is $(I_R\otimes W)|\Phi^+\rangle$, a pure stabilizer state. Let $\mathcal S_E$ be the signed stabilizer group of the reduced state on $R A$. It is obtained by keeping the original stabilizers with identity on every erased qubit and restricting them to the surviving coordinates. This follows directly from the Pauli expansion of the stabilizer projector, since every nonidentity one-qubit Pauli has trace zero.

For $P,Q\in\mathcal S_E$, define $a_v(P,Q)$ to be one when the Pauli factors at $v$ anticommute and zero otherwise. Put $a_v=0$ at an initially empty location. Signs play no role in $a_v$, but are retained for the final measurement corrections. A pair is admissible if $a_R(P,Q)=1$. One may choose $P_R=X$ and $Q_R=Z$ up to sign when enumerating admissible pairs. Any independent pair of reference Pauli factors spans the same two-dimensional space over $\mathbb F_2$, and changing the basis preserves the local commutation bit at every site.

The set of physical sites with $a_v=1$ has odd cardinality. Indeed, $P$ and $Q$ commute globally, while their factors on $R$ anticommute. With output $o$, define the even terminal set
```math
T(P,Q;o)=\{v\in V : a_v(P,Q)=1\}\mathbin{\triangle}\{o\},
```
where $\triangle$ is symmetric difference. An edge set $F$ is a $T$-join if its vertices of odd degree are exactly $T$. Write $\tau_G(T)$ for the minimum sum of edge costs over such sets, with value $+\infty$ if there is no join.

An erasure is correctable with unrestricted connectivity exactly when an admissible pair exists. For necessity, the Pauli expansion of the reduced Choi state must contain all three nonidentity reference axes, because a channel on the physical system cannot create any missing reference axis in this expansion. The reference restrictions of $\mathcal S_E$ form a linear space, so the condition is equivalent to finding two independent axes. Sufficiency follows from the [compiler](theorem.md) on the complete graph, where every even terminal set admits a join. Restricted connectivity can rule out particular outputs or increase the cost for a correctable erasure.

[Exact compiler](theorem.md) · [Classical compilation complexity](complexity.md) · [Examples](benchmarks.md) · [Related work](related-work.md)
