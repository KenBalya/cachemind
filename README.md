# CacheMind

**Autonomous Workload-Aware Cache Policy Optimization**

CacheMind is an engineering and research project combining
LLM-guided experiment planning with deterministic,
high-performance C++20 cache simulation.

The goal is to investigate whether an autonomous AI agent
can discover better cache configurations than conventional
search methods under equal evaluation budgets.

## Research Questions

### RQ-A: Search Quality

Given the same workload, parameter search space, and
experiment budget, can an LLM-guided agent achieve better
held-out cache hit ratios than random search and fixed policies?

### RQ-B: Systems Performance

Can a C++20 cache simulator reproduce independently verified
cache semantics while achieving measurable performance
improvements over a Python reference implementation?

## Architecture

CacheMind separates orchestration from simulation.

### Python Control Plane

Responsible for:

- Workload preparation and analysis
- Agent planning and tool execution
- Experiment orchestration
- Search-budget enforcement
- Baseline evaluation
- Reporting and reproducibility

### C++ Execution Plane

Responsible for:

- Deterministic cache replay
- FIFO, LRU, and SLRU policies
- Byte-capacity enforcement
- Admission control
- Cache hit/miss accounting
- Native performance measurement

The agent does not participate in individual cache requests.

Instead, it proposes configurations that are evaluated by
the native simulator.

## Technology Stack

| Component | Technology |
|---|---|
| Operating System | Windows 11 x64 |
| Python | Python 3.12 |
| Package Manager | uv |
| Native Language | C++20 |
| Compiler | GCC / MSYS2 UCRT64 |
| Build System | CMake + Ninja |
| Python Testing | pytest |
| Native Testing | CTest |
| Linting | Ruff |
| CI | GitHub Actions |

## Development Setup

Clone the repository and enter the project directory.

```powershell
git clone https://github.com/KenBalya/cachemind.git
cd cachemind
```

Install project dependencies using uv:

```powershell
uv sync --locked
```

Verify the Python environment:

```powershell
uv run --locked python --version
```

## Python CLI

Display available commands:

```powershell
uv run --locked cachemind --help
```

Display project version:

```powershell
uv run --locked cachemind --version
```

Validate the Windows development environment:

```powershell
uv run --locked cachemind doctor
```

## Native C++ Build

The current native development toolchain uses
MSYS2 UCRT64 GCC on Windows.

Configure the native project:

```powershell
cmake -S native -B build/native -G Ninja `
    -DCMAKE_BUILD_TYPE=Release `
    -DBUILD_TESTING=ON `
    "-DCMAKE_CXX_COMPILER=C:/msys64/ucrt64/bin/g++.exe" `
    "-DCMAKE_MAKE_PROGRAM=C:/msys64/ucrt64/bin/ninja.exe"
```

Build:

```powershell
cmake --build build/native
```

Execute the native smoke program:

```powershell
.\build\native\cachemind-native-smoke.exe
```

## Testing

Python tests:

```powershell
uv run --locked pytest -v
```

Python linting:

```powershell
uv run --locked ruff check .
```

Python formatting check:

```powershell
uv run --locked ruff format --check .
```

Native C++ tests:

```powershell
ctest --test-dir build/native --output-on-failure
```

## Evaluation Design

The planned evaluation protocol includes:

- Chronological workload splitting
- Fixed byte-capacity constraints
- FIFO, LRU, and two-segment SLRU
- Size-aware admission control
- Bounded agent experimentation
- Equal-budget random search
- Held-out validation and testing
- C++ versus Python performance comparison

The primary optimization objective is request hit ratio.

Results will be reported from stored experiment artifacts
rather than assumed performance improvements.

## Development Status

The project is under active development.

Current foundation:

- Python package management with uv
- CacheMind CLI foundation
- Windows-native C++20 build configuration
- Native compilation smoke test
- Automated Python and native tests
- GitHub Actions CI

The workload processing pipeline, cache policies,
autonomous experiment manager, and evaluation framework
are subsequent implementation milestones.

## License

License selection is pending.