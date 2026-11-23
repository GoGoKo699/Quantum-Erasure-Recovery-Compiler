# Decoder costs for standard codes

A comparison specifies the erased sites, which hardware remains available, the output location, and the edge costs. Here each used edge operation costs one unless otherwise stated. The erasure labels are known. A resettable erased site supplies a fresh product ancilla and does not restore the discarded state.

Write $`A`$ for the local anticommutation set of a surviving logical Pauli pair. The compiler minimizes the cost of a $`T`$-join for $`T=A\triangle\{o\}`$, where $`o`$ is the designated output. In particular, when $`T`$ has two vertices, its minimum cost is their shortest-path distance, with infinite distance when they are disconnected.

## The five-qubit code after two erasures

The conventional $`[[5,1,3]]`$ code has generators $`XZZXI, IXZZX, XIXZZ, ZXIXZ`$ and encoded Pauli operators $`XXXXX`$ and $`ZZZZZ`$. Every nonidentity stabilizer has weight four. After erasing any two physical qubits, the shortened Choi stabilizer on the reference and three survivors has two independent generators, one for each reference axis.

Indeed, erasure correctability guarantees a representative for each logical axis on the survivors. There is at most one representative per axis, since the ratio of two representatives for the same axis would be a physical stabilizer supported on three sites. Each nonidentity logical Pauli representative has weight at least three by the code distance. The $`X`$ and $`Z`$ representatives therefore have nonidentity factors at all three survivors. Their product also has logical weight three, so the two factors differ and anticommute at every survivor.

For any survivor output, $`T`$ consists of the other two survivors. With unit costs, the exact values are as follows.

| Available hardware | Output | Minimum CNOT count |
| --- | --- | ---: |
| Complete graph on the survivors | Any survivor | 1 |
| Path on three consecutive surviving sites | An endpoint | 1 |
| Path on three consecutive surviving sites | The middle site | 2 |
| Path with survivors at $`0,L,2L`$ and available intermediate sites | $`0`$ or $`2L`$ | $`L`$ |
| Path with survivors at $`0,L,2L`$ and available intermediate sites | $`L`$ | $`2L`$ |

For the original five-site path, one can also count over all 30 choices of a lost pair and a survivor output.

| Treatment of the two lost sites | Cost 1 | Cost 2 | Cost 3 | Cost 4 | Infeasible |
| --- | ---: | ---: | ---: | ---: | ---: |
| Remove the vertices and their incident edges | 12 | 3 | 0 | 0 | 15 |
| Keep the vertices as resettable sites | 12 | 9 | 6 | 3 | 0 |

For resettable sites, a non-output pair at separation $`d`$ has $`5-d`$ possible locations and three possible survivor outputs. For removed sites, twelve adjacent pairs give cost one. Cost two requires the output to occupy the middle of the non-output pair's path, which can happen in three ways.

## Arbitrary local operations on a generalized Smolin state

The five-qubit reduced Choi state is locally Clifford equivalent to the four-qubit Smolin state. More generally, let $`M`$ be a set of $`2k-1`$ marked physical sites with $`k\ge 2`$. Put the generalized Smolin state on $`R\cup M`$. Use the stabilizer convention

```math
\rho_{RM}=2^{-2k}(I+X^{\otimes 2k})(I+Z^{\otimes 2k}).
```

Each tensor power runs over the reference and all marked physical sites. The reference marginal is maximally mixed, and the state is a valid reduced Choi benchmark. The projector has rank $`2^{2k-2}`$, so a stabilizer purification uses $`2k-2`$ additional qubits. One way to obtain it is to map the two displayed stabilizers to two single-qubit $`Z`$ generators by a Clifford, purify the remaining maximally mixed qubits with Bell pairs, and undo that Clifford on $`RM`$. The pure state has one ebit across the reference, and stabilizer decoding on the physical side puts it into an encoded Bell form. Erasing the purifying qubits recovers $`\rho_{RM}`$.

