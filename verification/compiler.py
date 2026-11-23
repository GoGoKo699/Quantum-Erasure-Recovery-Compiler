"""Exact reference compiler for single-logical-qubit stabilizer recovery."""

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from heapq import heappop, heappush


class NoRecovery(ValueError):
    """The original logical qubit cannot be recovered under this input contract."""


@dataclass(frozen=True)
class Operation:
    gate: str
    sites: tuple[int, ...]
    parity: tuple[int, ...] = ()
    offset: int = 0


@dataclass(frozen=True)
class Recovery:
    cost: int | Fraction
    join_edges: tuple[tuple[int, int], ...]
    operations: tuple[Operation, ...]
    logical_x: str
    logical_z: str


@dataclass(frozen=True)
class _Pauli:
    # The operator is i**phase X**x Z**z, with X preceding Z on each site.
    x: int
    z: int
    phase: int = 0

    def __mul__(self, other):
        phase = self.phase + other.phase + 2 * (self.z & other.x).bit_count()
        return _Pauli(self.x ^ other.x, self.z ^ other.z, phase % 4)

    def letter(self, site):
        return 'IXZY'[(self.x >> site & 1) + 2 * (self.z >> site & 1)]

    def sign_bit(self):
        phase = (self.phase - (self.x & self.z).bit_count()) % 4
        assert phase in (0, 2)
        return phase // 2


def _parse_stabilizers(generators):
    words = tuple(generators)
    if not words or any(not isinstance(word, str) for word in words):
        raise ValueError('provide one signed Pauli string per Choi stabilizer generator')
    size = len(words)
    if size < 2:
        raise ValueError('the Choi state needs a reference and at least one physical site')
    stabilizers = []
    pivots = {}
    for word in words:
        letters = word[1:] if word.startswith(('+', '-')) else word
        if len(letters) != size or any(letter not in 'IXYZ' for letter in letters):
            raise ValueError('need N independent generators of length N, with reference first')
        x = sum(1 << site for site, letter in enumerate(letters) if letter in 'XY')
        z = sum(1 << site for site, letter in enumerate(letters) if letter in 'YZ')
        phase = (letters.count('Y') + 2 * word.startswith('-')) % 4
        for prior in stabilizers:
            if ((x & prior.z) ^ (z & prior.x)).bit_count() % 2:
                raise ValueError('Choi stabilizer generators must commute')
        vector = x | (z << size)
        while vector and vector.bit_length() in pivots:
            vector ^= pivots[vector.bit_length()]
        if not vector:
            raise ValueError('Choi stabilizer generators must be independent')
        pivots[vector.bit_length()] = vector
        stabilizers.append(_Pauli(x, z, phase))
    return stabilizers


def _erase_kernel(stabilizers, erased):
    width = len(stabilizers)
    mask = sum(1 << (site + 1) for site in erased)
    pivots = {}
    kernel = []
    for pauli in stabilizers:
        while True:
            projection = (pauli.x & mask) | ((pauli.z & mask) << width)
            if not projection:
                kernel.append(pauli)
                break
            leading = projection.bit_length()
            if leading not in pivots:
                pivots[leading] = pauli
                break
            pauli *= pivots[leading]
    return kernel


def _representatives(kernel):
    group = [_Pauli(0, 0)]
    for pauli in kernel:
        group += [element * pauli for element in group]
    xs = [pauli for pauli in group if pauli.letter(0) == 'X']
    zs = [pauli for pauli in group if pauli.letter(0) == 'Z']
    return xs, zs


def _hardware(edges, n, usable):
    graph = {site: [] for site in sorted(usable)}
    weights = {}
    for u, v, w in edges:
        if type(u) is not int or type(v) is not int or not (0 <= u < n and 0 <= v < n) or u == v:
            raise ValueError('hardware edges need distinct valid site indices')
        if type(w) not in (int, Fraction) or w < 0:
            raise ValueError('hardware costs must be nonnegative integers or Fractions')
        edge = tuple(sorted((u, v)))
        if edge in weights:
            raise ValueError('hardware edges must be unique and undirected')
        weights[edge] = w
        if u in usable and v in usable:
            graph[u].append((v, w))
            graph[v].append((u, w))
    return graph, weights


