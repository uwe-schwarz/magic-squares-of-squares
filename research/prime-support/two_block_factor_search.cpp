#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using i128 = __int128_t;
using u128 = __uint128_t;

namespace {

constexpr std::uint64_t kDefaultLimit = 1'000'000'000'000ULL;
constexpr std::uint64_t kMaximumLimit = 1'000'000'000'000ULL;

struct UInt256 {
  std::uint64_t limb[4]{};

  UInt256() = default;
  UInt256(std::uint64_t value) { limb[0] = value; }

  friend bool operator==(const UInt256& left, const UInt256& right) {
    return std::equal(std::begin(left.limb), std::end(left.limb),
                      std::begin(right.limb));
  }
  friend bool operator!=(const UInt256& left, const UInt256& right) {
    return !(left == right);
  }
  friend bool operator<(const UInt256& left, const UInt256& right) {
    for (int index = 3; index >= 0; --index) {
      if (left.limb[index] != right.limb[index]) {
        return left.limb[index] < right.limb[index];
      }
    }
    return false;
  }
  friend bool operator>(const UInt256& left, const UInt256& right) {
    return right < left;
  }

  static UInt256 multiply(u128 left, u128 right) {
    const std::uint64_t a[2]{static_cast<std::uint64_t>(left),
                             static_cast<std::uint64_t>(left >> 64)};
    const std::uint64_t b[2]{static_cast<std::uint64_t>(right),
                             static_cast<std::uint64_t>(right >> 64)};
    UInt256 product;
    for (int first = 0; first < 2; ++first) {
      u128 carry = 0;
      for (int second = 0; second < 2; ++second) {
        const int index = first + second;
        const u128 value = u128(a[first]) * b[second] +
                           product.limb[index] + carry;
        product.limb[index] = static_cast<std::uint64_t>(value);
        carry = value >> 64;
      }
      int index = first + 2;
      while (carry != 0 && index < 4) {
        const u128 value = u128(product.limb[index]) + carry;
        product.limb[index] = static_cast<std::uint64_t>(value);
        carry = value >> 64;
        ++index;
      }
      if (carry != 0) std::abort();
    }
    return product;
  }
};

UInt256 operator+(const UInt256& left, const UInt256& right) {
  UInt256 sum;
  u128 carry = 0;
  for (int index = 0; index < 4; ++index) {
    const u128 value = u128(left.limb[index]) + right.limb[index] + carry;
    sum.limb[index] = static_cast<std::uint64_t>(value);
    carry = value >> 64;
  }
  if (carry != 0) std::abort();
  return sum;
}

UInt256 operator-(const UInt256& left, const UInt256& right) {
  if (left < right) std::abort();
  UInt256 difference;
  std::uint64_t borrow = 0;
  for (int index = 0; index < 4; ++index) {
    const u128 subtrahend = u128(right.limb[index]) + borrow;
    const u128 minuend = left.limb[index];
    difference.limb[index] =
        static_cast<std::uint64_t>(minuend - subtrahend);
    borrow = minuend < subtrahend;
  }
  if (borrow != 0) std::abort();
  return difference;
}

UInt256 operator*(const UInt256& value, std::uint32_t factor) {
  UInt256 product;
  u128 carry = 0;
  for (int index = 0; index < 4; ++index) {
    const u128 term = u128(value.limb[index]) * factor + carry;
    product.limb[index] = static_cast<std::uint64_t>(term);
    carry = term >> 64;
  }
  if (carry != 0) std::abort();
  return product;
}

struct Signed256 {
  bool negative = false;
  UInt256 magnitude;
};

u128 unsigned_abs(i128 value) {
  return value < 0 ? u128(-(value + 1)) + 1 : u128(value);
}

Signed256 signed_product(i128 left, i128 right) {
  if (left == 0 || right == 0) return {};
  return {static_cast<bool>((left < 0) != (right < 0)),
          UInt256::multiply(unsigned_abs(left), unsigned_abs(right))};
}

Signed256 signed_sum(const Signed256& left, const Signed256& right) {
  if (left.magnitude == UInt256(0)) return right;
  if (right.magnitude == UInt256(0)) return left;
  if (left.negative == right.negative) {
    return {left.negative, left.magnitude + right.magnitude};
  }
  if (left.magnitude == right.magnitude) return {};
  if (left.magnitude > right.magnitude) {
    return {left.negative, left.magnitude - right.magnitude};
  }
  return {right.negative, right.magnitude - left.magnitude};
}

struct Gaussian {
  i128 real;
  i128 imag;
};

struct Block {
  std::uint64_t value;
  std::uint32_t prime;
  std::uint32_t exponent;
  std::vector<Gaussian> local_squares;
};

struct Summary {
  std::uint64_t blocks = 0;
  std::uint64_t dominant_blocks = 0;
  std::uint64_t block_pairs = 0;
  std::uint64_t offset_values = 0;
  std::uint64_t offset_pair_tests = 0;
  std::uint64_t relation_events = 0;
  std::uint64_t candidate_pairs = 0;
};

Gaussian multiply(const Gaussian& left, const Gaussian& right) {
  return {
      left.real * right.real - left.imag * right.imag,
      left.real * right.imag + left.imag * right.real,
  };
}

Gaussian power(Gaussian base, std::uint32_t exponent) {
  Gaussian result{1, 0};
  while (exponent != 0) {
    if ((exponent & 1U) != 0) result = multiply(result, base);
    exponent >>= 1U;
    if (exponent != 0) base = multiply(base, base);
  }
  return result;
}

std::uint64_t integer_square_root(std::uint64_t value) {
  std::uint64_t root = static_cast<std::uint64_t>(std::sqrt(value));
  while ((root + 1) <= value / (root + 1)) ++root;
  while (root > value / root) --root;
  return root;
}

std::vector<bool> prime_sieve(std::uint32_t limit) {
  std::vector<bool> is_prime(limit + 1, true);
  is_prime[0] = false;
  if (limit >= 1) is_prime[1] = false;
  for (std::uint32_t prime = 2;
       std::uint64_t(prime) * prime <= limit; ++prime) {
    if (!is_prime[prime]) continue;
    for (std::uint64_t multiple = std::uint64_t(prime) * prime;
         multiple <= limit; multiple += prime) {
      is_prime[static_cast<std::size_t>(multiple)] = false;
    }
  }
  return is_prime;
}

std::uint64_t modular_power(std::uint64_t base, std::uint64_t exponent,
                            std::uint64_t modulus) {
  std::uint64_t result = 1;
  while (exponent != 0) {
    if ((exponent & 1U) != 0) {
      result = static_cast<std::uint64_t>(
          (u128(result) * base) % modulus);
    }
    exponent >>= 1U;
    if (exponent != 0) {
      base = static_cast<std::uint64_t>((u128(base) * base) % modulus);
    }
  }
  return result;
}

bool three_halves_is_fourth_power(std::uint32_t prime) {
  const std::uint64_t inverse_two = (std::uint64_t(prime) + 1) / 2;
  const std::uint64_t residue = (3 * inverse_two) % prime;
  return modular_power(residue, (prime - 1) / 4, prime) == 1;
}

Gaussian split_prime(std::uint32_t prime) {
  // Every prime entering the scan is 1 modulo 8.  Choose the associate with
  // positive odd real coordinate and positive even imaginary coordinate.
  for (std::uint32_t imag = 2;
       std::uint64_t(imag) * imag < prime; imag += 2) {
    const std::uint64_t real_squared = prime - std::uint64_t(imag) * imag;
    const std::uint64_t real = integer_square_root(real_squared);
    if ((real & 1U) != 0 && real * real == real_squared) {
      return {real, imag};
    }
  }
  throw std::runtime_error("split-prime representation not found");
}

i128 integer_power(std::uint32_t base, std::uint32_t exponent) {
  i128 result = 1;
  for (std::uint32_t index = 0; index < exponent; ++index) result *= base;
  return result;
}

std::vector<Gaussian> local_squared_factors(std::uint32_t prime,
                                             std::uint32_t exponent) {
  const Gaussian pi = split_prime(prime);
  std::vector<Gaussian> factors;
  factors.reserve(2 * exponent + 1);
  for (std::int32_t index = -static_cast<std::int32_t>(exponent);
       index <= static_cast<std::int32_t>(exponent); ++index) {
    const std::uint32_t magnitude =
        static_cast<std::uint32_t>(index < 0 ? -index : index);
    Gaussian factor = power(pi, 4 * magnitude);
    if (index < 0) factor.imag = -factor.imag;
    const i128 scale = integer_power(prime, 2 * (exponent - magnitude));
    factor.real *= scale;
    factor.imag *= scale;
    factors.push_back(std::move(factor));
  }
  return factors;
}

std::vector<Block> enumerate_blocks(std::uint64_t limit) {
  const std::uint32_t prime_limit =
      static_cast<std::uint32_t>(integer_square_root(limit));
  const std::vector<bool> is_prime = prime_sieve(prime_limit);
  std::vector<Block> blocks;
  for (std::uint32_t prime = 17; prime <= prime_limit; ++prime) {
    if (!is_prime[prime] || prime % 8 != 1) continue;
    std::uint64_t value = std::uint64_t(prime) * prime;
    std::uint32_t exponent = 2;
    while (value <= limit) {
      blocks.push_back(
          {value, prime, exponent, local_squared_factors(prime, exponent)});
      if (value > limit / prime) break;
      value *= prime;
      ++exponent;
    }
  }
  std::sort(blocks.begin(), blocks.end(),
            [](const Block& left, const Block& right) {
              if (left.value != right.value) return left.value < right.value;
              return left.prime < right.prime;
            });
  return blocks;
}

bool is_dominant_eligible(const Block& block) {
  return block.exponent >= 3 && block.prime % 24 == 1 &&
         three_halves_is_fourth_power(block.prime);
}

bool passes_height_bound(std::uint64_t dominant, std::uint64_t smaller) {
  return u128(dominant) * dominant < u128(3) * smaller * smaller;
}

std::vector<UInt256> offsets_for_pair(const Block& left,
                                      const Block& right) {
  std::vector<UInt256> offsets;
  offsets.reserve(left.local_squares.size() * right.local_squares.size());
  for (const Gaussian& first : left.local_squares) {
    for (const Gaussian& second : right.local_squares) {
      const Signed256 imag = signed_sum(
          signed_product(first.real, second.imag),
          signed_product(first.imag, second.real));
      if (imag.magnitude != UInt256(0)) offsets.push_back(imag.magnitude);
    }
  }
  std::sort(offsets.begin(), offsets.end());
  offsets.erase(std::unique(offsets.begin(), offsets.end()), offsets.end());
  return offsets;
}

std::uint64_t count_relations(const std::vector<UInt256>& offsets,
                              std::uint64_t& pair_tests) {
  const std::uint64_t size = offsets.size();
  pair_tests += size * (size - 1) / 2;
  std::uint64_t relations = 0;
  for (std::size_t first = 0; first < offsets.size(); ++first) {
    for (std::size_t second = first + 1; second < offsets.size(); ++second) {
      const UInt256& a = offsets[first];
      const UInt256& b = offsets[second];
      if (b == a * 2) continue;  // |b-a|=a would repeat an opposite pair.
      const UInt256 difference = b - a;
      const UInt256 sum = b + a;
      if (std::binary_search(offsets.begin(), offsets.end(), difference) &&
          std::binary_search(offsets.begin(), offsets.end(), sum)) {
        ++relations;
      }
    }
  }
  return relations;
}

std::uint64_t offset_fingerprint(const std::vector<UInt256>& offsets) {
  std::uint64_t hash = 1469598103934665603ULL;
  for (const UInt256& value : offsets) {
    for (std::uint64_t limb : value.limb) {
      hash ^= limb;
      hash *= 1099511628211ULL;
    }
  }
  return hash;
}

Summary scan(std::uint64_t limit, bool print_hits) {
  const std::vector<Block> blocks = enumerate_blocks(limit);
  Summary summary;
  summary.blocks = blocks.size();

  for (const Block& dominant : blocks) {
    if (!is_dominant_eligible(dominant)) continue;
    ++summary.dominant_blocks;
    for (const Block& smaller : blocks) {
      if (smaller.value >= dominant.value) break;
      if (smaller.prime == dominant.prime ||
          !passes_height_bound(dominant.value, smaller.value)) {
        continue;
      }
      ++summary.block_pairs;
      const std::vector<UInt256> offsets = offsets_for_pair(dominant, smaller);
      summary.offset_values += offsets.size();
      const std::uint64_t relations =
          count_relations(offsets, summary.offset_pair_tests);
      if (relations != 0) {
        ++summary.candidate_pairs;
        summary.relation_events += relations;
        if (print_hits) {
          std::cout << "HIT dominant=" << dominant.value
                    << " smaller=" << smaller.value
                    << " p=" << dominant.prime
                    << " k=" << dominant.exponent
                    << " q=" << smaller.prime
                    << " ell=" << smaller.exponent
                    << " relations=" << relations << '\n';
        }
      }
    }
  }
  return summary;
}

void self_test() {
  const std::vector<UInt256> positive{1, 2, 3, 4};
  const std::vector<UInt256> negative{1, 2, 4};
  std::uint64_t tests = 0;
  if (count_relations(positive, tests) != 1 || tests != 6) std::abort();
  tests = 0;
  if (count_relations(negative, tests) != 0 || tests != 3) std::abort();

  const Block first{17 * 17, 17, 2, local_squared_factors(17, 2)};
  const Block second{41 * 41, 41, 2, local_squared_factors(41, 2)};
  if (first.local_squares.size() != 5 || second.local_squares.size() != 5) {
    std::abort();
  }
  const i128 expected_norm = integer_power(17, 8);
  for (const Gaussian& value : first.local_squares) {
    if (value.real * value.real + value.imag * value.imag != expected_norm) {
      std::abort();
    }
  }
  const std::vector<UInt256> offsets = offsets_for_pair(first, second);
  if (offsets.empty() || !std::is_sorted(offsets.begin(), offsets.end()) ||
      std::adjacent_find(offsets.begin(), offsets.end()) != offsets.end()) {
    std::abort();
  }
  std::cout << "self_test=ok synthetic_relations=1 gaussian_offsets="
            << offsets.size() << '\n';
}

std::uint64_t parse_limit(const std::string& argument) {
  std::size_t parsed = 0;
  const std::uint64_t value = std::stoull(argument, &parsed);
  if (parsed != argument.size() || value < 17 * 17 ||
      value > kMaximumLimit) {
    throw std::runtime_error("limit must be between 289 and 1000000000000");
  }
  return value;
}

std::uint32_t parse_u32(const std::string& argument, const char* name) {
  std::size_t parsed = 0;
  const std::uint64_t value = std::stoull(argument, &parsed);
  if (parsed != argument.size() || value > UINT32_MAX) {
    throw std::runtime_error(std::string("invalid ") + name);
  }
  return static_cast<std::uint32_t>(value);
}

std::uint64_t checked_block_value(std::uint32_t prime,
                                  std::uint32_t exponent) {
  std::uint64_t value = 1;
  for (std::uint32_t index = 0; index < exponent; ++index) {
    if (prime == 0 || value > kMaximumLimit / prime) {
      throw std::runtime_error("pair block exceeds the supported limit");
    }
    value *= prime;
  }
  return value;
}

void inspect_pair(std::uint32_t first_prime, std::uint32_t first_exponent,
                  std::uint32_t second_prime,
                  std::uint32_t second_exponent) {
  if (first_prime == second_prime || first_prime % 8 != 1 ||
      second_prime % 8 != 1 || first_exponent < 2 || second_exponent < 2) {
    throw std::runtime_error(
        "pair requires distinct primes 1 mod 8 and exponents at least 2");
  }
  const std::uint32_t prime_limit = std::max(first_prime, second_prime);
  const std::vector<bool> is_prime = prime_sieve(prime_limit);
  if (!is_prime[first_prime] || !is_prime[second_prime]) {
    throw std::runtime_error("pair bases must be prime");
  }
  const Block first{checked_block_value(first_prime, first_exponent),
                    first_prime, first_exponent,
                    local_squared_factors(first_prime, first_exponent)};
  const Block second{checked_block_value(second_prime, second_exponent),
                     second_prime, second_exponent,
                     local_squared_factors(second_prime, second_exponent)};
  const std::vector<UInt256> offsets = offsets_for_pair(first, second);
  std::uint64_t pair_tests = 0;
  const std::uint64_t relations = count_relations(offsets, pair_tests);
  std::cout << "pair_p=" << first_prime << '\n'
            << "pair_k=" << first_exponent << '\n'
            << "pair_q=" << second_prime << '\n'
            << "pair_ell=" << second_exponent << '\n'
            << "offset_values=" << offsets.size() << '\n'
            << "offset_pair_tests=" << pair_tests << '\n'
            << "relation_events=" << relations << '\n'
            << "offset_fingerprint=" << offset_fingerprint(offsets) << '\n';
}

}  // namespace

