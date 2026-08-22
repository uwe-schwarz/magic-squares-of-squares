// Exact coupled-identity scan over the 134 weighted p^2 q r classes.
//
// For a center root e = p^2 q r, a class fixes, for each of the four offset
// columns c (corners 0,1; edges 2,3), the Gaussian exponents of the square
// root of the offset relation: z_c carries pi^(2+j_p) pi_bar^(2-j_p) at the
// p-block (k=2) and beta^(1+j_q) beta_bar^(1-j_q), gamma^(1+j_r)
// gamma_bar^(1-j_r) at the exponent-one blocks.  The four offsets
// d_c = |Im(z_c^2)| are therefore explicit monomials in the three Gaussian
// primes, and a full magic square of squares with this class exists exactly
// when {d_2, d_3} = {d_0 + d_1, |d_0 - d_1|} (corners 0,1; edges 2,3).
//
// The scanner enumerates every ordered assignment of three rational primes
// = 1 mod 4 to the roles (p,q,r), every canonical class, and the four
// generator choices modulo global conjugation, and tests the two additive
// offset equations exactly in 128-bit unsigned arithmetic.  It also records
// the weaker 111 and 211 three-offset events on the edge/corner deletions.
//
// A positive full-configuration event is a genuine 3x3 magic square of
// distinct squares with center root p^2 q r.  A zero count is bounded
// evidence only.

#include "class_table.h"

#include <atomic>
#include <cinttypes>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <mutex>
#include <thread>
#include <vector>

using u128 = unsigned __int128;
using s128 = __int128;