def _shortest_paths(graph, start):
    heap = [(0, 0, start, ())]
    paths = {}
    while heap:
        cost, hops, site, path = heappop(heap)
        if site in paths:
            continue
        paths[site] = cost, hops, path
        for neighbor, weight in graph[site]:
            if neighbor not in paths:
                edge = tuple(sorted((site, neighbor)))
                heappush(heap, (cost + weight, hops + 1, neighbor, path + (edge,)))
    return paths


def _minimum_join(boundary, shortest_paths):
    terminals = tuple(boundary)

    @lru_cache(maxsize=None)
    def match(vertices):
        if not vertices:
            return 0, 0, ()
        u, *others = vertices
        best = None
        paths = shortest_paths[u]
        for i, v in enumerate(others):
            if v not in paths:
                continue
            tail = match(tuple(others[:i] + others[i + 1:]))
            if tail is None:
                continue
            cost, hops, path = paths[v]
            candidate = cost + tail[0], hops + tail[1], path + tail[2]
            if best is None or candidate < best:
                best = candidate
        return best

    matching = match(terminals)
    if matching is None:
        return None
    odd_edges = set()
    for edge in matching[2]:
        odd_edges.symmetric_difference_update((edge,))
    return tuple(sorted(odd_edges))


# The six distinct one-qubit symplectic actions. Phases are tracked separately.
_BASES = ((), ('H',), ('S',), ('H', 'S'), ('S', 'H'), ('H', 'S', 'H'))


def _conjugate(pauli, gate, sites):
    x, z, phase = pauli.x, pauli.z, pauli.phase
    first = 1 << (sites[0] + 1)
    if gate == 'H':
        phase += 2 * bool(x & z & first)
        if (x ^ z) & first:
            x ^= first
            z ^= first
    elif gate == 'S':
        if x & first:
            z ^= first
            phase += 1
    else:
        assert gate == 'CNOT'
        second = 1 << (sites[1] + 1)
        if x & first:
            x ^= second
        if z & second:
            z ^= first
    return _Pauli(x, z, phase % 4)


def _rows(pair, site):
    return tuple(sum(((getattr(p, attr) >> (site + 1)) & 1) << i
                     for i, p in enumerate(pair)) for attr in ('x', 'z'))


def _independent(row_a, row_b):
    return row_a != 0 and row_b != 0 and row_a != row_b


def _rotations(pair, site):
    for gates in _BASES:
        rotated = pair
        for gate in gates:
            rotated = tuple(_conjugate(p, gate, (site,)) for p in rotated)
        yield gates, _rows(rotated, site)