int main(int argc, char** argv) {
  try {
    if (argc == 2 && std::string(argv[1]) == "--self-test") {
      self_test();
      return 0;
    }
    if (argc == 6 && std::string(argv[1]) == "--pair") {
      inspect_pair(parse_u32(argv[2], "first prime"),
                   parse_u32(argv[3], "first exponent"),
                   parse_u32(argv[4], "second prime"),
                   parse_u32(argv[5], "second exponent"));
      return 0;
    }
    if (argc > 2) {
      std::cerr << "usage: " << argv[0]
                << " [limit|--self-test|--pair p k q ell]\n";
      return 2;
    }
    const std::uint64_t limit =
        argc == 2 ? parse_limit(argv[1]) : kDefaultLimit;
    const auto start = std::chrono::steady_clock::now();
    const Summary summary = scan(limit, true);
    const double seconds = std::chrono::duration<double>(
                               std::chrono::steady_clock::now() - start)
                               .count();
    std::cout << "limit=" << limit << '\n'
              << "blocks=" << summary.blocks << '\n'
              << "dominant_blocks=" << summary.dominant_blocks << '\n'
              << "block_pairs=" << summary.block_pairs << '\n'
              << "offset_values=" << summary.offset_values << '\n'
              << "offset_pair_tests=" << summary.offset_pair_tests << '\n'
              << "relation_events=" << summary.relation_events << '\n'
              << "candidate_pairs=" << summary.candidate_pairs << '\n'
              << "elapsed_seconds=" << seconds << '\n';
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "error: " << error.what() << '\n';
    return 2;
  }
}
