// Modular obstruction check for the unresolved p^2 q r classes.
//
// For a fixed class, the four offsets d_c = |Im(z_c^2)| are explicit
// monomials in the three Gaussian primes.  Any integer realization with
// center root p^2 q r reduces modulo every auxiliary prime l (l not
// dividing 2pqr) to a solution of the same system over the ring
// Z[i]/(l): the generators pi, beta, gamma become units (their norms are
// the nonzero residues of p, q, r), and the two additive offset equations
// hold for some choice of the eight unit signs.  If for a single l no
// unit triple with pairwise distinct norms and no sign pattern solves the
// system, the class is empty over the integers.
//
// The check is a relaxation: primality of the norms and all size
// constraints are dropped.  Finding solutions is therefore expected and
// carries no information; a decisive negative at any l would be a proof.

#include "class_table.h"

#include <cstdio>
#include <cstring>
#include <vector>

namespace {

int MOD = 0;

struct G {
    int a = 0;
    int b = 0;
};

inline G gmul(const G& x, const G& y) {
    return {(x.a * y.a - x.b * y.b) % MOD, (x.a * y.b + x.b * y.a) % MOD};
}

inline G gconj(const G& x) { return {x.a, -x.b}; }

inline int gnorm(const G& x) {
    return (x.a * x.a + x.b * x.b) % MOD;
}

// Evaluate z_c = pi^(2+jp) pibar^(2-jp) * beta^(1+jq) betabar^(1-jq)
// * gamma^(1+jr) gammabar^(1-jr) for the given generator orientations.
G column_root(const G& pi, const G& beta, const G& gamma, int jp, int jq,
              int jr) {
    G ppow[5], pbpow[5], bpow[3], bbpow[3], gpow[3], gbpow[3];
    ppow[0] = pbpow[0] = bpow[0] = bbpow[0] = gpow[0] = gbpow[0] = {1, 0};
    for (int i = 1; i < 5; ++i) {
        ppow[i] = gmul(ppow[i - 1], pi);
        pbpow[i] = gmul(pbpow[i - 1], gconj(pi));
    }
    for (int i = 1; i < 3; ++i) {
        bpow[i] = gmul(bpow[i - 1], beta);
        bbpow[i] = gmul(bbpow[i - 1], gconj(beta));
        gpow[i] = gmul(gpow[i - 1], gamma);
        gbpow[i] = gmul(gbpow[i - 1], gconj(gamma));
    }
    return gmul(gmul(ppow[2 + jp], pbpow[2 - jp]),
                gmul(gmul(bpow[1 + jq], bbpow[1 - jq]),
                     gmul(gpow[1 + jr], gbpow[1 - jr])));
}

inline int imag_sq(const G& z) {
    // Im(z^2) = 2 a b.
    return (2 * z.a % MOD) * z.b % MOD;
}

bool pattern_ok(const int v[4], int e0, int e1, int e2, int e3, int swap) {
    // Corners 0,1 carry signs e0,e1; the sum edge and difference edge are
    // (2,3) in one of the two orders.
    int sum_edge = swap ? v[3] : v[2];
    int dif_edge = swap ? v[2] : v[3];
    int lhs_sum = (e0 * v[0] + e1 * v[1]) % MOD;
    int lhs_dif = (e0 * v[0] - e1 * v[1]) % MOD;
    return ((e2 * sum_edge - lhs_sum) % MOD == 0) &&
           ((e3 * dif_edge - lhs_dif) % MOD == 0);
}

// Does any sign pattern and unit generator triple with distinct norms
// solve the coupled system for this class mod MOD?  An integer
// realization reduces to one such solution, so a full negative at a
// single modulus excludes the class over the integers.
bool class_solvable(const P2QRClass& cls, unsigned long long* tries,
                    unsigned long long* degenerate_tries) {
    std::vector<G> units;
    std::vector<int> unit_norms;
    for (int a = 0; a < MOD; ++a) {
        for (int b = 0; b < MOD; ++b) {
            if ((a | b) == 0) {
                continue;
            }
            int norm = (a * a + b * b) % MOD;
            if (norm != 0) {
                units.push_back({a, b});
                unit_norms.push_back(norm);
            }
        }
    }
    const std::size_t n = units.size();
    for (std::size_t i = 0; i < n; ++i) {
        G ppow[5], pbpow[5];
        ppow[0] = pbpow[0] = {1, 0};
        for (int t = 1; t < 5; ++t) {
            ppow[t] = gmul(ppow[t - 1], units[i]);
            pbpow[t] = gmul(pbpow[t - 1], gconj(units[i]));
        }
        G pcol[5];
        for (int jp = -2; jp <= 2; ++jp) {
            pcol[jp + 2] = gmul(ppow[2 + jp], pbpow[2 - jp]);
        }
        for (std::size_t j = 0; j < n; ++j) {
            G bpow[3], bbpow[3];
            bpow[0] = bbpow[0] = {1, 0};
            for (int t = 1; t < 3; ++t) {
                bpow[t] = gmul(bpow[t - 1], units[j]);
                bbpow[t] = gmul(bbpow[t - 1], gconj(units[j]));
            }
            G bcol[3];
            for (int jq = -1; jq <= 1; ++jq) {
                bcol[jq + 1] = gmul(bpow[1 + jq], bbpow[1 - jq]);
            }
            for (std::size_t k = 0; k < n; ++k) {
                G gpow[3], gbpow[3];
                gpow[0] = gbpow[0] = {1, 0};
                for (int t = 1; t < 3; ++t) {
                    gpow[t] = gmul(gpow[t - 1], units[k]);
                    gbpow[t] = gmul(gbpow[t - 1], gconj(units[k]));
                }
                G gcol[3];
                for (int jr = -1; jr <= 1; ++jr) {
                    gcol[jr + 1] = gmul(gpow[1 + jr], gbpow[1 - jr]);
                }
                ++*tries;
                int v[4];
                bool degenerate = true;
                for (int c = 0; c < 4; ++c) {
                    G z = gmul(gmul(pcol[cls.j[0][c] + 2],
                                    bcol[cls.j[1][c] + 1]),
                               gcol[cls.j[2][c] + 1]);
                    v[c] = imag_sq(z);
                    if (v[c] < 0) {
                        v[c] += MOD;
                    }
                    if (v[c] != 0) {
                        degenerate = false;
                    }
                }
                // The all-zero offset locus (every z_c real mod MOD) solves
                // every sign pattern trivially; it is the reduction of an
                // integer realization only when MOD divides all four
                // offsets, so it is tracked separately.
                if (degenerate) {
                    ++*degenerate_tries;
                    continue;
                }
                for (int swap = 0; swap < 2; ++swap) {
                    for (int bits = 0; bits < 16; ++bits) {
                        if (pattern_ok(v, (bits & 8) ? 1 : -1,
                                       (bits & 4) ? 1 : -1,
                                       (bits & 2) ? 1 : -1,
                                       (bits & 1) ? 1 : -1, swap)) {
                            return true;
                        }
                    }
                }
            }
        }
    }
    return false;
}

}  // namespace