def _synthesize(pair, join, output, usable):
    operations = []

    def apply(gate, *sites):
        nonlocal pair
        operations.append(Operation(gate, sites))
        pair = tuple(_conjugate(p, gate, sites) for p in pair)

    neighbors = {site: [] for site in usable}
    for u, v in join:
        neighbors[u].append(v)
        neighbors[v].append(u)

    visited = set()
    for root in [output, *sorted(usable - {output})]:
        if root in visited:
            continue
        visited.add(root)
        traversal = [(root, None)]
        for site, parent in traversal:
            for child in neighbors[site]:
                if child != parent:
                    assert child not in visited, 'minimum-cardinality T-join is a forest'
                    visited.add(child)
                    traversal.append((child, site))
        for child, parent in reversed(traversal[1:]):
            assert _independent(*_rows(pair, child))
            if _rows(pair, parent) == (0, 0):
                # The reset preserves both observables. Its +Z stabilizer
                # can then be added to the first representative.
                operations.append(Operation('RESET', (parent,)))
                pair = (pair[0] * _Pauli(0, 1 << (parent + 1)), pair[1])
            for gates, (row_x, _) in _rotations(pair, child):
                feasible = next((at_parent for at_parent, (_, row_z) in _rotations(pair, parent)
                                 if _independent(row_x, row_z)), None)
                if feasible is not None:
                    break
            assert feasible is not None
            for gate in gates:
                apply(gate, child)
            for gate in feasible:
                apply(gate, parent)
            apply('CNOT', child, parent)

    gates = next(gates for gates, rows in _rotations(pair, output) if rows == (1, 2))
    for gate in gates:
        apply(gate, output)

    parity_x, parity_z = [], []
    for site in sorted(usable - {output}):
        x_letter, z_letter = (p.letter(site + 1) for p in pair)
        if x_letter == z_letter == 'I':
            continue
        assert x_letter == 'I' or z_letter == 'I' or x_letter == z_letter
        letter = z_letter if x_letter == 'I' else x_letter
        operations.append(Operation('MEASURE_' + letter, (site,)))
        if x_letter != 'I':
            parity_x.append(site)
        if z_letter != 'I':
            parity_z.append(site)
    for gate, pauli, parity in (('CORRECT_Z', pair[0], parity_x),
                                 ('CORRECT_X', pair[1], parity_z)):
        offset = pauli.sign_bit()
        if parity or offset:
            operations.append(Operation(gate, (output,), tuple(parity), offset))
    return tuple(operations)


def _word(pauli, n):
    sign = '-' if pauli.sign_bit() else '+'
    return sign + ''.join(pauli.letter(site + 1) for site in range(n))


def compile_recovery(generators, erased, hardware, output, *, relay_erased=()):
    """Compile an optimal exact recovery within the native stabilizer gate model.

    See README.md for the signed Choi, hardware and conditional operation formats.
    """
    stabilizers = _parse_stabilizers(generators)
    n = len(stabilizers) - 1
    sites = set(range(n))
    erased = frozenset(erased)
    relay_erased = frozenset(relay_erased)
    if any(type(site) is not int for site in erased | relay_erased):
        raise ValueError('erased and relay indices must be integers')
    if not relay_erased <= erased <= sites:
        raise ValueError('relays must be a subset of valid erased sites')
    usable = (sites - erased) | relay_erased
    if type(output) is not int or output not in usable:
        raise ValueError('the designated output must be an available hardware site')
    graph, weights = _hardware(hardware, n, usable)
    # The unerased Choi reference must encode a qubit rather than a fixed state.
    ref_rank = {p.letter(0) for p in stabilizers} - {'I'}
    if len(ref_rank) < 2:
        raise ValueError('the Choi reference must be maximally mixed')
    xs, zs = _representatives(_erase_kernel(stabilizers, erased))
    if not xs or not zs:
        raise NoRecovery('the surviving subsystem has no joint logical X and Z representatives')
    distances = {site: _shortest_paths(graph, site) for site in graph}
    usable_in_order = sorted(usable)

    @lru_cache(maxsize=None)
    def join_for(boundary):
        join = _minimum_join(boundary, distances)
        if join is None:
            return None
        return sum(weights[edge] for edge in join), len(join), join

    best = None
    pair = None
    for lx in xs:
        for lz in zs:
            active = (lx.x & lz.z) ^ (lx.z & lz.x)
            physical_boundary = (active >> 1) ^ (1 << output)
            boundary = tuple(site for site in usable_in_order if physical_boundary >> site & 1)
            result = join_for(boundary)
            if result is not None and (best is None or result < best):
                best, pair = result, (lx, lz)
    if best is None:
        raise NoRecovery('hardware connectivity prevents exact recovery at the selected site')
    cost, _, join = best
    operations = _synthesize(pair, join, output, usable)
    return Recovery(cost, join, operations, _word(pair[0], n), _word(pair[1], n))
