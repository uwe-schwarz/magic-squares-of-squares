// Fast torus-parametrized modular rigidity sweep for the unresolved
// p^2 q r classes.  See torus_obstruction.py for the validated logic; this
// program runs the identical exhaustive torus enumeration in C++ so that
// large auxiliary primes stay feasible.
//
// For each class and each modulus l, it decides whether any non-degenerate
// (rho, sigma, tau) on the norm-one torus of Z[i]/l, together with any of
// the 32 sign/edge patterns, satisfies the two coupled offset relations.
// "ONLY DEGENERATE" means every solution collapses to all four offsets
// vanishing mod l, which forces l | d_c for all four offsets in any
// integer realization of the class with l not dividing 2 p q r.

#include "class_table.h"

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <thread>
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

bool class_solvable(const P2QRClass& cls, unsigned long long* steps) {
    // Torus elements: norm-one elements of Z[i]/MOD.
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
    // Precompute per-torus-element inverse and even powers up to 4.
    const std::size_t n = torus.size();
    std::vector<G> inv(n);
    std::vector<G> sq(n);    // t^2
    std::vector<G> isq(n);   // t^{-2}
    std::vector<G> fo(n);    // t^4
    std::vector<G> ifo(n);   // t^{-4}
    for (std::size_t i = 0; i < n; ++i) {
        G z = torus[i];
        int nz = (z.a * z.a + z.b * z.b) % MOD;
        int nzi = 1;
        for (int e = 0; e < 30; ++e) {
            // Newton: nzi = nzi*(2 - nz*nzi) mod MOD
            int t = (2 - nz * nzi % MOD) % MOD;
            nzi = (int)((long long)nzi * t % MOD);
        }
        inv[i] = {(int)((long long)gconj(z).a * nzi % MOD),
                  (int)((long long)gconj(z).b * nzi % MOD)};
        sq[i] = gmul(z, z);
        isq[i] = gmul(inv[i], inv[i]);
        fo[i] = gmul(sq[i], sq[i]);
        ifo[i] = gmul(isq[i], isq[i]);
    }
    // rho^{2 j_p}: j_p in {-2,-1,0,1,2} gives t^{-4}, t^{-2}, 1, t^2, t^4.
    for (std::size_t i = 0; i < n; ++i) {
        G rp[5] = {ifo[i], isq[i], {1, 0}, sq[i], fo[i]};
        G pcol[4];
        for (int c = 0; c < 4; ++c) {
            pcol[c] = rp[cls.j[0][c] + 2];
        }
        for (std::size_t j = 0; j < n; ++j) {
            G rq[3] = {{1, 0}, sq[j], isq[j]};
            G prefix[4];
            for (int c = 0; c < 4; ++c) {
                prefix[c] = gmul(pcol[c], rq[cls.j[1][c] == 0
                                                   ? 0
                                                   : (cls.j[1][c] > 0 ? 1
                                                                      : 2)]);
            }
            for (std::size_t k = 0; k < n; ++k) {
                G rr[3] = {{1, 0}, sq[k], isq[k]};
                int v[4];
                bool degenerate = true;
                for (int c = 0; c < 4; ++c) {
                    int jr = cls.j[2][c];
                    G x = gmul(prefix[c], rr[jr == 0 ? 0 : (jr > 0 ? 1 : 2)]);
                    int im = x.b % MOD;
                    if (im < 0) {
                        im += MOD;
                    }
                    v[c] = im;
                    if (im != 0) {
                        degenerate = false;
                    }
                }
                ++*steps;
                if (degenerate) {
                    continue;
                }
                for (int swap = 0; swap < 2; ++swap) {
                    int se = swap ? v[3] : v[2];
                    int de = swap ? v[2] : v[3];
                    for (int bits = 0; bits < 16; ++bits) {
                        int e0 = (bits & 8) ? 1 : -1;
                        int e1 = (bits & 4) ? 1 : -1;
                        int e2 = (bits & 2) ? 1 : -1;
                        int e3 = (bits & 1) ? 1 : -1;
                        if ((e2 * se - (e0 * v[0] + e1 * v[1])) % MOD == 0 &&
                            (e3 * de - (e0 * v[0] - e1 * v[1])) % MOD == 0) {
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
        std::fprintf(stderr, "usage: torus_rigidity L1 [L2 ...]\n");
        return 2;
    }
    std::vector<int> moduli;
    for (int i = 1; i < argc; ++i) {
        moduli.push_back(std::atoi(argv[i]));
    }
    for (int mod : moduli) {
        MOD = mod;
        int rigid = 0;
        int checked = 0;
        std::printf("modulus %d\n", mod);
        std::fflush(stdout);
        for (std::size_t ci = 0; ci < kP2QRClassCount; ++ci) {
            const P2QRClass& cls = kP2QRClasses[ci];
            if (cls.excluded) {
                continue;
            }
            ++checked;
            unsigned long long steps = 0;
            bool ok = class_solvable(cls, &steps);
            if (!ok) {
                ++rigid;
            }
            std::printf("  %s (%s): %s [%llu steps]\n", cls.form, cls.role,
                        ok ? "solvable" : "ONLY DEGENERATE", steps);
            std::fflush(stdout);
        }
        std::printf("modulus %d summary: %d/%d locally solvable, %d rigid\n",
                    mod, checked - rigid, checked, rigid);
        std::fflush(stdout);
    }
    return 0;
}