namespace {

struct Gauss {
    s128 x = 0;
    s128 y = 0;
};

inline Gauss operator*(const Gauss& a, const Gauss& b) {
    return {a.x * b.x - a.y * b.y, a.x * b.y + a.y * b.x};
}

inline u128 abs_u128(s128 v) {
    return v < 0 ? static_cast<u128>(-(v + 1)) + 1 : static_cast<u128>(v);
}

// Minimal 256-bit unsigned value for exact pruning comparisons; only
// u128*u128 products and comparisons are needed.
struct U256 {
    u128 hi = 0;
    u128 lo = 0;
};

inline U256 mul_u128(u128 a, u128 b) {
    unsigned long long a0 = static_cast<unsigned long long>(a);
    unsigned long long a1 = static_cast<unsigned long long>(a >> 64);
    unsigned long long b0 = static_cast<unsigned long long>(b);
    unsigned long long b1 = static_cast<unsigned long long>(b >> 64);
    u128 p00 = static_cast<u128>(a0) * b0;
    u128 p01 = static_cast<u128>(a0) * b1;
    u128 p10 = static_cast<u128>(a1) * b0;
    u128 p11 = static_cast<u128>(a1) * b1;
    u128 mid = (p00 >> 64) + static_cast<unsigned long long>(p01) +
               static_cast<unsigned long long>(p10);
    u128 lo = (mid << 64) | static_cast<unsigned long long>(p00);
    u128 hi = p11 + (p01 >> 64) + (p10 >> 64) + (mid >> 64);
    return {hi, lo};
}

inline bool less_u256_u128(const U256& a, u128 b) {
    if (a.hi != 0) {
        return false;
    }
    return a.lo < b;
}

// d = |Im(z^2)| = |2 x y|.
inline u128 offset_of(const Gauss& z) {
    u128 xx = abs_u128(z.x);
    u128 yy = abs_u128(z.y);
    return 2 * xx * yy;
}

bool is_square_u128(u128 n, u128& root) {
    if (n == 0) {
        root = 0;
        return true;
    }
    // Newton iteration seeded by long double, then exact correction.
    unsigned long long hint = static_cast<unsigned long long>(
        std::sqrt(static_cast<long double>(n)));
    u128 r = hint > 8 ? hint - 8 : 0;
    while (r * r > n) {
        r /= 2;
        if (r == 0) {
            r = 1;
        }
    }
    while ((r + 1) * (r + 1) <= n) {
        ++r;
    }
    root = r;
    return r * r == n;
}

void print_u128(u128 v, char* buf) {
    if (v == 0) {
        buf[0] = '0';
        buf[1] = 0;
        return;
    }
    char tmp[48];
    int n = 0;
    while (v > 0) {
        tmp[n++] = static_cast<char>('0' + static_cast<int>(v % 10));
        v /= 10;
    }
    for (int i = 0; i < n; ++i) {
        buf[i] = tmp[n - 1 - i];
    }
    buf[n] = 0;
}

// ---------------------------------------------------------------------------
// Prime table: rational primes = 1 mod 4 up to a limit, each with one
// Gaussian representative (a, b), a^2 + b^2 = p.  |Im(z^2)| is invariant
// under associates and conjugation of every generator, so any fixed
// representative is valid; per-row conjugation is enumerated at scan time.
// ---------------------------------------------------------------------------

struct PrimeRep {
    unsigned p;
    short a;
    short b;
};

std::vector<PrimeRep> build_primes(unsigned limit) {
    std::vector<unsigned char> is_comp(limit + 1, 0);
    for (unsigned i = 2; static_cast<unsigned long long>(i) * i <= limit;
         ++i) {
        if (!is_comp[i]) {
            for (unsigned j = i * i; j <= limit; j += i) {
                is_comp[j] = 1;
            }
        }
    }
    std::vector<int> rep_a(limit + 1, -1);
    std::vector<int> rep_b(limit + 1, -1);
    for (unsigned a = 1; static_cast<unsigned long long>(a) * a <= limit;
         ++a) {
        for (unsigned b = 1; b <= a; ++b) {
            unsigned long long s =
                static_cast<unsigned long long>(a) * a +
                static_cast<unsigned long long>(b) * b;
            if (s > limit) {
                break;
            }
            unsigned sum = static_cast<unsigned>(s);
            if (rep_a[sum] < 0) {
                rep_a[sum] = static_cast<int>(a);
                rep_b[sum] = static_cast<int>(b);
            }
        }
    }
    std::vector<PrimeRep> primes;
    for (unsigned p = 5; p <= limit; p += 2) {
        if (!is_comp[p] && p % 4 == 1 && rep_a[p] > 0) {
            primes.push_back({p, static_cast<short>(rep_a[p]),
                              static_cast<short>(rep_b[p])});
        }
    }
    return primes;
}

inline Gauss make_gauss(const PrimeRep& pr, bool conjugate) {
    if (conjugate) {
        return {pr.a, -pr.b};
    }
    return {pr.a, pr.b};
}

// Per-prime monomial blocks: block[role][sign][j + k] is
// g^(k+j) * gbar^(k-j) with role 0 = p (k = 2), roles 1,2 = q,r (k = 1),
// sign = conjugation of the stored representative.
// p-blocks: j in -2..2 (5 entries); q/r-blocks: j in -1..1 (3 entries).
struct Blocks {
    Gauss pblock[2][5];
    Gauss qblock[2][3];
};

Blocks build_blocks(const PrimeRep& pr) {
    Blocks bl;
    for (int s = 0; s < 2; ++s) {
        Gauss g = make_gauss(pr, s == 1);
        Gauss gb = make_gauss(pr, s != 1);
        std::vector<Gauss> pow_g(5), pow_gb(5);
        pow_g[0] = {1, 0};
        pow_gb[0] = {1, 0};
        for (int i = 1; i < 5; ++i) {
            pow_g[i] = pow_g[i - 1] * g;
            pow_gb[i] = pow_gb[i - 1] * gb;
        }
        for (int j = -2; j <= 2; ++j) {
            bl.pblock[s][j + 2] = pow_g[2 + j] * pow_gb[2 - j];
        }
        for (int j = -1; j <= 1; ++j) {
            bl.qblock[s][j + 1] = pow_g[1 + j] * pow_gb[1 - j];
        }
    }
    return bl;
}

// ---------------------------------------------------------------------------
// Event detection on the four offsets (d0,d1 corners; d2,d3 edges).
// ---------------------------------------------------------------------------

bool is_full_config(u128 d0, u128 d1, u128 d2, u128 d3) {
    u128 sum = d0 + d1;
    u128 diff = d0 > d1 ? d0 - d1 : d1 - d0;
    return (d2 == sum && d3 == diff) || (d3 == sum && d2 == diff);
}

// A 111 event on a triple (x, y, z): one value is the sum of the other two.
bool is_111(u128 x, u128 y, u128 z) {
    return x + y == z || x + z == y || y + z == x;
}

// A 211 event on a triple, in any of the four coefficient arrangements.
bool is_211(u128 x, u128 y, u128 z) {
    return 2 * x + y == z || x + 2 * y == z || 2 * x + z == y ||
           x + 2 * z == y || 2 * y + z == x || y + 2 * z == x;
}

struct Counters {
    unsigned long long evaluations = 0;
    unsigned long long events_111 = 0;
    unsigned long long events_211 = 0;
    unsigned long long full_configs = 0;
    unsigned long long inequality_skips = 0;
    unsigned long long distinct_failures = 0;
    bool hit = false;
};

void add_counters(Counters& global, const Counters& local,
                  std::mutex& mutex) {
    std::lock_guard<std::mutex> lock(mutex);
    global.evaluations += local.evaluations;
    global.events_111 += local.events_111;
    global.events_211 += local.events_211;
    global.full_configs += local.full_configs;
    global.inequality_skips += local.inequality_skips;
    global.distinct_failures += local.distinct_failures;
    global.hit = global.hit || local.hit;
}

void report_hit(const char* kind, unsigned p, unsigned q, unsigned r,
                const P2QRClass& cls, unsigned gen, const u128* d) {
    char bufs[4][48];
    for (int c = 0; c < 4; ++c) {
        print_u128(d[c], bufs[c]);
    }
    std::printf("HIT %s p=%u q=%u r=%u class=%s role=%s excluded=%d gen=%u "
                "d=(%s,%s,%s,%s)\n",
                kind, p, q, r, cls.form, cls.role,
                static_cast<int>(cls.excluded), gen, bufs[0], bufs[1],
                bufs[2], bufs[3]);
    std::fflush(stdout);
}

// Proved necessary size filters from three-block-p2qr.md, section 3.
// role-specific: (1) universal, (5) corner exceptions, (8)/(9) edge
// exceptions.  Only used when --prune is given; a false negative here would
// invalidate the scan, so every test is an exact integer comparison.
struct PruneFilter {
    bool enabled = false;
};

bool prune_triple(const PruneFilter& pf, unsigned p, unsigned q, unsigned r,
                  const P2QRClass& cls) {
    if (!pf.enabled) {
        return false;
    }
    // (1): p^2 < q r, q < p^2 r, r < p^2 q  (strict, exact in u128).
    const unsigned long long p2 =
        static_cast<unsigned long long>(p) * p;
    const unsigned long long q2 =
        static_cast<unsigned long long>(q) * q;
    const unsigned long long r2 =
        static_cast<unsigned long long>(r) * r;
    const unsigned long long qr =
        static_cast<unsigned long long>(q) * r;
    if (!(p2 < qr)) {
        return true;
    }
    if (!(static_cast<unsigned long long>(q) < p2 * r)) {
        return true;
    }
    if (!(static_cast<unsigned long long>(r) < p2 * q)) {
        return true;
    }
    // M_s^2 for each role; e = p^2 q r fits u128 by the max_e guard.
    u128 ms2[3];
    {
        u128 qru = qr;
        u128 p4 = static_cast<u128>(p2) * p2;
        ms2[0] = qru * qru;                    // M_p = q r
        ms2[1] = p4 * static_cast<u128>(r2);   // M_q = p^2 r
        ms2[2] = p4 * static_cast<u128>(q2);   // M_r = p^2 q
    }
    const unsigned bases[3] = {p, q, r};
    const int k[3] = {2, 1, 1};
    for (int row = 0; row < 3; ++row) {
        char role = cls.role[row];
        if (role == 'F') {
            continue;
        }
        u128 s = bases[row];
        u128 s2 = s * s;
        if (role == 'C') {
            // (5): |nu_s| s^{2k} < 2 M^2 with s^4 | nu_s, i.e.
            // s^{4+2k} < 2 M_s^2, exact in u128.
            u128 spow = row == 0 ? s2 * s2 * s2 * s2  // s^8 (k = 2)
                                 : s2 * s2 * s2;      // s^6 (k = 1)
            if (!(spow < 2 * ms2[row])) {
                return true;
            }
        } else {
            // (9): every edge-exceptional base is 1 mod 8.
            if (bases[row] % 8 != 1) {
                return true;
            }
            // (8): s^4 delta < 2 M_s^2 with delta = prod_{t != s} t^d_t,
            // d_t = 2k_t - |j'_{t,0} - j'_{t,1}| after aligning the corner
            // signs of row s to the actual intermediate magnitude.
            int sign = cls.j[row][0] > 0 ? 1 : -1;
            u128 delta = 1;
            for (int t = 0; t < 3; ++t) {
                if (t == row) {
                    continue;
                }
                int jp0 = sign * cls.j[t][0];
                int jp1 = sign * cls.j[t][1];
                int dt = 2 * k[t] - (jp0 > jp1 ? jp0 - jp1 : jp1 - jp0);
                for (int e = 0; e < dt; ++e) {
                    delta *= bases[t];
                }
            }
            U256 lhs = mul_u128(s2 * s2, delta);
            if (!less_u256_u128(lhs, 2 * ms2[row])) {
                return true;
            }
        }
    }
    return false;
}

// ---------------------------------------------------------------------------
// Scan
// ---------------------------------------------------------------------------

struct ScanOptions {
    unsigned prime_limit = 10000;
    unsigned threads = 0;
    bool survivors_only = false;
    bool prune = false;
    unsigned long long max_e = 12000000000000000000ULL;  // 1.2e19
};

void scan_squares(unsigned p_idx, const std::vector<PrimeRep>& primes,
                  const std::vector<Blocks>& blocks,
                  const ScanOptions& opt, Counters& local) {
    const PrimeRep& pr_p = primes[p_idx];
    const unsigned p = pr_p.p;
    for (unsigned qi = 0; qi < primes.size(); ++qi) {
        if (qi == p_idx) {
            continue;
        }
        for (unsigned ri = qi + 1; ri < primes.size(); ++ri) {
            if (ri == p_idx) {
                continue;
            }
            // Two ordered assignments (q,r) and (r,q).
            for (int flip = 0; flip < 2; ++flip) {
                unsigned q = primes[flip ? ri : qi].p;
                unsigned r = primes[flip ? qi : ri].p;
                const Blocks& bq = blocks[flip ? ri : qi];
                const Blocks& br = blocks[flip ? qi : ri];
                u128 ee = static_cast<u128>(p) * p * q * r;
                if (ee > opt.max_e) {
                    ++local.inequality_skips;
                    continue;
                }
                for (std::size_t ci = 0; ci < kP2QRClassCount; ++ci) {
                    const P2QRClass& cls = kP2QRClasses[ci];
                    if (opt.survivors_only && cls.excluded) {
                        continue;
                    }
                    if (prune_triple(PruneFilter{opt.prune}, p, q, r, cls)) {
                        continue;
                    }
                    // Generator choices modulo global conjugation.
                    for (unsigned gen = 0; gen < 4; ++gen) {
                        int sp = (gen >> 0) & 1;
                        int sq = (gen >> 1) & 1;
                        int sr = (gen >> 2) & 1;
                        u128 d[4];
                        for (int c = 0; c < 4; ++c) {
                            Gauss z = blocks[p_idx].pblock[sp]
                                                [cls.j[0][c] + 2] *
                                      bq.qblock[sq][cls.j[1][c] + 1] *
                                      br.qblock[sr][cls.j[2][c] + 1];
                            d[c] = offset_of(z);
                        }
                        ++local.evaluations;
                        if (d[0] == d[1] || d[0] == d[2] || d[0] == d[3] ||
                            d[1] == d[2] || d[1] == d[3] || d[2] == d[3]) {
                            ++local.distinct_failures;
                        }
                        if (is_full_config(d[0], d[1], d[2], d[3])) {
                            ++local.full_configs;
                            local.hit = true;
                            report_hit("FULL", p, q, r, cls, gen, d);
                        }
                        if (is_111(d[0], d[1], d[2])) {
                            ++local.events_111;
                            report_hit("111", p, q, r, cls, gen, d);
                        }
                        if (is_111(d[0], d[1], d[3])) {
                            ++local.events_111;
                            report_hit("111", p, q, r, cls, gen, d);
                        }
                        if (is_211(d[1], d[2], d[3])) {
                            ++local.events_211;
                            report_hit("211", p, q, r, cls, gen, d);
                        }
                        if (is_211(d[0], d[2], d[3])) {
                            ++local.events_211;
                            report_hit("211", p, q, r, cls, gen, d);
                        }
                    }
                }
            }
        }
    }
}

int run_scan(const ScanOptions& opt) {
    std::vector<PrimeRep> primes = build_primes(opt.prime_limit);
    if (primes.size() < 3) {
        std::fprintf(stderr, "need at least three primes 1 mod 4\n");
        return 1;
    }
    std::fprintf(stderr, "primes(1 mod 4) <= %u: %zu\n", opt.prime_limit,
                 primes.size());
    std::vector<Blocks> blocks;
    blocks.reserve(primes.size());
    for (const auto& pr : primes) {
        blocks.push_back(build_blocks(pr));
    }
    Counters ctr;
    std::mutex counter_mutex;
    unsigned nthreads = opt.threads ? opt.threads
                                    : std::thread::hardware_concurrency();
    if (nthreads == 0) {
        nthreads = 1;
    }
    std::vector<std::thread> pool;
    for (unsigned t = 0; t < nthreads; ++t) {
        pool.emplace_back([&, t]() {
            Counters local;
            for (std::size_t i = t; i < primes.size(); i += nthreads) {
                scan_squares(static_cast<unsigned>(i), primes, blocks, opt,
                             local);
            }
            add_counters(ctr, local, counter_mutex);
        });
    }
    for (auto& th : pool) {
        th.join();
    }
    char bufs[6][48];
    print_u128(ctr.evaluations, bufs[0]);
    print_u128(ctr.events_111, bufs[1]);
    print_u128(ctr.events_211, bufs[2]);
    print_u128(ctr.full_configs, bufs[3]);
    print_u128(ctr.inequality_skips, bufs[4]);
    print_u128(ctr.distinct_failures, bufs[5]);
    std::printf(
        "SUMMARY prime_limit=%u threads=%u survivors_only=%d prune=%d "
        "evaluations=%s relation_111_events=%s relation_211_events=%s "
        "full_configs=%s max_e_skips=%s distinct_failures=%s\n",
        opt.prime_limit, nthreads, static_cast<int>(opt.survivors_only),
        static_cast<int>(opt.prune), bufs[0], bufs[1], bufs[2], bufs[3],
        bufs[4], bufs[5]);
    return 0;
}

// ---------------------------------------------------------------------------
// Self-test: every computed offset really lies in S_e, and the relation
// detectors see synthetic positive and negative examples.
// ---------------------------------------------------------------------------

bool self_test() {
    // Synthetic detector tests.
    {
        u128 a = 7, b = 5, sp = 12, df = 2;
        if (!is_full_config(a, b, sp, df) || !is_full_config(a, b, df, sp) ||
            !is_full_config(b, a, sp, df)) {
            std::fprintf(stderr, "full-config detector failed positive\n");
            return false;
        }
        if (is_full_config(a, b, sp, 3)) {
            std::fprintf(stderr, "full-config detector false positive\n");
            return false;
        }
        if (!is_111(2, 3, 5) || is_111(2, 3, 6)) {
            std::fprintf(stderr, "111 detector failed\n");
            return false;
        }
        if (!is_211(2, 2, 6) || is_211(2, 3, 6)) {
            std::fprintf(stderr, "211 detector failed\n");
            return false;
        }
    }
    // Offset construction: for sample classes and primes, every d_c must
    // satisfy that e^2 -/+ d_c are perfect squares (d_c in S_e).
    std::vector<PrimeRep> primes = build_primes(2000);
    std::vector<Blocks> blocks;
    for (const auto& pr : primes) {
        blocks.push_back(build_blocks(pr));
    }
    std::size_t checked = 0;
    for (std::size_t ci = 0; ci < kP2QRClassCount; ci += 7) {
        const P2QRClass& cls = kP2QRClasses[ci];
        for (std::size_t pi = 0; pi + 2 < primes.size(); pi += 23) {
            for (std::size_t qi = pi + 1; qi + 1 < primes.size(); qi += 17) {
                std::size_t ri = qi + 1;
                unsigned p = primes[pi].p, q = primes[qi].p,
                         r = primes[ri].p;
                u128 e2 = static_cast<u128>(p) * p * q * r;
                e2 = e2 * e2;  // e^2 = p^4 q^2 r^2
                for (unsigned gen = 0; gen < 4; ++gen) {
                    u128 d[4];
                    for (int c = 0; c < 4; ++c) {
                        Gauss z = blocks[pi].pblock[(gen >> 0) & 1]
                                            [cls.j[0][c] + 2] *
                                  blocks[qi].qblock[(gen >> 1) & 1]
                                                   [cls.j[1][c] + 1] *
                                  blocks[ri].qblock[(gen >> 2) & 1]
                                                   [cls.j[2][c] + 1];
                        d[c] = offset_of(z);
                    }
                    for (int c = 0; c < 4; ++c) {
                        u128 root;
                        if (!is_square_u128(e2 + d[c], root) ||
                            !is_square_u128(e2 - d[c], root)) {
                            std::fprintf(stderr,
                                         "offset not in S_e: class=%s "
                                         "p=%u q=%u r=%u gen=%u col=%d\n",
                                         cls.form, p, q, r, gen, c);
                            return false;
                        }
                        ++checked;
                    }
                    // Pairwise distinctness must hold by projective
                    // distinctness of the class columns.
                    if (d[0] == d[1] || d[0] == d[2] || d[0] == d[3] ||
                        d[1] == d[2] || d[1] == d[3] || d[2] == d[3]) {
                        std::fprintf(stderr,
                                     "duplicate offsets: class=%s p=%u "
                                     "q=%u r=%u gen=%u\n",
                                     cls.form, p, q, r, gen);
                        return false;
                    }
                }
            }
        }
    }
    std::printf("self-test ok (%zu offsets verified in S_e)\n", checked);
    return true;
}

int run_dump(unsigned p, unsigned q, unsigned r, const char* form) {
    // Print the four offsets of one class for all generator choices, for
    // external cross-validation against independent S_e enumeration.
    std::vector<PrimeRep> primes = build_primes(
        p < q ? (q < r ? r : q) : (p < r ? r : p));
    const PrimeRep* rp = nullptr;
    const PrimeRep* rq = nullptr;
    const PrimeRep* rr = nullptr;
    for (const auto& pr : primes) {
        if (pr.p == p) {
            rp = &pr;
        }
        if (pr.p == q) {
            rq = &pr;
        }
        if (pr.p == r) {
            rr = &pr;
        }
    }
    if (!rp || !rq || !rr) {
        std::fprintf(stderr, "all three arguments must be primes 1 mod 4\n");
        return 1;
    }
    const P2QRClass* cls = nullptr;
    for (std::size_t i = 0; i < kP2QRClassCount; ++i) {
        if (std::strcmp(kP2QRClasses[i].form, form) == 0) {
            cls = &kP2QRClasses[i];
        }
    }
    if (!cls) {
        std::fprintf(stderr, "unknown class form %s\n", form);
        return 1;
    }
    Blocks bp = build_blocks(*rp);
    Blocks bq = build_blocks(*rq);
    Blocks br = build_blocks(*rr);
    char bufs[4][48];
    for (unsigned gen = 0; gen < 4; ++gen) {
        u128 d[4];
        for (int c = 0; c < 4; ++c) {
            Gauss z = bp.pblock[(gen >> 0) & 1][cls->j[0][c] + 2] *
                      bq.qblock[(gen >> 1) & 1][cls->j[1][c] + 1] *
                      br.qblock[(gen >> 2) & 1][cls->j[2][c] + 1];
            d[c] = offset_of(z);
        }
        for (int c = 0; c < 4; ++c) {
            print_u128(d[c], bufs[c]);
        }
        std::printf("gen=%u d=(%s,%s,%s,%s)\n", gen, bufs[0], bufs[1],
                    bufs[2], bufs[3]);
    }
    return 0;
}

}  // namespace

