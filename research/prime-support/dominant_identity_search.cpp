#include <algorithm>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

using i128 = __int128_t;
using u128 = __uint128_t;

struct GInt {
  int64_t x, y;
  bool operator<(const GInt& o) const { return x < o.x || (x == o.x && y < o.y); }
  bool operator==(const GInt& o) const { return x == o.x && y == o.y; }
};

static GInt mul(GInt a, GInt b) {
  return {a.x * b.x - a.y * b.y, a.x * b.y + a.y * b.x};
}
static GInt gpw(GInt a, uint32_t n) {
  GInt r{1, 0};
  while (n) {
    if (n & 1) r = mul(r, a);
    n >>= 1;
    // Do not square after consuming the highest bit.  Besides being wasted
    // work, that extra square can exceed int64_t even though the requested
    // power and every value used by the bounded scan fit exactly.
    if (n) a = mul(a, a);
  }
  return r;
}
static GInt conj(GInt a) { return {a.x, -a.y}; }
static GInt neg(GInt a) { return {-a.x, -a.y}; }

static std::vector<uint32_t> spf_sieve(uint32_t n) {
  std::vector<uint32_t> spf(n + 1);
  std::iota(spf.begin(), spf.end(), 0);
  if (n) spf[1] = 1;
  for (uint32_t p = 2; uint64_t(p) * p <= n; ++p)
    if (spf[p] == p)
      for (uint64_t x = uint64_t(p) * p; x <= n; x += p)
        if (spf[x] == x) spf[x] = p;
  return spf;
}

static std::vector<std::pair<uint32_t, uint32_t>> factor(uint32_t n,
                                                         const std::vector<uint32_t>& spf) {
  std::vector<std::pair<uint32_t, uint32_t>> out;
  while (n > 1) {
    uint32_t p = spf[n], k = 0;
    do { n /= p; ++k; } while (n > 1 && spf[n] == p);
    out.emplace_back(p, k);
  }
  return out;
}

static GInt split_rep(uint32_t p, std::map<uint32_t, GInt>& cache) {
  auto it = cache.find(p);
  if (it != cache.end()) return it->second;
  for (uint32_t a = 1; uint64_t(a) * a < p; ++a) {
    uint32_t b2 = p - a * a;
    uint32_t b = std::sqrt(b2);
    if (b * b == b2) return cache[p] = {int64_t(a), int64_t(b)};
  }
  std::abort();
}

static std::vector<GInt> gaussian_squares(
    uint32_t M, const std::vector<std::pair<uint32_t, uint32_t>>& fs,
    std::map<uint32_t, GInt>& cache) {
  std::vector<GInt> ws{{1, 0}};
  for (auto [p, k] : fs) {
    GInt pi = split_rep(p, cache), pb = conj(pi);
    std::vector<GInt> choices;
    for (uint32_t a = 0; a <= 2 * k; ++a)
      choices.push_back(mul(gpw(pi, a), gpw(pb, 2 * k - a)));
    std::vector<GInt> next;
    next.reserve(ws.size() * choices.size());
    for (GInt w : ws) for (GInt c : choices) next.push_back(mul(w, c));
    ws.swap(next);
  }
  std::vector<GInt> Gs;
  Gs.reserve(2 * ws.size());
  for (GInt w : ws) {
    GInt g = mul(w, w);
    Gs.push_back(g);
    Gs.push_back(neg(g));
  }
  std::sort(Gs.begin(), Gs.end());
  Gs.erase(std::unique(Gs.begin(), Gs.end()), Gs.end());
  for (GInt g : Gs) {
    i128 norm = i128(g.x) * g.x + i128(g.y) * g.y;
    if (norm != i128(M) * M * M * M) std::abort();
  }
  return Gs;
}

static u128 norm128(i128 x, i128 y) {
  return u128(x < 0 ? -x : x) * u128(x < 0 ? -x : x) +
         u128(y < 0 ? -y : y) * u128(y < 0 ? -y : y);
}
static u128 pow4(uint64_t q) { return u128(q) * q * q * q; }

static uint64_t fourth_root_if_exact(u128 n) {
  long double approx = std::sqrt(std::sqrt((long double)n));
  uint64_t q = std::max<uint64_t>(1, uint64_t(approx));
  // Floating point only supplies a nearby starting value.  Monotone exact
  // u128 comparisons determine the result, so rounding cannot create a false
  // positive or false negative within the documented scan bound.
  while (pow4(q) > n) --q;
  while (pow4(q) < n) ++q;
  return pow4(q) == n ? q : 0;
}

