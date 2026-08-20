#include <algorithm>
#include <atomic>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <mutex>
#include <numeric>
#include <stdexcept>
#include <string>
#include <thread>
#include <unordered_set>
#include <utility>
#include <vector>

namespace {

using u64 = std::uint64_t;
using u128 = unsigned __int128;

struct Fraction {
    u64 numerator;
    u64 denominator;

    bool operator==(const Fraction&) const = default;
};

struct FractionHash {
    std::size_t operator()(const Fraction& value) const noexcept {
        const auto first = std::hash<u64>{}(value.numerator);
        const auto second = std::hash<u64>{}(value.denominator);
        return first ^ (second + 0x9e3779b97f4a7c15ULL + (first << 6U) + (first >> 2U));
    }
};

struct Counters {
    u64 pairs = 0;
    u64 relation_111 = 0;
    u64 relation_211 = 0;
};

u128 gcd128(u128 left, u128 right) {
    while (right != 0) {
        const u128 remainder = left % right;
        left = right;
        right = remainder;
    }
    return left;
}

bool less_fraction(const Fraction& left, const Fraction& right) {
    return static_cast<u128>(left.numerator) * right.denominator <
           static_cast<u128>(right.numerator) * left.denominator;
}

bool lookup_target(
    u128 numerator,
    u128 denominator,
    const std::unordered_set<Fraction, FractionHash>& values,
    Fraction* reduced = nullptr
) {
    if (numerator == 0 || numerator >= denominator) {
        return false;
    }
    const u128 divisor = gcd128(numerator, denominator);
    numerator /= divisor;
    denominator /= divisor;
    if (numerator > std::numeric_limits<u64>::max() ||
        denominator > std::numeric_limits<u64>::max()) {
        return false;
    }
    const Fraction candidate{
        static_cast<u64>(numerator), static_cast<u64>(denominator)};
    if (reduced != nullptr) {
        *reduced = candidate;
    }
    return values.contains(candidate);
}

void print_hit(
    const char* kind,
    const Fraction& left,
    const Fraction& right,
    const Fraction& target
) {
    std::cout << "hit=" << kind << " left=" << left.numerator << '/'
              << left.denominator << " right=" << right.numerator << '/'
              << right.denominator << " target=" << target.numerator << '/'
              << target.denominator << '\n';
}

Counters scan_relations(
    const std::vector<Fraction>& fractions,
    bool print_hits,
    std::size_t thread_count = 1
) {
    const std::unordered_set<Fraction, FractionHash> values(
        fractions.begin(), fractions.end());
    if (thread_count == 0) {
        throw std::invalid_argument("thread count must be positive");
    }
    thread_count = std::min(thread_count, std::max<std::size_t>(1, fractions.size()));

    constexpr std::size_t chunk_size = 16;
    std::atomic<std::size_t> next_left{0};
    std::mutex output_mutex;
    std::vector<Counters> local_counters(thread_count);
    std::vector<std::thread> workers;
    workers.reserve(thread_count);

    for (std::size_t worker_index = 0; worker_index < thread_count; ++worker_index) {
        workers.emplace_back([&, worker_index] {
            Counters& counters = local_counters[worker_index];
            while (true) {
                const std::size_t begin = next_left.fetch_add(
                    chunk_size, std::memory_order_relaxed);
                if (begin >= fractions.size()) {
                    break;
                }
                const std::size_t end = std::min(begin + chunk_size, fractions.size());
                for (std::size_t left_index = begin; left_index < end; ++left_index) {
                    const Fraction left = fractions[left_index];
                    for (std::size_t right_index = left_index + 1;
                         right_index < fractions.size(); ++right_index) {
                        const Fraction right = fractions[right_index];
                        ++counters.pairs;

                        const u128 common_denominator =
                            static_cast<u128>(left.denominator) * right.denominator;
                        const u128 left_scaled =
                            static_cast<u128>(left.numerator) * right.denominator;
                        const u128 right_scaled =
                            static_cast<u128>(right.numerator) * left.denominator;
                        Fraction target{};

                        auto record_hit = [&](const char* kind, bool relation_111) {
                            if (relation_111) {
                                ++counters.relation_111;
                            } else {
                                ++counters.relation_211;
                            }
                            if (print_hits) {
                                const std::lock_guard<std::mutex> lock(output_mutex);
                                print_hit(kind, left, right, target);
                            }
                        };

                        if (lookup_target(
                                left_scaled + right_scaled,
                                common_denominator,
                                values,
                                &target)) {
                            record_hit("111:x+y", true);
                        }

                        if (lookup_target(
                                2 * left_scaled + right_scaled,
                                common_denominator,
                                values,
                                &target)) {
                            record_hit("211:2x+y", false);
                        }

                        if (lookup_target(
                                left_scaled + 2 * right_scaled,
                                common_denominator,
                                values,
                                &target)) {
                            record_hit("211:x+2y", false);
                        }

                        if (lookup_target(
                                2 * right_scaled - left_scaled,
                                common_denominator,
                                values,
                                &target)) {
                            record_hit("211:x+z=2y", false);
                        }
                    }
                }
            }
        });
    }

    for (std::thread& worker : workers) {
        worker.join();
    }

    Counters total;
    for (const Counters& counters : local_counters) {
        total.pairs += counters.pairs;
        total.relation_111 += counters.relation_111;
        total.relation_211 += counters.relation_211;
    }
    return total;
}

std::vector<Fraction> primitive_offsets(u64 hypotenuse_limit) {
    std::vector<Fraction> fractions;
    for (u64 larger = 2; larger * larger < hypotenuse_limit; ++larger) {
        for (u64 smaller = 1; smaller < larger; ++smaller) {
            if (((larger - smaller) & 1U) == 0 ||
                std::gcd(larger, smaller) != 1) {
                continue;
            }
            const u64 hypotenuse = larger * larger + smaller * smaller;
            if (hypotenuse > hypotenuse_limit) {
                continue;
            }
            const u64 odd_leg = larger * larger - smaller * smaller;
            const u64 even_leg = 2 * larger * smaller;
            const u128 numerator = 2 * static_cast<u128>(odd_leg) * even_leg;
            const u128 denominator = static_cast<u128>(hypotenuse) * hypotenuse;
            if (numerator > std::numeric_limits<u64>::max() ||
                denominator > std::numeric_limits<u64>::max()) {
                throw std::overflow_error("fraction does not fit in 64 bits");
            }
            const Fraction value{
                static_cast<u64>(numerator), static_cast<u64>(denominator)};
            if (std::gcd(value.numerator, value.denominator) != 1) {
                throw std::logic_error("primitive offset fraction was not reduced");
            }
            fractions.push_back(value);
        }
    }

    std::sort(fractions.begin(), fractions.end(), less_fraction);
    fractions.erase(
        std::unique(fractions.begin(), fractions.end()), fractions.end());
    return fractions;
}

int self_test() {
    std::vector<Fraction> synthetic{{1, 10}, {1, 5}, {3, 10}, {1, 2}};
    std::sort(synthetic.begin(), synthetic.end(), less_fraction);
    const Counters counters = scan_relations(synthetic, false);
    if (counters.relation_111 == 0 || counters.relation_211 == 0) {
        std::cerr << "self-test failed to detect synthetic relations\n";
        return 1;
    }

    const auto real = primitive_offsets(500);
    const Counters real_counters = scan_relations(real, false);
    if (real_counters.relation_111 != 0 || real_counters.relation_211 != 0) {
        std::cerr << "self-test unexpectedly found a real relation\n";
        return 1;
    }
    std::cout << "self-test passed synthetic_111=" << counters.relation_111
              << " synthetic_211=" << counters.relation_211
              << " real_values=" << real.size() << '\n';
    return 0;
}

}  // namespace

