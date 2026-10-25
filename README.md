# chinese_remainder_theorem

Solve a system of simultaneous congruences with pairwise-coprime moduli. Given residues `[r1, r2, ...]` and moduli `[m1, m2, ...]` with `gcd(mi, mj) == 1` for `i != j`, `solve` returns the unique `x` in `[0, m1*m2*...)` satisfying `x ≡ ri (mod mi)` for every `i`.

```python
from chinese_remainder_theorem import solve

x = solve([2, 3, 2], [3, 5, 7])
assert x == 23
```

## Why

Reconstructing a large integer from its residues modulo several small primes is a standard building block in big-integer arithmetic and in threshold-style computations where each party holds a residue and no single party holds the full value. The implementation uses the extended Euclidean algorithm directly rather than Garner's scheme, trading a little speed for code that is short, dependency-free, and easy to audit.

## Edge cases

Residues must satisfy `0 <= r < m`. Passing `r = m` or a negative residue raises `ModulusTooSmallError` rather than silently normalising — two callers passing the same equation in different forms should get the same answer, and quiet canonicalisation would break that contract. Moduli must be pairwise coprime; a shared factor raises `NotCoprimeError`. A modulus of `1` is allowed and acts as the identity congruence, which is the standard way to make a constraint drop out.

## Exports

- `solve(residues, moduli)` — returns the unique solution in `[0, product of moduli)`.
- `NotCoprimeError` — raised when two moduli share a factor.
- `ModulusTooSmallError` — raised when a residue is not in `[0, modulus)`.

## Performance

The window keeps a bounded buffer, so `push` is constant time and memory does not
grow with the length of the stream. `peak` and `trough` are linear in the window
size, which is the trade that keeps `push` cheap.

## Limitations

Values are coerced to floats, so very large integers lose precision. If you need
exact integer aggregates over a window, this is the wrong tool.