int main(int argc, char** argv) {
    ScanOptions opt;
    bool do_self_test = false;
    const char* dump_form = nullptr;
    unsigned dump_p = 0, dump_q = 0, dump_r = 0;
    for (int i = 1; i < argc; ++i) {
        if (std::strcmp(argv[i], "--self-test") == 0) {
            do_self_test = true;
        } else if (std::strcmp(argv[i], "--survivors-only") == 0) {
            opt.survivors_only = true;
        } else if (std::strcmp(argv[i], "--prune") == 0) {
            opt.prune = true;
        } else if (std::strncmp(argv[i], "--dump=", 7) == 0) {
            // --dump=p,q,r,FORM
            dump_form = argv[i] + 7;
            char* comma1 = std::strchr(const_cast<char*>(dump_form), ',');
            char* comma2 = comma1 ? std::strchr(comma1 + 1, ',') : nullptr;
            char* comma3 = comma2 ? std::strchr(comma2 + 1, ',') : nullptr;
            if (!comma3) {
                std::fprintf(stderr, "--dump expects p,q,r,FORM\n");
                return 2;
            }
            dump_p = static_cast<unsigned>(
                std::strtoul(dump_form, nullptr, 10));
            dump_q = static_cast<unsigned>(
                std::strtoul(comma1 + 1, nullptr, 10));
            dump_r = static_cast<unsigned>(
                std::strtoul(comma2 + 1, nullptr, 10));
            dump_form = comma3 + 1;
        } else if (std::strncmp(argv[i], "--threads=", 10) == 0) {
            opt.threads = static_cast<unsigned>(
                std::strtoul(argv[i] + 10, nullptr, 10));
        } else if (std::strncmp(argv[i], "--primes=", 9) == 0) {
            opt.prime_limit = static_cast<unsigned>(
                std::strtoul(argv[i] + 9, nullptr, 10));
        } else {
            std::fprintf(stderr, "unknown argument %s\n", argv[i]);
            return 2;
        }
    }
    if (do_self_test) {
        return self_test() ? 0 : 1;
    }
    if (dump_form) {
        return run_dump(dump_p, dump_q, dump_r, dump_form);
    }
    return run_scan(opt);
}
