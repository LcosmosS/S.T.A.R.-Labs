[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/LcosmosS/S.T.A.R.-Program)

# Contributing to S.T.A.R. Labs Research Program

**S.T.A.R. Labs Research Program** (Symbolic–Topological–Arithmetic–Relativity) is an open research project exploring a novel framework for mathematical and theoretical physics. Contributions are welcome from researchers, developers, and enthusiasts committed to rigorous, reproducible, and innovative work at the intersection of mathematical-physics and number theory, topology, symbolic computation, theroetical-physics, and cosmology.

## Code of Conduct

All contributors are expected to adhere to the [Code of Conduct](CODE_OF_CONDUCT.md), based on the [Contributor Covenant](https://www.contributor-covenant.org). Respectful, constructive, and inclusive collaboration is highly valued.

## Ways to Contribute

Contributions are welcome in several areas:

- **Theoretical Developments** — Extensions to the ACSC or ECC conjectures, new lemmas, or mathematical refinements.
- **Computational Cosmology** — Improvements to MCMC pipelines, likelihood functions, or symbolic regression.
- **Topological Data Analysis** — Enhancements to persistent homology pipelines and stability analysis.
- **Software Engineering** — Performance optimization, robustness, testing, and CI/CD improvements.
- **Documentation & Visualization** — Better notebooks, figures, and explanatory materials.
- **Data & Infrastructure** — Curating cosmological datasets and improving data loaders.

## Development Setup

### Prerequisites
- Python 3.10+
- SageMath (recommended for symbolic computation)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/LcosmosS/S.T.A.R.-Labs.git
```
```bash
# Checkout the repository
cd S.T.A.R.-Labs
```
```bash
# Install in editable mode with development dependencies
pip install -e ".[dev]"
```
```bash
# (Optional but recommended) Install SageMath packages if needed
sage -pip install -e ".[dev]"
```
### Running Notebooks

All core demonstrations are in the examples/ directory:
```bash
jupyter nbconvert --to notebook --execute examples/full_cosmology_inference.ipynb --output examples/full_cosmology_inference-executed.ipynb
```
### Project Structure
```
textsrc/
├── likelihoods/           # Data loaders and cosmological likelihoods
├── physics/               # Core models, symbolic cosmology, and MCMC
├── pipeline/              # Analysis and figure-generation pipelines
├── visualization/         # Publication-quality plotting tools
├── acsc/                  # Arithmetic-Cosmic Structure Conjecture modules
├── ecc/                   # Entropy Cohomology Conjecture modules
└── tda/                   # Topological Data Analysis tools

examples/                  # Jupyter notebooks demonstrating key features
data/                      # Raw and processed cosmological datasets
```

### SageMath-Specific Notes

Many symbolic and algebraic features rely on SageMath.
Use SageMath kernels in Jupyter for best compatibility.
When writing code that uses Sage features (RealNumber, Integer, symbolic rings, etc.), prefer explicit imports.
Test notebooks with both standard Python and SageMath kernels when possible.

### Citation Guidelines
If your contribution results in academic output (papers, theses, presentations), please cite the project as:
```bash
bibtex@software{star_labs,
  author       = {Patrick J. McNamara and contributors},
  title        = {S.T.A.R. Labs Research: A Symbolic--Topological--Arithmetic--Relativity Program},
  year         = {2026},
  url          = {https://github.com/LcosmosS/S.T.A.R.-Labs},
  doi          = {TBD},
}
```
We also encourage citing the foundational papers on ACSC and ECC once they are published. Contributors making significant theoretical or algorithmic contributions may be offered co-authorship on resulting publications.

### Contributor Ladder & Governance
We follow a lightweight, merit-based governance model:

#### Roles

- Maintainer: Final approval on PRs, strategic direction.
- Core Contributor: Regular high-quality contributions, can review PRs.
- Contributor: Anyone who has had a PR merged.

### Recognition
All contributors are listed in AUTHORS.md. Significant contributors (theoretical breakthroughs, major modules, sustained high-quality work) may be invited to join the core team.

### Pull Request Process

1. Fork the repository and create a feature branch:
```bash
git checkout -b feature/your-contribution-name
```
2. Make your changes following the style guidelines below.
3. Ensure all modified notebooks execute successfully.
4. Submit a Pull Request with a clear title and description.

#### PR Requirements

1. Clear motivation and description of changes
2. All affected notebooks must run end-to-end
3. Code must pass Black formatting
4. Appropriate tests or validation (when applicable)
5. Updated documentation where relevant

#### PR Checklist
```
▢ Code passes Black formatting
▢ Notebooks run end-to-end without errors
▢ Appropriate docstrings and comments
▢ Follows SageMath compatibility practices (when applicable)
▢ Updates to documentation or citation files if relevant
```
### Style Guide

- Code Formatting: Use Black with default settings.
- Docstrings: Google style.
- Type Hints: Encouraged for new code.
- Naming: Use descriptive variable and function names.
- Reproducibility: Prefer explicit seeds and deterministic behavior where possible.

### Testing
```bash
# Run all notebooks (recommended before submitting PR)
./scripts/run_all_notebooks.sh
```
### Recognition
All contributors will be acknowledged in the AUTHORS.md file and in relevant publications where appropriate. Significant theoretical or algorithmic contributions may warrant co-authorship on resulting papers.

### Questions?
- Use GitHub Discussions for ideas, questions, or theoretical discussions.
- or Feel free to contact the maintainer.
- *For bugs or feature requests, open an Issue.*

**Thank you for contributing to the advancement of mathematical and theoretical physics.**