The exact cost is the minimum $`T`$-join for $`T=M\triangle\{o\}`$. For this family it holds even when each paid edge can implement an arbitrary two-site operation and local instruments need not be Clifford. The upper bound is the Clifford compiler. The lower bound uses separability.

When either side of a cut has an even number of marks, counting the reference as marked, the restrictions of the uniform $`X`$ and $`Z`$ strings commute on each side. In their local common eigenbases, both generators have product eigenvectors and the state is diagonal. Thus the input is separable across that cut, also after adjoining product ancillas.

In any nonzero transcript of an exact decoder, form the graph of paid edges used by that transcript. If a component away from the output has an odd number of physical marks, the cut with that component and the reference on one side has an even number of marks and separates reference from output. Every operation on the transcript is local to one side of the cut, with possible classical feed-forward. Conditioning such a separable operation on a transcript preserves separability. The reduced output on the transcript must be the same pure Bell state as the exact unconditional output, which contradicts separability across the cut.

Every component away from the output must therefore contain an even number of marked physical sites. Since the total number of physical marks is odd, the output component contains an odd number. Equivalently, every component has an even number of vertices in $`T`$. A spanning tree of each component supplies a $`T`$-join by including each parent edge whose child subtree has odd $`T`$ parity. Its weight is at most the transcript's paid cost. This argument also applies to any nonzero success transcript of an exact heralded decoder.

For complete unit-cost hardware and a marked output, the optimum is $`k-1`$ CNOTs. On a line, with a marked output and the remaining marked sites in increasing order $`v_1,\ldots,v_{2k-2}`$, the optimum is the sum of the path lengths from $`v_{2j-1}`$ to $`v_{2j}`$. On a tree each edge is forced by its terminal parity, which also yields the line rule for weighted edges. These lower bounds include the five-qubit path examples above.

## The Steane code after two erasures

Index the seven physical sites of the $`[[7,1,3]]`$ Steane code by the nonzero vectors of $`\mathbb F_2^3`$. The $`X`$ and $`Z`$ stabilizer supports are the nonzero linear test supports $`\{x:u\cdot x=1\}`$, each the complement of a Fano line. A Fano line has the form $`\{a,b,a+b\}`$. The nontrivial logical support of either CSS type is the full set or any Fano line, since multiplying the uniform logical by a nonidentity check complements a check support.

For lost sites $`p,q`$, set $`t=p+q`$. The two Fano lines avoiding both lost sites each contain $`t`$. Write them as $`\{t\}\cup U`$ and $`\{t\}\cup V`$, with $`U,V`$ disjoint pairs. The only nonzero check support avoiding the losses is $`F=U\cup V`$, the complement of the line through $`p,q`$.

A surviving reference-$`X`$ generator therefore has one of the two lines as its $`X`$ support and either empty or $`F`$ as its $`Z`$ support. A reference-$`Z`$ generator has the reverse roles. Their coordinatewise symplectic products give exactly the following choices of $`A`$:

```math
\{t\},\quad \{t\}\cup U,\quad \{t\}\cup V,\quad \{t\}\cup U\cup V.
```

These four sets give the exact cost by the same $`T`$-join rule on any hardware graph. On a complete graph, $`t`$ is the unique surviving output with zero cost. Each other surviving output costs one CNOT. If the output lies in $`U`$ and only $`t`$ and the other member of $`U`$ are connected by an edge, the recovery still costs one CNOT. The pair with $`A=\{t\}\cup U`$ places both terminals of the join at the ends of that edge, and final local measurements and reports deliver the state to the isolated output. The initial encoded correlations participate in the recovery.

The [benchmark verifier](../verification/check_benchmark_witnesses.py) reproduces the tabulated unit-cost cases and the isolated-output example with the reference compiler.

## Projective-line recovery

Take the binary one-qubit CSS code of Audoux and Couvreur on the $`n=q^2+q+1`$ points of $`\mathrm{PG}(2,q)`$, with $`q`$ a power of two and $`q\ge 2`$. Each projective line $`L`$ has $`q+1`$ points and supports logical representatives $`X(L)`$ and $`Z(L)`$, the corresponding Pauli products on the line.

