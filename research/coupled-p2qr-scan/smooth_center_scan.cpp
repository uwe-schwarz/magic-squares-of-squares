// Smooth-center scan: exhaustive relation search over all center roots
// whose prime factors all lie in the split primes (1 mod 4).
//
// For a center root e, S_e = {|Im(z^2)| : N(z) = e^2} depends only on the
// factorization of e in Z[i].  If e = e_split * m with m a product of
// inert primes (3 mod 4), every offset scales by m^2, so the presence of
// 111/211 relations and full four-offset configurations depends only on
// e_split.  This scan therefore enumerates every split-smooth e up to a
// bound B, builds S_e from the Gaussian divisors of e^2, and tests:
//   - 111 relations:  x + y = z among distinct offsets;
//   - 211 relations:  2x + y = z, x + 2y = z, x + z = 2y;
//   - full configurations: {a, b, a+b, |a-b|} subset S_e.
// A full configuration is a genuine 3x3 magic square of distinct squares.
//
// All arithmetic is exact in unsigned __int128; offsets fit since
// d <= e^2 <= B^2.

#include <algorithm>
#include <atomic>
#include <atomic>
#include <cinttypes>
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

struct SplitPrime {
    unsigned p;
    short a;
    short b;  // a^2 + b^2 = p
};

std::vector<SplitPrime> build_split_primes(unsigned limit) {
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
    std::vector<SplitPrime> primes;
    for (unsigned p = 5; p <= limit; p += 2) {
        if (!is_comp[p] && p % 4 == 1 && rep_a[p] > 0) {
            primes.push_back({p, static_cast<short>(rep_a[p]),
                              static_cast<short>(rep_b[p])});
        }
    }
    return primes;
}

struct Counters {
    unsigned long long centers = 0;
    unsigned long long offsets = 0;
    unsigned long long relation_111 = 0;
    unsigned long long relation_211 = 0;
    unsigned long long full_configs = 0;
    unsigned long long centers_scanned = 0;
    bool hit = false;
};