static bool prime_power(uint32_t q, const std::vector<uint32_t>& spf,
                        uint32_t& p, uint32_t& k) {
  p = spf[q]; k = 0;
  do { q /= p; ++k; } while (q > 1 && spf[q] == p);
  return q == 1;
}

static std::string str128(i128 n) {
  if (!n) return "0";
  bool minus = n < 0;
  u128 v = minus ? u128(-n) : u128(n);
  std::string s;
  while (v) { s.push_back(char('0' + v % 10)); v /= 10; }
  if (minus) s.push_back('-');
  std::reverse(s.begin(), s.end());
  return s;
}

struct SearchState {
  uint64_t norm_candidates = 0, fourth_norms = 0, prime_power_norms = 0;
  uint64_t pure_targets = 0, genuine_hits = 0, degenerate_hits = 0;
};

static void test_identity(uint32_t M, const std::vector<GInt>& terms,
                          const std::vector<int>& coeffs, i128 hx, i128 hy,
                          uint32_t constant, const std::vector<uint32_t>& spf,
                          std::map<uint32_t, GInt>& cache, SearchState& state) {
  const u128 M4 = u128(M) * M * M * M;
  u128 n = norm128(hx, hy);
  if (n <= M4 || n > u128(constant) * constant * M4) return;
  ++state.norm_candidates;
  uint64_t q64 = fourth_root_if_exact(n);
  if (!q64 || q64 <= M || q64 >= spf.size()) return;
  ++state.fourth_norms;
  uint32_t q = q64, p, k;
  if (!prime_power(q, spf, p, k) || p % 4 != 1 || M % p == 0) return;
  ++state.prime_power_norms;
  GInt rho = split_rep(p, cache);
  GInt target = gpw(rho, 4 * k);
  GInt H{int64_t(hx), int64_t(hy)};
  GInt A;
  if (H == target || H == neg(target)) A = conj(target);
  else if (H == conj(target) || H == neg(conj(target))) A = target;
  else return;
  ++state.pure_targets;
  std::vector<i128> Is, ds;
  for (GInt g : terms) {
    i128 I = i128(A.x) * g.y + i128(A.y) * g.x;
    Is.push_back(I);
    ds.push_back(I < 0 ? -I : I);
  }
  i128 check = 0;
  for (size_t i = 0; i < Is.size(); ++i) check += i128(coeffs[i]) * Is[i];
  bool distinct = std::all_of(ds.begin(), ds.end(), [](i128 d) { return d != 0; });
  for (size_t i = 0; i < ds.size(); ++i)
    for (size_t j = 0; j < i; ++j) if (ds[i] == ds[j]) distinct = false;
  bool p_units = std::all_of(ds.begin(), ds.end(), [p](i128 d) { return d % p != 0; });
  if (check != 0 || !distinct || !p_units) {
    ++state.degenerate_hits;
    return;
  }
  ++state.genuine_hits;
  std::cout << "HIT M=" << M << " q=" << q << " p=" << p << " k=" << k
            << " coeffs=";
  for (int c : coeffs) std::cout << c << ',';
  std::cout << " H=(" << str128(hx) << ',' << str128(hy) << ") d=";
  for (i128 d : ds) std::cout << str128(d) << ',';
  std::cout << " I_signs=";
  for (i128 I : Is) std::cout << (I > 0 ? '+' : '-') << ',';
  std::cout << '\n';
}

