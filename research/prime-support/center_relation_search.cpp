// Exact bounded search for additive relations among centered square-pair
// offsets.  For each center root e, S_e contains every positive d for which
// e^2-d and e^2+d are integer squares.  The program exhausts all distinct
// three-offset relations with coefficient magnitudes {1,1,1} or {2,1,1}, and
// the full four-offset condition {a,b,a+b,|a-b|}.

#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <set>
#include <string>
#include <tuple>
#include <utility>
#include <vector>

struct PrimitiveTriple {
  uint32_t c, x, y;
};

struct Record {
  uint32_t e;
  uint64_t d;
  bool operator<(const Record& other) const {
    return e < other.e || (e == other.e && d < other.d);
  }
};

static std::vector<uint32_t> smallest_prime_factors(uint32_t n) {
  std::vector<uint32_t> spf(n + 1);
  std::iota(spf.begin(), spf.end(), 0);
  if (n >= 1) spf[1] = 1;
  for (uint32_t p = 2; uint64_t(p) * p <= n; ++p) {
    if (spf[p] != p) continue;
    for (uint64_t x = uint64_t(p) * p; x <= n; x += p) {
      if (spf[x] == x) spf[x] = p;
    }
  }
  return spf;
}

static std::vector<std::pair<uint32_t, uint32_t>> factor(
    uint32_t n, const std::vector<uint32_t>& spf) {
  std::vector<std::pair<uint32_t, uint32_t>> fs;
  while (n > 1) {
    uint32_t p = spf[n], k = 0;
    do {
      n /= p;
      ++k;
    } while (n > 1 && spf[n] == p);
    fs.emplace_back(p, k);
  }
  return fs;
}

static uint64_t ipow(uint64_t p, uint32_t k) {
  uint64_t q = 1;
  while (k--) q *= p;
  return q;
}

struct RelationCounts {
  uint64_t pair_tests = 0;
  uint64_t relation_111 = 0;
  uint64_t relation_211 = 0;
  uint64_t full_candidates = 0;
};

using RelationExample =
    std::tuple<uint32_t, uint64_t, uint64_t, uint64_t, const char*>;

static RelationCounts analyze_offsets(
    uint32_t e, const std::vector<uint64_t>& ds,
    std::vector<RelationExample>* relation_examples = nullptr) {
  RelationCounts counts;
  for (size_t i = 0; i < ds.size(); ++i) {
    for (size_t j = i + 1; j < ds.size(); ++j) {
      ++counts.pair_tests;
      const uint64_t a = ds[i], b = ds[j];
      const uint64_t diff = b - a, sum = a + b;
      const bool has_diff = std::binary_search(ds.begin(), ds.end(), diff);
      const bool has_sum = std::binary_search(ds.begin(), ds.end(), sum);
      if (has_diff && diff != a && diff != b) {
        ++counts.relation_111;
        if (relation_examples && relation_examples->size() < 20)
          relation_examples->emplace_back(e, diff, a, b, "111:diff+a=b");
      }
      if (has_sum && sum != a && sum != b) {
        ++counts.relation_111;
        if (relation_examples && relation_examples->size() < 20)
          relation_examples->emplace_back(e, a, b, sum, "111:a+b=sum");
      }
      const uint64_t twice_a_plus_b = 2 * a + b;
      const uint64_t a_plus_twice_b = a + 2 * b;
      const uint64_t twice_b_minus_a = 2 * b - a;
      if (std::binary_search(ds.begin(), ds.end(), twice_a_plus_b)) {
        ++counts.relation_211;
        if (relation_examples && relation_examples->size() < 20)
          relation_examples->emplace_back(e, a, b, twice_a_plus_b, "211:2a+b=c");
      }
      if (std::binary_search(ds.begin(), ds.end(), a_plus_twice_b)) {
        ++counts.relation_211;
        if (relation_examples && relation_examples->size() < 20)
          relation_examples->emplace_back(e, a, b, a_plus_twice_b, "211:a+2b=c");
      }
      if (twice_b_minus_a != a && twice_b_minus_a != b &&
          std::binary_search(ds.begin(), ds.end(), twice_b_minus_a)) {
        ++counts.relation_211;
        if (relation_examples && relation_examples->size() < 20)
          relation_examples->emplace_back(e, a, b, twice_b_minus_a, "211:a+c=2b");
      }
      if (has_diff && has_sum) {
        std::set<uint64_t> four{a, b, diff, sum};
        if (four.size() == 4) ++counts.full_candidates;
      }
    }
  }
  return counts;
}