// Test one center: build S_e and look for relations.
void test_center(u128 e, const std::vector<Gauss>& generators,
                 const std::vector<int>& exponents, Counters& local) {
    // Enumerate all z with N(z) = e^2 by exponents a_i in [0, 2 k_i].
    std::vector<u128> offsets;
    int blocks = static_cast<int>(generators.size());
    // Precompute powers pi^a and pibar^(2k-a) for each block.
    std::vector<std::vector<Gauss>> pow_g(blocks), pow_gb(blocks);
    for (int i = 0; i < blocks; ++i) {
        int max_a = 2 * exponents[i];
        pow_g[i].resize(max_a + 1);
        pow_gb[i].resize(max_a + 1);
        pow_g[i][0] = {1, 0};
        pow_gb[i][0] = {1, 0};
        Gauss gb = {generators[i].x, -generators[i].y};
        for (int a = 1; a <= max_a; ++a) {
            pow_g[i][a] = pow_g[i][a - 1] * generators[i];
            pow_gb[i][a] = pow_gb[i][a - 1] * gb;
        }
    }
    std::vector<int> idx(blocks, 0);
    while (true) {
        Gauss z = {1, 0};
        for (int i = 0; i < blocks; ++i) {
            z = z * pow_g[i][idx[i]] * pow_gb[i][2 * exponents[i] - idx[i]];
        }
        u128 d = 2 * (z.x < 0 ? -static_cast<u128>(z.x) : static_cast<u128>(z.x)) *
                 (z.y < 0 ? -static_cast<u128>(z.y) : static_cast<u128>(z.y));
        if (d != 0) {
            offsets.push_back(d);
        }
        // odometer
        int i = 0;
        while (i < blocks && idx[i] == 2 * exponents[i]) {
            idx[i] = 0;
            ++i;
        }
        if (i == blocks) {
            break;
        }
        ++idx[i];
    }
    std::sort(offsets.begin(), offsets.end());
    offsets.erase(std::unique(offsets.begin(), offsets.end()), offsets.end());
    local.centers_scanned++;
    local.offsets += offsets.size();
    if (offsets.size() < 3) {
        return;
    }
    // 111: x + y = z with distinct x < y < z.  211 variants.  Full config.
    for (std::size_t i = 0; i < offsets.size(); ++i) {
        for (std::size_t j = i + 1; j < offsets.size(); ++j) {
            u128 x = offsets[i], y = offsets[j];
            u128 sum = x + y;
            if (std::binary_search(offsets.begin(), offsets.end(), sum)) {
                ++local.relation_111;
                char b1[48], b2[48], b3[48], b4[48];
                print_u128(e, b1);
                print_u128(x, b2);
                print_u128(y, b3);
                print_u128(sum, b4);
                std::printf(
                    "HIT 111 e=%s offsets=%s+%s=%s\n", b1, b2, b3, b4);
                std::fflush(stdout);
            }
            u128 two_x_y = 2 * x + y;
            if (std::binary_search(offsets.begin(), offsets.end(),
                                   two_x_y)) {
                ++local.relation_211;
                std::printf("HIT 211 (2x+y)\n");
                std::fflush(stdout);
            }
            u128 x_two_y = x + 2 * y;
            if (std::binary_search(offsets.begin(), offsets.end(),
                                   x_two_y)) {
                ++local.relation_211;
                std::printf("HIT 211 (x+2y)\n");
                std::fflush(stdout);
            }
            u128 z3 = 2 * y - x;  // third 211 form: x + z = 2y, z > y
            if (std::binary_search(offsets.begin(), offsets.end(), z3)) {
                ++local.relation_211;
                std::printf("HIT 211 (x+z=2y)\n");
                std::fflush(stdout);
            }
            u128 diff = y - x;
            if (y != 2 * x && diff != 0 &&
                std::binary_search(offsets.begin(), offsets.end(), diff)) {
                // x + y and y - x both admissible: {x, y, x+y, y-x}.
                ++local.full_configs;
                local.hit = true;
                char b1[48], b2[48], b3[48], b4[48], b5[48];
                print_u128(e, b1);
                print_u128(x, b2);
                print_u128(y, b3);
                print_u128(sum, b4);
                print_u128(diff, b5);
                std::printf(
                    "HIT FULL e=%s offsets={%s,%s,%s,%s} MAGIC SQUARE\n",
                    b1, b2, b3, b4, b5);
                std::fflush(stdout);
            }
        }
    }
}

void dfs(u128 e, std::size_t prime_index, u128 limit,
         const std::vector<SplitPrime>& primes, std::vector<Gauss>& gens,
         std::vector<int>& exponents, Counters& local) {
    if (e > 1) {
        test_center(e, gens, exponents, local);
    }
    for (std::size_t i = prime_index; i < primes.size(); ++i) {
        unsigned p = primes[i].p;
        if (e > limit / p) {
            break;  // primes sorted; later primes only larger
        }
        // exponent k with e * p^k <= limit
        u128 next = e;
        int k = 0;
        std::size_t added = gens.size();
        gens.push_back({primes[i].a, primes[i].b});
        exponents.push_back(0);
        while (next <= limit / p) {
            next *= p;
            ++k;
            exponents[added] = k;
            dfs(next, i + 1, limit, primes, gens, exponents, local);
        }
        gens.pop_back();
        exponents.pop_back();
    }
}

}  // namespace