int main(int argc, char** argv) {
    if (argc < 2) {
        std::fprintf(stderr,
                     "usage: modular_obstruction L1 [L2 ...]  (odd primes)\n");
        return 2;
    }
    for (int i = 1; i < argc; ++i) {
        MOD = std::atoi(argv[i]);
        if (MOD < 3 || MOD % 2 == 0) {
            std::fprintf(stderr, "ignoring invalid modulus %d\n", MOD);
            continue;
        }
        std::printf("modulus %d: unit count check\n", MOD);
        int empty = 0;
        int checked = 0;
        for (std::size_t ci = 0; ci < kP2QRClassCount; ++ci) {
            const P2QRClass& cls = kP2QRClasses[ci];
            if (cls.excluded) {
                continue;
            }
            ++checked;
            unsigned long long tries = 0;
            unsigned long long degen = 0;
            bool ok = class_solvable(cls, &tries, &degen);
            std::printf("  class %s (%s): %s (%llu unit triples)\n",
                        cls.form, cls.role,
                        ok ? "non-degenerately solvable" : "ONLY DEGENERATE",
                        tries);
            if (!ok) {
                ++empty;
            }
            (void)degen;
        }
        std::printf("modulus %d summary: %d/%d classes without obstruction\n",
                    MOD, checked - empty, checked);
        if (empty > 0) {
            std::printf("*** %d classes obstructed at %d ***\n", empty, MOD);
        }
        std::fflush(stdout);
    }
    return 0;
}
