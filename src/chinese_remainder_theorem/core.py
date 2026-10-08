"""Chinese Remainder Theorem solver using the extended Euclidean algorithm."""


class NotCoprimeError(ValueError):
    """Raised when two moduli share a common factor greater than one.

    The constructive CRT proof requires pairwise coprimality; without it the
    solution may not exist and, when it does, is not unique modulo the product.
    We refuse to guess which case applies rather than silently returning a
    number that is only one of several possible answers.
    """


class ModulusTooSmallError(ValueError):
    """Raised when a residue is out of range for its modulus.

    Concretely, when 0 <= r < m is violated. Tolerating r >= m would let two
    callers pass the same equation in two different forms and get two different
    answers, which defeats the uniqueness guarantee.
    """


def _extended_gcd(a, b):
    """Return (g, x, y) with a*x + b*y = g = gcd(a, b).

    Iterative form. The classic recursive version is elegant but blows the
    call stack on the large inputs this library is meant for.
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    # old_r is now the gcd; it is non-negative because Python's floor division
    # keeps remainders non-negative when inputs are non-negative, which we
    # enforce at the top of solve().
    return old_r, old_s, old_t


def solve(residues, moduli):
    """Return x satisfying x ≡ residues[i] (mod moduli[i]) for all i.

    Requires moduli to be pairwise coprime and each residue to satisfy
    0 <= r < m. Returns the unique solution in [0, product of moduli).

    Uses the standard constructive proof: build up the answer one congruence
    at a time, merging "current answer modulo current product" with the next
    equation via a Bézout coefficient from the extended Euclidean algorithm.
    """
    if len(residues) != len(moduli):
        raise ValueError("residues and moduli must have equal length")
    if len(residues) == 0:
        raise ValueError("at least one congruence is required")

    # Normalise to plain int. This rejects bools (which subclass int but
    # almost always indicate a caller bug) and numpy-style scalars without
    # importing anything. Fractions are rejected because CRT is a statement
    # about integers.
    clean_pairs = []
    for r, m in zip(residues, moduli):
        if isinstance(r, bool) or isinstance(m, bool):
            raise TypeError("moduli and residues must be integers, not bool")
        if not isinstance(r, int) or not isinstance(m, int):
            raise TypeError("moduli and residues must be integers")
        if m <= 0:
            raise ValueError("moduli must be positive")
        if r < 0 or r >= m:
            raise ModulusTooSmallError(
                f"residue {r} out of range for modulus {m}"
            )
        clean_pairs.append((r, m))

    x = 0
    prod = 1
    for r, m in clean_pairs:
        # x is the solution so far modulo prod; we need to lift it to also
        # satisfy x ≡ r (mod m). The number we add is a multiple of prod,
        # chosen via the inverse of prod mod m.
        g, p_inv, _ = _extended_gcd(prod % m, m)
        if g != 1:
            raise NotCoprimeError(
                f"modulus {m} is not coprime with the product of preceding "
                f"moduli (gcd={g})"
            )
        # p_inv satisfies (prod * p_inv) ≡ 1 (mod m), so prod * p_inv * (r - x)
        # is the increment that fixes the next congruence while preserving
        # all previous ones.
        x = x + prod * (p_inv * ((r - x) % m) % m)
        prod *= m

    return x % prod
