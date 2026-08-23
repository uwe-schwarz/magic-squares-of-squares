// Prime-power (l^2) torus rigidity sweep for the unresolved p^2 q r classes.
// See torus_obstruction_l2.py for the validated logic; this program runs the
// identical exhaustive torus enumeration in C++ over the FULL norm-one torus
// T of Z[i]/l^2 (the Python paths work over the squares subgroup U, so the
// C++ match counts must be exactly 8x the Python counts: rho -> rho^2 is
// 2-to-1 on T, independently in each of the three factors).
//
// For each class and each prime l it tracks, over every solution of the two
// coupled offset relations (all 16 fixed-e0 sign patterns, both edge
// orders), the minimum common l-valuation of the four offsets, capped at 2.
// Outcome 2 ("RIGID AT l^2") means every solution mod l^2 has all four
// imaginary parts divisible by l^2, which forces l^2 | d_c for all four
// offsets in any integer realization of the class with l not dividing
// 2 p q r.  Outcome 1 keeps the mod-l statement only: a valuation-1 branch
// exists.  Outcome 0 means the class is not rigid at l at all.

#include "class_table.h"

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <thread>
#include <vector>

namespace {

int MOD = 0;   // l^2
int PRIME = 0; // l

struct G {
    int a = 0;
    int b = 0;
};

inline G gmul(const G& x, const G& y) {
    return {(x.a * y.a - x.b * y.b) % MOD, (x.a * y.b + x.b * y.a) % MOD};
}

inline int valuation(int x) {
    if (x % PRIME) {
        return 0;
    }
    return (x % MOD) ? 1 : 2;
}

// Pattern accounting for one torus triple: counts matching fixed-e0
// sign/edge patterns (16 total) and updates the running minimum common
// valuation.  Mirrors pattern_match_count in torus_obstruction_l2.py.
struct Tally {
    unsigned long long matches = 0;
    int best = 3; // sentinel: no match yet
};

void tally_triple(const int v[4], Tally& t) {
    int best_here = 3;
    unsigned long long m = 0;
    for (int swap = 0; swap < 2; ++swap) {
        int se = swap ? v[3] : v[2];
        int de = swap ? v[2] : v[3];
        int s1 = (v[0] + v[1]) % MOD;
        int d1 = ((v[0] - v[1]) % MOD + MOD) % MOD;
        int ms = (se == s1) + (se == (MOD - s1) % MOD);
        int md = (de == d1) + (de == (MOD - d1) % MOD);
        int ms2 = (se == d1) + (se == (MOD - d1) % MOD);
        int md2 = (de == s1) + (de == (MOD - s1) % MOD);
        m += static_cast<unsigned long long>(ms) * md +
             static_cast<unsigned long long>(ms2) * md2;
        if (ms * md || ms2 * md2) {
            int vals[4] = {v[0], v[1], se, de};
            int common = 2;
            for (int i = 0; i < 4; ++i) {
                int w = valuation(vals[i]);
                if (w < common) {
                    common = w;
                }
            }
            if (common < best_here) {
                best_here = common;
            }
        }
    }
    t.matches += m;
    if (best_here < t.best) {
        t.best = best_here;
    }
}

Tally class_scan(const P2QRClass& cls, unsigned hardware_threads) {
    // Torus elements: norm-one elements of Z[i]/MOD, full group T.
    std::vector<G> torus;
    for (int a = 0; a < MOD; ++a) {
        for (int b = 0; b < MOD; ++b) {
            if ((a | b) == 0) {
                continue;
            }
            if ((a * a + b * b) % MOD == 1) {
                torus.push_back({a, b});
            }
        }
    }
    const std::size_t n = torus.size();
    // Precompute per-element inverse and even powers up to 4.
    std::vector<G> inv(n), sq(n), isq(n), fo(n), ifo(n);
    for (std::size_t i = 0; i < n; ++i) {
        G z = torus[i];
        int nz = (z.a * z.a + z.b * z.b) % MOD;
        int nzi = 1;
        for (int e = 0; e < 40; ++e) {
            // Newton iteration for the inverse of nz mod MOD (odd).
            long long t = (2 - static_cast<long long>(nz) * nzi % MOD) % MOD;
            nzi = static_cast<int>(static_cast<long long>(nzi) * t % MOD);
        }
        G ci = {static_cast<int>(static_cast<long long>(z.a) * nzi % MOD),
                static_cast<int>((MOD -
                  static_cast<long long>(z.b) * nzi % MOD) % MOD)};
        inv[i] = ci;
        sq[i] = gmul(z, z);
        isq[i] = gmul(ci, ci);
        fo[i] = gmul(sq[i], sq[i]);
        ifo[i] = gmul(isq[i], isq[i]);
    }
    // rho^{2 j_p}: j_p in {-2,-1,0,1,2} gives t^{-4}, t^{-2}, 1, t^2, t^4.
    const unsigned nt = hardware_threads;
    std::vector<Tally> partial(nt);
    std::vector<std::thread> threads;
    for (unsigned slot = 0; slot < nt; ++slot) {
        threads.emplace_back([&, slot]() {
            Tally& t = partial[slot];
            for (std::size_t i = slot; i < n; i += nt) {
                G rp[5] = {ifo[i], isq[i], {1, 0}, sq[i], fo[i]};
                G pcol[4];
                for (int c = 0; c < 4; ++c) {
                    pcol[c] = rp[cls.j[0][c] + 2];
                }
                for (std::size_t j = 0; j < n; ++j) {
                    G rq[3] = {{1, 0}, sq[j], isq[j]};
                    G prefix[4];
                    for (int c = 0; c < 4; ++c) {
                        prefix[c] = gmul(
                            pcol[c],
                            rq[cls.j[1][c] == 0
                                   ? 0
                                   : (cls.j[1][c] > 0 ? 1 : 2)]);
                    }
                    for (std::size_t k = 0; k < n; ++k) {
                        G rr[3] = {{1, 0}, sq[k], isq[k]};
                        int v[4];
                        for (int c = 0; c < 4; ++c) {
                            int jr = cls.j[2][c];
                            G x = gmul(prefix[c],
                                       rr[jr == 0 ? 0 : (jr > 0 ? 1 : 2)]);
                            int im = x.b % MOD;
                            if (im < 0) {
                                im += MOD;
                            }
                            v[c] = im;
                        }
                        tally_triple(v, t);
                    }
                }
            }
        });
    }
    for (auto& th : threads) {
        th.join();
    }
    Tally total;
    for (const Tally& t : partial) {
        total.matches += t.matches;
        if (t.best < total.best) {
            total.best = t.best;
        }
    }
    return total;
}

}  // namespace