static void self_test() {
  const auto positive = analyze_offsets(0, {1, 2, 3, 5});
  if (!positive.relation_111 || !positive.relation_211 ||
      !positive.full_candidates) {
    std::cerr << "self-test failed: synthetic positive relation set\n";
    std::exit(2);
  }
  const auto negative = analyze_offsets(0, {10, 23, 41});
  if (negative.relation_111 || negative.relation_211 ||
      negative.full_candidates) {
    std::cerr << "self-test failed: synthetic negative relation set\n";
    std::exit(2);
  }
  std::cout << "self_test=ok"
            << " positive_111_events=" << positive.relation_111
            << " positive_211_events=" << positive.relation_211
            << " positive_full_candidates=" << positive.full_candidates << '\n';
}

int main(int argc, char** argv) {
  if (argc > 1 && std::string(argv[1]) == "--self-test") {
    self_test();
    return 0;
  }
  const uint32_t limit = argc > 1 ? std::strtoul(argv[1], nullptr, 10) : 25000000;
  const uint32_t block_size = argc > 2 ? std::strtoul(argv[2], nullptr, 10) : 2000000;
  if (limit == 0 || limit > 500000000 || block_size == 0) {
    std::cerr << "limit must be in [1, 500000000] and block size must be positive\n";
    return 2;
  }
  const auto begin = std::chrono::steady_clock::now();
  auto spf = smallest_prime_factors(limit);
  uint64_t expected_centers_global = 0, expected_representations_global = 0;
  for (uint32_t e = 1; e <= limit; ++e) {
    uint64_t product = 1;
    for (const auto& [p, k] : factor(e, spf))
      if (p % 4 == 1) product *= (2 * k + 1);
    const uint64_t count = (product - 1) / 2;
    expected_representations_global += count;
    if (count) ++expected_centers_global;
  }

  std::vector<PrimitiveTriple> primitive;
  primitive.reserve(size_t(limit * 0.17));
  const uint32_t max_m = std::sqrt(limit);
  for (uint32_t m = 2; m <= max_m; ++m) {
    for (uint32_t n = 1; n < m; ++n) {
      const uint64_t c64 = uint64_t(m) * m + uint64_t(n) * n;
      if (c64 > limit) break;
      if (((m - n) & 1u) == 0 || std::gcd(m, n) != 1) continue;
      const uint32_t x = m * m - n * n;
      const uint32_t y = 2 * m * n;
      primitive.push_back({uint32_t(c64), x, y});
    }
  }

  uint64_t representations = 0, centers = 0, count_failures = 0, duplicate_failures = 0;
  uint64_t pair_tests = 0, relation_111 = 0, relation_211 = 0, full_candidates = 0;
  uint64_t eligible_centers = 0, eligible_four = 0;
  uint64_t fail_bound_2 = 0, fail_bound_sqrt3 = 0, fail_refined = 0;
  std::vector<RelationExample> relation_examples;

  for (uint32_t lo = 1; lo <= limit;) {
    const uint32_t hi = std::min<uint64_t>(limit, uint64_t(lo) + block_size - 1);
    std::vector<Record> records;
    records.reserve(size_t((hi - lo + 1) * 2.6));
    for (const auto& t : primitive) {
      if (t.c > hi) continue;
      const uint32_t k0 = std::max<uint32_t>(1, (lo + t.c - 1) / t.c);
      const uint32_t k1 = hi / t.c;
      for (uint32_t k = k0; k <= k1; ++k) {
        const uint32_t e = k * t.c;
        const uint64_t u = uint64_t(k) * t.x;
        const uint64_t v = uint64_t(k) * t.y;
        records.push_back({e, 2 * u * v});
      }
    }
    std::sort(records.begin(), records.end());
    representations += records.size();

    for (size_t at = 0; at < records.size();) {
      size_t end = at + 1;
      while (end < records.size() && records[end].e == records[at].e) ++end;
      const uint32_t e = records[at].e;
      ++centers;
      std::vector<uint64_t> ds;
      ds.reserve(end - at);
      for (size_t i = at; i < end; ++i) ds.push_back(records[i].d);
      if (std::adjacent_find(ds.begin(), ds.end()) != ds.end()) ++duplicate_failures;

      const auto fs = factor(e, spf);
      uint64_t expected_product = 1;
      bool eligible = e > 1;
      bool bound2 = true, bound3 = true, refined = true;
      for (const auto& [p, k] : fs) {
        if (p % 4 == 1) expected_product *= (2 * k + 1);
        else eligible = false;
        const uint64_t q = ipow(p, k), M = e / q;
        if (q > 2 * M) bound2 = false;
        if (q * q > 3 * M * M) bound3 = false;
        if (q * q > 3 * M * M || (p % 8 == 5 && q * q > 2 * M * M)) refined = false;
      }
      const uint64_t expected = (expected_product - 1) / 2;
      if (expected != ds.size()) ++count_failures;
      if (eligible) {
        ++eligible_centers;
        if (ds.size() >= 4) {
          ++eligible_four;
          if (!bound2) ++fail_bound_2;
          if (!bound3) ++fail_bound_sqrt3;
          if (!refined) ++fail_refined;
        }
      }

      const auto relation_counts = analyze_offsets(e, ds, &relation_examples);
      pair_tests += relation_counts.pair_tests;
      relation_111 += relation_counts.relation_111;
      relation_211 += relation_counts.relation_211;
      full_candidates += relation_counts.full_candidates;
      at = end;
    }
    std::cerr << "processed_root_centers_through=" << hi
              << " cumulative_representations=" << representations << '\n';
    if (hi == limit) break;
    lo = hi + 1;
  }

  const double elapsed = std::chrono::duration<double>(
      std::chrono::steady_clock::now() - begin).count();
  std::cout << "limit=" << limit << '\n';
  std::cout << "block_size=" << block_size << '\n';
  std::cout << "primitive_triples=" << primitive.size() << '\n';
  std::cout << "scaled_representations=" << representations << '\n';
  std::cout << "expected_scaled_representations=" << expected_representations_global << '\n';
  std::cout << "centers_with_representations=" << centers << '\n';
  std::cout << "expected_centers_with_representations=" << expected_centers_global << '\n';
  std::cout << "representation_count_failures=" << count_failures << '\n';
  std::cout << "duplicate_offset_failures=" << duplicate_failures << '\n';
  std::cout << "offset_pair_tests=" << pair_tests << '\n';
  std::cout << "relation_111_events=" << relation_111 << '\n';
  std::cout << "relation_211_events=" << relation_211 << '\n';
  std::cout << "full_candidates=" << full_candidates << '\n';
  std::cout << "eligible_primitive_centers=" << eligible_centers << '\n';
  std::cout << "eligible_centers_with_at_least_4_offsets=" << eligible_four << '\n';
  std::cout << "eligible_four_rejected_by_original_constant_2=" << fail_bound_2 << '\n';
  std::cout << "eligible_four_rejected_by_universal_sqrt3=" << fail_bound_sqrt3 << '\n';
  std::cout << "eligible_four_rejected_by_sqrt3_plus_p5mod8_sqrt2=" << fail_refined << '\n';
  std::cout << "relation_examples=" << relation_examples.size() << '\n';
  for (const auto& [e, a, b, c, type] : relation_examples)
    std::cout << "  e=" << e << " a=" << a << " b=" << b
              << " c=" << c << " type=" << type << '\n';
  std::cout << "elapsed_seconds=" << elapsed << '\n';
}
