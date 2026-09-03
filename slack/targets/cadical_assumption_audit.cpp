// Run frozen assumption cubes either in fresh CaDiCaL instances or through
// one persistent instance.  Output is TSV so every result remains auditable.

#include "cadical.hpp"

#include <chrono>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <memory>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

using Clock = std::chrono::steady_clock;

struct Cube {
  std::string name;
  std::string stratum;
  int manifest_index;
  std::vector<int> assumptions;
};

static std::vector<std::string> split(const std::string &line, char separator) {
  std::vector<std::string> fields;
  std::stringstream stream(line);
  std::string field;
  while (std::getline(stream, field, separator)) fields.push_back(field);
  return fields;
}

static std::vector<Cube> read_manifest(const std::string &path) {
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open manifest: " + path);
  std::vector<Cube> cubes;
  std::string line;
  while (std::getline(input, line)) {
    if (line.empty() || line[0] == '#') continue;
    const auto fields = split(line, '\t');
    if (fields.size() != 4) throw std::runtime_error("bad manifest row: " + line);
    Cube cube{fields[0], fields[1], std::stoi(fields[2]), {}};
    for (const auto &literal : split(fields[3], ',')) cube.assumptions.push_back(std::stoi(literal));
    if (cube.assumptions.empty()) throw std::runtime_error("cube has no assumptions");
    cubes.push_back(std::move(cube));
  }
  return cubes;
}

static std::unique_ptr<CaDiCaL::Solver> load_formula(const std::string &path) {
  auto solver = std::make_unique<CaDiCaL::Solver>();
  std::ifstream input(path);
  if (!input) throw std::runtime_error("cannot open CNF: " + path);
  std::string token;
  while (input >> token) {
    if (token == "c") {
      std::string rest;
      std::getline(input, rest);
    } else if (token == "p") {
      std::string format;
      int variables, clauses;
      input >> format >> variables >> clauses;
      if (format != "cnf") throw std::runtime_error("expected DIMACS CNF header");
      solver->resize(variables);
    } else if (token == "%") {
      break;
    } else {
      solver->add(std::stoi(token));
    }
  }
  return solver;
}

static int64_t choose(int n, int k) {
  if (k < 0 || k > n) return 0;
  int64_t result = 1;
  for (int i = 1; i <= k; ++i) result = result * (n - k + i) / i;
  return result;
}

static int64_t coverage(int positives, int negatives) {
  int64_t result = 0;
  const int remaining = 49 - positives - negatives;
  for (int size = positives; size <= 3; ++size)
    result += choose(remaining, size - positives);
  return result;
}

static double seconds_since(Clock::time_point start) {
  return std::chrono::duration<double>(Clock::now() - start).count();
}

static std::string join(const std::vector<int> &values) {
  std::ostringstream result;
  for (size_t index = 0; index < values.size(); ++index) {
    if (index) result << ',';
    result << values[index];
  }
  return result.str();
}

int main(int argc, char **argv) {
  if (argc != 5) {
    std::cerr << "usage: cadical_assumption_audit BASE.cnf MANIFEST.tsv fresh|persistent|propagate TICK_LIMIT\n";
    return 2;
  }
  const std::string cnf_path = argv[1];
  const auto cubes = read_manifest(argv[2]);
  const std::string mode = argv[3];
  const int tick_limit = std::stoi(argv[4]);
  if (mode != "fresh" && mode != "persistent" && mode != "propagate")
    throw std::runtime_error("invalid mode");
  if (tick_limit <= 0) throw std::runtime_error("tick limit must be positive");

  std::unique_ptr<CaDiCaL::Solver> persistent;
  double persistent_load_seconds = 0;
  if (mode == "persistent") {
    const auto start = Clock::now();
    persistent = load_formula(cnf_path);
    persistent_load_seconds = seconds_since(start);
  }

  std::cout << "name\tstratum\tmanifest_index\tmode\tresult\tload_s\tsolve_s"
               "\tticks\tconflicts\timplied_original\tcore_p\tcore_q\tcoverage\tcore\n";
  for (size_t cube_index = 0; cube_index < cubes.size(); ++cube_index) {
    const auto &cube = cubes[cube_index];
    std::unique_ptr<CaDiCaL::Solver> fresh;
    CaDiCaL::Solver *solver;
    double load_seconds = 0;
    if (mode == "fresh" || mode == "propagate") {
      const auto load_start = Clock::now();
      fresh = load_formula(cnf_path);
      load_seconds = seconds_since(load_start);
      solver = fresh.get();
    } else {
      solver = persistent.get();
      if (!cube_index) load_seconds = persistent_load_seconds;
    }

    const auto ticks_before = solver->get_statistic_value("ticks");
    const auto conflicts_before = solver->get_statistic_value("conflicts");
    for (const int literal : cube.assumptions) solver->assume(literal);
    solver->limit("ticks", tick_limit);
    const auto solve_start = Clock::now();
    const int result = mode == "propagate" ? solver->propagate() : solver->solve();
    const double solve_seconds = seconds_since(solve_start);
    const auto ticks = solver->get_statistic_value("ticks") - ticks_before;
    const auto conflicts = solver->get_statistic_value("conflicts") - conflicts_before;

    int implied_original = 0;
    if (mode == "propagate" && result != 20) {
      std::vector<int> implied;
      solver->implied(implied);
      for (const int literal : implied)
        if (49 < std::abs(literal) && std::abs(literal) <= 343) ++implied_original;
    }

    std::vector<int> core;
    int positives = 0, negatives = 0;
    if (result == 20) {
      for (const int literal : cube.assumptions) {
        if (solver->failed(literal)) {
          core.push_back(literal);
          if (literal > 0) ++positives;
          else ++negatives;
        }
      }
    }
    bool plane_content_core = result == 20;
    for (const int literal : cube.assumptions)
      if (std::abs(literal) > 49) plane_content_core = false;
    const int64_t covered = plane_content_core ? coverage(positives, negatives) : 0;
    std::cout << cube.name << '\t' << cube.stratum << '\t' << cube.manifest_index << '\t'
              << mode << '\t' << result << '\t' << std::fixed << std::setprecision(6)
              << load_seconds << '\t' << solve_seconds << '\t' << ticks << '\t' << conflicts
              << '\t' << implied_original << '\t' << positives << '\t' << negatives << '\t'
              << covered << '\t'
              << join(core) << '\n';
    std::cout.flush();
  }
}