int main(int argc, char** argv) {
    unsigned long long bound = 1000000000ULL;
    unsigned threads = 0;
    for (int i = 1; i < argc; ++i) {
        if (std::strncmp(argv[i], "--bound=", 8) == 0) {
            bound = std::strtoull(argv[i] + 8, nullptr, 10);
        } else if (std::strncmp(argv[i], "--threads=", 10) == 0) {
            threads = static_cast<unsigned>(
                std::strtoul(argv[i] + 10, nullptr, 10));
        } else {
            std::fprintf(stderr, "unknown argument %s\n", argv[i]);
            return 2;
        }
    }
    if (bound > 4000000000000ULL) {
        std::fprintf(stderr, "bound above audited 4e12 limit\n");
        return 1;
    }
    // Enumerate every split-smooth e <= bound whose prime factors are all
    // at most sqrt(bound).  Two-block centers with one large prime are
    // already excluded by the proved two-block theorem; the p^2 q r
    // family with one large prime is covered by coupled_p2qr_scan.
    unsigned prime_limit = static_cast<unsigned>(std::sqrt((double)bound)) + 1;
    std::vector<SplitPrime> primes = build_split_primes(prime_limit);
    std::fprintf(stderr, "split primes <= %u: %zu\n", prime_limit,
                 primes.size());

    // Parallelize over the smallest prime factor of e.
    struct Shard {
        std::size_t begin;
        std::size_t end;
    };
    unsigned nthreads = threads ? threads
                                : std::thread::hardware_concurrency();
    if (nthreads == 0) {
        nthreads = 1;
    }
    Counters total;
    std::mutex mutex;
    std::vector<std::thread> pool;
    // Work tasks fix the two smallest prime-power blocks; finer than
    // whole first-prime shards, which would serialize on p = 5.
    struct Task {
        u128 e;
        std::size_t next;  // next prime index for the DFS
        std::vector<Gauss> gens;
        std::vector<int> exponents;
    };
    std::vector<Task> tasks;
    for (std::size_t i = 0; i < primes.size(); ++i) {
        u128 e1 = 1;
        int k = 0;
        while (e1 <= bound / primes[i].p) {
            e1 *= primes[i].p;
            ++k;
            tasks.push_back({e1, i + 1, {{primes[i].a, primes[i].b}}, {k}});
            for (std::size_t j = i + 1; j < primes.size(); ++j) {
                u128 e2 = e1;
                int m = 0;
                while (e2 <= bound / primes[j].p) {
                    e2 *= primes[j].p;
                    ++m;
                    tasks.push_back(
                        {e2, j + 1,
                         {{primes[i].a, primes[i].b},
                          {primes[j].a, primes[j].b}},
                         {k, m}});
                }
            }
        }
    }
    std::fprintf(stderr, "tasks: %zu\n", tasks.size());
    std::atomic<std::size_t> next_task(0);
    for (unsigned t = 0; t < nthreads; ++t) {
        pool.emplace_back([&]() {
            Counters local;
            while (true) {
                std::size_t ti = next_task.fetch_add(1);
                if (ti >= tasks.size()) {
                    break;
                }
                const Task& task = tasks[ti];
                std::vector<Gauss> gens = task.gens;
                std::vector<int> exponents = task.exponents;
                if (task.gens.size() == 1) {
                    // single-block task: pair tasks own everything deeper
                    test_center(task.e, gens, exponents, local);
                } else {
                    dfs(task.e, task.next, bound, primes, gens, exponents,
                        local);
                }
            }
            std::lock_guard<std::mutex> lock(mutex);
            total.centers += local.centers;
            total.centers_scanned += local.centers_scanned;
            total.offsets += local.offsets;
            total.relation_111 += local.relation_111;
            total.relation_211 += local.relation_211;
            total.full_configs += local.full_configs;
            total.hit = total.hit || local.hit;
        });
    }
    for (auto& th : pool) {
        th.join();
    }
    char b1[48], b2[48], b3[48], b4[48], b5[48];
    print_u128(total.centers_scanned, b1);
    print_u128(total.offsets, b2);
    print_u128(total.relation_111, b3);
    print_u128(total.relation_211, b4);
    print_u128(total.full_configs, b5);
    std::printf(
        "SUMMARY bound=%llu threads=%u centers_scanned=%s offsets=%s "
        "relation_111_events=%s relation_211_events=%s full_configs=%s\n",
        bound, nthreads, b1, b2, b3, b4, b5);
    return 0;
}