static void self_test() {
  auto spf = spf_sieve(100);
  std::map<uint32_t, GInt> cache;

  auto Gs = gaussian_squares(5, factor(5, spf), cache);
  const std::vector<GInt> expected{{-25, 0}, {-7, -24}, {-7, 24},
                                   {7, -24}, {7, 24}, {25, 0}};
  if (Gs != expected) {
    std::cerr << "self-test failed: Gaussian enumeration for M=5\n";
    std::exit(2);
  }
  if (fourth_root_if_exact(pow4(5)) != 5 ||
      fourth_root_if_exact(pow4(5) - 1) != 0 ||
      fourth_root_if_exact(pow4(5) + 1) != 0) {
    std::cerr << "self-test failed: exact fourth-root recognition\n";
    std::exit(2);
  }

  // Synthetic pipeline hits.  These terms deliberately do not lie on one
  // common norm circle: they isolate and exercise the code that recognizes
  // the known target conjugate((2+i)^4)=-7-24i, chooses its conjugate
  // multiplier, verifies the signed projection relation, distinctness, and
  // p-unit condition.  The production scan obtains terms only from the
  // separately checked gaussian_squares() enumerator above.
  SearchState s111, s211;
  test_identity(3, {{1, 0}, {0, 1}, {-8, -25}}, {1, 1, 1},
                -7, -24, 3, spf, cache, s111);
  // For type 211 use conjugate((2+3i)^4)=-119+120i with M=11,
  // so q=13 lies inside q^2 <= 2M^2.
  test_identity(11, {{1, 0}, {0, 1}, {-240, -241}}, {2, 1, 1},
                -119, -120, 2, spf, cache, s211);
  if (s111.fourth_norms != 1 || s111.prime_power_norms != 1 ||
      s111.pure_targets != 1 || s111.genuine_hits != 1 ||
      s211.fourth_norms != 1 || s211.prime_power_norms != 1 ||
      s211.pure_targets != 1 || s211.genuine_hits != 1) {
    std::cerr << "self-test failed: synthetic identity pipeline\n";
    std::exit(2);
  }
  std::cout << "self_test=ok\n";
}

int main(int argc, char** argv) {
  if (argc > 1 && std::string(argv[1]) == "--self-test") {
    self_test();
    return 0;
  }
  uint32_t limit = argc > 1 ? std::strtoul(argv[1], nullptr, 10) : 100000;
  uint32_t qlimit = uint32_t(std::ceil(std::sqrt(3.0) * limit)) + 10;
  auto spf = spf_sieve(qlimit);
  std::map<uint32_t, GInt> cache;
  SearchState s111, s211;
  uint64_t eligible = 0, Gtotal = 0, loops111 = 0, loops211 = 0;
  for (uint32_t M = 1; M <= limit; M += 2) {
    auto fs = factor(M, spf);
    bool ok = true;
    for (auto [p, k] : fs) if (p % 4 != 1) ok = false;
    if (!ok) continue;
    ++eligible;
    auto Gs = gaussian_squares(M, fs, cache);
    Gtotal += Gs.size();
    for (size_t i = 0; i < Gs.size(); ++i)
      for (size_t j = i; j < Gs.size(); ++j)
        for (size_t l = j; l < Gs.size(); ++l) {
          ++loops111;
          i128 hx = i128(Gs[i].x) + Gs[j].x + Gs[l].x;
          i128 hy = i128(Gs[i].y) + Gs[j].y + Gs[l].y;
          test_identity(M, {Gs[i], Gs[j], Gs[l]}, {1, 1, 1}, hx, hy, 3,
                        spf, cache, s111);
        }
    for (size_t i = 0; i < Gs.size(); ++i)
      for (size_t j = 0; j < Gs.size(); ++j)
        for (size_t l = j; l < Gs.size(); ++l) {
          ++loops211;
          i128 Hx = i128(2) * Gs[i].x + Gs[j].x + Gs[l].x;
          i128 Hy = i128(2) * Gs[i].y + Gs[j].y + Gs[l].y;
          if ((Hx & 1) || (Hy & 1)) std::abort();
          // Search the exact dominant identity H/2 = +/- bar(pi)^(4k).
          test_identity(M, {Gs[i], Gs[j], Gs[l]}, {2, 1, 1}, Hx / 2, Hy / 2,
                        2, spf, cache, s211);
        }
  }
  std::cout << "M_limit=" << limit << " eligible_M=" << eligible
            << " total_G_values=" << Gtotal << '\n';
  std::cout << "111_loops=" << loops111 << " norm_window=" << s111.norm_candidates
            << " fourth_norms=" << s111.fourth_norms
            << " prime_power_norms=" << s111.prime_power_norms
            << " pure_targets=" << s111.pure_targets << " genuine_hits=" << s111.genuine_hits
            << " degenerate_hits=" << s111.degenerate_hits << '\n';
  std::cout << "211_loops=" << loops211 << " norm_window=" << s211.norm_candidates
            << " fourth_norms=" << s211.fourth_norms
            << " prime_power_norms=" << s211.prime_power_norms
            << " pure_targets=" << s211.pure_targets << " genuine_hits=" << s211.genuine_hits
            << " degenerate_hits=" << s211.degenerate_hits << '\n';
}