Suppose exactly one complete line survives. A physical stabilizer supported on $`L`$ must be the identity. For each $`x\in L`$, choose a distinct line meeting $`L`$ only at $`x`$. The stabilizer commutes with both logical Pauli representatives on that other line, so its factor at $`x`$ commutes with both $`X`$ and $`Z`$. This forces identity there. Thus the reduced Choi stabilizer group is generated by $`X_R X(L)`$ and $`Z_R Z(L)`$. Every admissible pair anticommutes at precisely the sites in $`L`$. The reduced state is the generalized Smolin state analyzed above, including its branchwise lower bound for arbitrary local instruments and paid two-site operations.

With available graph $`G`$, the [exact cost theorem](theorem.md) gives $`\tau_G(L\triangle\{o\})`$ at output $`o`$. For the wiring problem, remove erased vertices and their couplers, let the flag select a survivor output, and use unit-cost edges. The $`q`$ terminals in $`L\setminus\{o\}`$ require at least $`q/2`$ edges. At equality the edges must pair these terminals and leave $`o`$ unmatched. On each pair $`(a,b)`$, a CNOT from $`a`$ to $`b`$ maps $`X_aX_b`$ and $`Z_aZ_b`$ to $`X_a`$ and $`Z_b`$. Local measurements of those factors give two outcome parities for the final Pauli correction at $`o`$. The CNOTs act on disjoint pairs and fit in one layer.

In the Fano plane ($`q=2`$), one surviving edge is enough when the third site is the output. With no surviving edge, extraction is infeasible. If the survivors form a three-site path and the middle site is the designated output, the join uses both edges and costs two CNOTs.

Across the $`n`$ possible lines, each installed edge is internal to just one line. With a flag-selected output and an active budget of at least $`q/2`$, $`H`$ installed couplers can therefore serve at most $`\min\{n,\lfloor 2H/q\rfloor\}`$ lines. This count is attained by installing an independent near-perfect matching on each selected line.

When the physical channel chooses a uniform line and independently retains its points with probability $`t`$, the filter passes exactly the budget-feasible complete lines and replaces every other physical output by an empty erasure flag. If the graph serves $`m`$ lines, the accepted probability is $`p=t^{q+1}m/n`$. The sister repository [Correlated Erasure Capacity](https://github.com/GoGoKo699/Correlated-Erasure-Capacity/blob/fcfdc7400bc526c4ca100e7e7d1d18182a2aeed9/science/projective-line-recovery.md) gives the encoder and proves that the filtered physical channel has capacity $`\max\{0,2p-1\}`$ qubits per block, including a converse for arbitrary codes across filtered blocks. The per-block CNOT count covers extraction at the selected survivor. Outer coding operations and transport to a fixed output port have separate costs.

## Sources

- The five-qubit code is due to [Laflamme, Miquel, Paz and Zurek](https://doi.org/10.1103/PhysRevLett.77.198) and independently [Bennett, DiVincenzo, Smolin and Wootters](https://doi.org/10.1103/PhysRevA.54.3824).
- The four-qubit example uses [Smolin's unlockable state](https://doi.org/10.1103/PhysRevA.63.032306). [Wang and Ying](https://arxiv.org/abs/quant-ph/0703033) develop its multipartite stabilizer generalization and unlocking properties.
- [Steane](https://arxiv.org/abs/quant-ph/9601029) gives the seven-qubit code. The Fano-plane labels here express its usual Hamming-code checks.
- [Audoux and Couvreur](https://doi.org/10.4171/AIHPD/71), Section 4.1, supply the projective code and its logical representatives. The pairwise Bell measurement on the resulting line state is the generalized Smolin unlocking operation of [Wang and Ying](https://arxiv.org/abs/quant-ph/0703033), Example 2. The graph optimization counts the paid edges needed to realize it.