int main(int argc, char** argv) {
    if (argc < 2) {
        std::fprintf(stderr, "usage: torus_rigidity_l2 L1 [L2 ...]\n");
        return 2;
    }
    std::vector<int> primes;
    for (int i = 1; i < argc; ++i) {
        primes.push_back(std::atoi(argv[i]));
    }
    const unsigned hw = std::thread::hardware_concurrency();
    const unsigned nt = hw ? std::min(hw, 8u) : 1u;
    for (int l : primes) {
        if (l < 3 || l % 2 == 0) {
            std::fprintf(stderr, "prime %d: must be odd and >= 3\n", l);
            return 2;
        }
        MOD = l * l;
        PRIME = l;
        std::printf("prime %d (modulus %d) [threads %u]\n", l, MOD, nt);
        std::fflush(stdout);
        for (std::size_t ci = 0; ci < kP2QRClassCount; ++ci) {
            const P2QRClass& cls = kP2QRClasses[ci];
            if (cls.excluded) {
                continue;
            }
            Tally t = class_scan(cls, nt);
            const char* verdict = t.best == 2
                                      ? "RIGID AT l^2 (l^2 | d forced)"
                                      : (t.best == 1
                                             ? "l | d forced, valuation-1 "
                                               "branch exists"
                                             : "solvable mod l");
            std::printf("  %s (%s): %s [matches=%llu, min_common_v=%d]\n",
                        cls.form, cls.role, verdict, t.matches, t.best);
            std::fflush(stdout);
        }
    }
    return 0;
}