int main(int argc, char** argv) {
    if (argc == 2 && std::string(argv[1]) == "--self-test") {
        return self_test();
    }
    if (argc != 2 && argc != 3) {
        std::cerr << "usage: rational_relation_search HYPOTENUSE_LIMIT [THREADS]\n";
        return 2;
    }
    const u64 limit = std::strtoull(argv[1], nullptr, 10);
    if (limit < 5 || limit > 1000000000ULL) {
        std::cerr << "hypotenuse limit must be between 5 and 1000000000\n";
        return 2;
    }

    const std::size_t thread_count = argc == 3
        ? static_cast<std::size_t>(std::strtoull(argv[2], nullptr, 10))
        : 1;
    if (thread_count == 0 || thread_count > 256) {
        std::cerr << "thread count must be between 1 and 256\n";
        return 2;
    }

    const auto fractions = primitive_offsets(limit);
    const Counters counters = scan_relations(fractions, true, thread_count);
    std::cout << "hypotenuse_limit=" << limit << '\n'
              << "threads=" << thread_count << '\n'
              << "primitive_offset_values=" << fractions.size() << '\n'
              << "offset_pairs=" << counters.pairs << '\n'
              << "relation_111_events=" << counters.relation_111 << '\n'
              << "relation_211_events=" << counters.relation_211 << '\n';
    return 0;
}
