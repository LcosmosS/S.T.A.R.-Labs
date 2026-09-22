[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/LcosmosS/S.T.A.R.-Labs)

# S.T.A.R. Labs
## Symbolic–Topological–Arithmetic–Relativity

**Author:** Patrick J. McNamara  
**ORCiD:** 0009-0002-8978-5563  
**Project:** March 2025 — active research

**S.T.A.R. Labs** is a research program for investigating proposed relationships among arithmetic invariants, geometric and topological structure, symbolic fields, and physical/cosmological observables.

The repository is both a computational research archive and a controlled-experiment framework. Its purpose is to make speculative constructions explicit, testable, reproducible, and separable from established results.

> **Scientific status:** ACSC, ECC, GLMPCT, RTCH, and related constructions are hypotheses and formal models under test. They are not presented by this repository as established physical laws or mathematical theorems.

---

## Research Charter

The governing document is:

- **[RESEARCH_CHARTER_v0.2.md](charter/RESEARCH_CHARTER_v0.2.md)**

The charter establishes the project's scientific posture and repository controls.

### Core principles

> Do not ask whether the theory can be made to fit the universe. Ask whether a fixed mathematical construction predicts structure that was not used to construct it.
> ~ Michael Dine ~


1. **Hypotheses remain hypotheses.**  
   ACSC, ECC, GLMPCT, RTCH, and related constructions are research hypotheses or formal models unless supported by appropriate evidence.

2. **BSD is inspiration, not a claimed proof.**  
   Birch–Swinnerton-Dyer is used as structural inspiration, analogy, and a computational source of arithmetic objects. The project does not claim to prove BSD. Where registered, empirical tests are designed to be independent of BSD's proof status.

3. **Mappings are not assumed to be bijections.**  
   The project treats mappings from arithmetic objects to cosmic or geometric representations as projection families that may exhibit degeneracy, many-to-one behavior, and isogeny-class structure. These properties must be measured rather than assumed away.

4. **Exploration is not automatically evidence.**  
   Historical computational results are retained as R&D artifacts, but exploratory or illustrative results are not silently promoted to controlled evidence.

5. **Controls precede strong claims.**  
   Controlled experiments must identify their claim, dataset, parameter set, null model, and reproducibility/provenance information.

6. **CI validates; it does not rewrite the research record.**  
   Continuous integration is read-only with respect to the repository source of record. Generated outputs belong in CI artifacts or explicitly versioned datasets rather than automatic commits.

---

## Research architecture

The S.T.A.R. Labs research program currently spans several related components.

### **[ACSC](The_Arithmetic–Cosmic_Structure_Conjecture_(ACSC)_Monograph.pdf)** — Arithmetic–Cosmic Structure Conjecture

ACSC investigates whether computable arithmetic invariants can be mapped into geometric/topological representations that can be compared with cosmic data.

The repository treats the mapping problem as an empirical question. Candidate mappings and their null models are registered separately, including BSD-independent alternatives where specified.

### **[ECC](The_Entropy_Cohomology_Conjecture_(ECC).pdf)** — Entropy Cohomology Conjecture

ECC develops a symbolic entropy/cohomology framework intended to operationalize information-flow and field-like structures computationally.

Its registry status is a hypothesis requiring defined observables and falsifiable tests.

### **[GLMPCT](_Arithmetic_Invariants_and_Cosmological_Geometry_in_Cartography_.pdf)** — Global-to-Local Mapping Paradox Correction Theory

GLMPCT addresses the proposed relationship between global structure and local observations in the project's mapping framework. Its constructions are part of the broader research program and remain subject to explicit mathematical and empirical validation.

### **[RTCH](Relativistic_Thermodynamic_Cohomology.pdf)**

RTCH is a proposed thermodynamic/geometric coupling framework. The registered RTCH program includes a **standard-physics recovery limit** and numerical tests intended to determine whether the proposed construction can reproduce appropriate conventional limits.

### SFR and astronomical applications

The repository also investigates whether arithmetic/cosmological features provide predictive information for **star-formation-rate (SFR)** modeling. These are application hypotheses and are subject to leakage-controlled prediction, baseline comparison, robustness testing, and null-model comparison.

---

## Evidence hierarchy

The charter uses the following evidence hierarchy:

1. Reproducible controlled experiment
2. Independent replication
3. Robustness/null-model evidence
4. Exploratory computational result
5. Analytic/theoretical proposal
6. Historical or illustrative artifact

A numerical result appearing in an old notebook, manuscript, or exploratory script is therefore not by itself evidence for a registered claim.

---

## Registry and experiment control layer

The controlled research program is organized around stable registry identifiers.

Every controlled experiment is required to identify:

- **Experiment_ID**
- **Claim_ID(s)**
- **Dataset_ID**
- **Parameter_Set_ID**
- **Null_ID**
- reproducibility and provenance information sufficient to reconstruct the analysis

The current registry layer is:

| Registry | Purpose |
|---|---|
| [claim_evidence_v0.2.csv](registry/claim_evidence_v0.2.csv) | Registered claims and evidence requirements |
| [claim_experiment_crosswalk_v0.2.csv](registry/claim_experiment_crosswalk_v0.2.csv) | Claim-to-experiment relationships and required controls |
| [experiment_registry_v0.2.csv](registry/experiment_registry_v0.2.csv) | Registered controlled experiments |
| [dataset_registry_v0.1.csv](registry/dataset_registry_v0.1.csv) | Datasets and their current control/provenance status |
| [data_provenance_registry_v0.1.csv](registry/data_provenance_registry_v0.1.csv) | Dataset-level provenance, lineage, acquisition history, and provenance status |
| [parameter_registry_v0.1.csv](registry/parameter_registry_v0.1.csv) | Parameter sets and preregistration status |
| [null_registry_v0.1.csv](registry/null_registry_v0.1.csv) | Null/control models |
| [r&d_artifact_registry_v0.1.csv](registry/r%26d_artifact_registry_v0.1.csv) | Retained exploratory and historical artifacts |

### Current registry status

The registry tables currently contain planned experiments and placeholder parameter/null definitions where the controlled specifications still need to be fixed.

In particular:

- a parameter value discovered after seeing an outcome is **not** retroactively preregistered;
- planned experiments remain planned until their definitions are sufficiently specified;
- dataset records identify the intended data source but do not imply that a particular release/version has already been provenance-locked;
- the R&D artifact registry preserves historical work without promoting it to controlled evidence.

The **Data Provenance Registry is part of the current repository control layer** and is validated by the existing registry-validation CI job. Individual provenance records may still carry an `unknown`, `unverified`, or `partially_verified` status when their exact source, release/version, selection, acquisition history, or lineage has not yet been established. The provenance registry does not preregister experiment parameters, null models, or scientific claims.

---

## Controlled notebooks

The canonical controlled notebook suite is defined directly by:

- [.github/workflows/notebooks.yml](.github/workflows/notebooks.yml)

The current suite contains exactly these nine notebooks:

1. [00_registry_overview.ipynb](notebooks/00_registry_overview.ipynb)
2. [01_preprocessing.ipynb](notebooks/01_preprocessing.ipynb)
3. [02_arithmetic_reconstruction.ipynb](notebooks/02_arithmetic_reconstruction.ipynb)
4. [03_mapping_benchmark.ipynb](notebooks/03_mapping_benchmark.ipynb)
5. [04_rank_environment.ipynb](notebooks/04_rank_environment.ipynb)
6. [05_rank_topology.ipynb](notebooks/05_rank_topology.ipynb)
7. [06_null_models.ipynb](notebooks/06_null_models.ipynb)
8. [07_sfr_prediction.ipynb](notebooks/07_sfr_prediction.ipynb)
9. [08_robustness.ipynb](notebooks/08_robustness.ipynb)

The controlled-notebook workflow executes this exact set. Controlled notebooks are expected to be deterministic where practical, to fail rather than silently substitute missing scientific dependencies, and to distinguish computational fixtures from empirical evidence.

Exploratory and historical notebooks are retained separately under:

- [historical/r&d/](historical/r%26d/)
- [historical/legacy_notebooks/](historical/legacy_notebooks/)

They are not part of the controlled notebook manifest unless explicitly promoted through the research-control process.

---

## Repository structure

The repository contains both the current control layer and a substantial body of scientific code and historical research material.

```text
S.T.A.R.-Labs/
├── charter/
│   └── RESEARCH_CHARTER_v0.2.md
│
├── registry/
│   ├── claim_evidence_v0.2.csv
│   ├── claim_experiment_crosswalk_v0.2.csv
│   ├── experiment_registry_v0.2.csv
│   ├── dataset_registry_v0.1.csv
│   ├── data_provenance_registry_v0.1.csv
│   ├── parameter_registry_v0.1.csv
│   ├── null_registry_v0.1.csv
│   └── r&d_artifact_registry_v0.1.csv
│
├── src/
│   ├── acsc/                  # ACSC projection and arithmetic geometry
│   ├── analysis/              # Analysis/documentation utilities
│   ├── blender/               # Visualization and mapping utilities
│   ├── cli/                   # Command-line interfaces
│   ├── data/                  # Data and survey integration
│   ├── entropy/               # ECC entropy/cohomology machinery
│   ├── likelihoods/           # Cosmological likelihood components
│   ├── mappings/              # Mapping and projection machinery
│   ├── nulls/                 # Null-model utilities
│   ├── physics/               # Cosmological/physical model components
│   ├── pipeline/              # Analysis and inference pipelines
│   ├── statistics/            # Statistical utilities
│   ├── symbolic_regression/   # Symbolic law discovery
│   ├── tda/                   # Persistent homology and TDA
│   ├── tests/                 # Survey/integration tests
│   ├── utils/                 # Astronomical/general utilities
│   └── visualization/         # Figures and plotting
│
├── experiments/
│   ├── priority_a/
│   └── priority_b/
│
├── notebooks/                 # Canonical controlled notebook suite
│
├── historical/
│   ├── r&d/                  # Retained exploratory research
│   ├── legacy_notebooks/     # Legacy notebooks
│   ├── legacy_scripts/       # Legacy scripts
│   └── legacy_results/      # Historical outputs
│
├── tests/                    # Automated software tests
├── docs/                     # Project documentation and research documents
├── RTCH_E1/                  # RTCH experimental implementation
├── tools/                    # Supporting conversion/utility tools
│
├── .github/workflows/        # CI, controlled notebooks, survey tests
├── pyproject.toml
├── requirements.txt
└── README.md
```

The repository also contains manuscript-level documents, legacy material, survey integrations, RTCH experimental files, and other research artifacts that are intentionally not represented as controlled evidence merely because they are versioned.

---

## Computational methods

The codebase supports several complementary computational approaches:

- elliptic-curve and arithmetic-invariant computation;
- arithmetic-to-geometric projection experiments;
- alternative mapping constructions;
- persistent homology and related topological data analysis;
- Wasserstein and related persistence comparisons;
- null and permutation controls;
- symbolic regression and law-discovery experiments;
- cosmological likelihood and inference utilities;
- scalar-field, metric-perturbation, entropy, and related physics prototypes;
- astronomical/survey data integration;
- SFR prediction experiments;
- RTCH computational experiments.

The presence of an implementation does not imply that the corresponding scientific hypothesis has been validated.

---

## Reproducibility and CI

The repository uses automated checks to protect the research control layer.

The main CI workflow:

- runs the software test suite;
- validates registry foreign-key relationships and required fields;
- runs an arithmetic projection smoke test;
- produces CI metadata as an artifact;
- does not automatically commit generated research results.

The controlled-notebook workflow separately executes the nine canonical notebooks in a SageMath environment with the registered scientific dependencies.

Relevant workflows:

- [S.T.A.R. CI](.github/workflows/ci.yml)
- [Controlled Notebooks](.github/workflows/notebooks.yml)
- [Tests](.github/workflows/test.yml)
- [Sky Survey Pipeline](.github/workflows/sky_surveys.yml)

For local software testing:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e . --no-deps
pytest -q
```

The project currently targets **Python 3.12 or newer**.

For the controlled notebooks, the authoritative execution environment is defined by the workflow and currently uses the SageMath container.

---

## Documentation and theory

The repository contains the project's evolving theoretical and explanatory documents, including:

- [OVERVIEW.md](OVERVIEW.md)
- [1_STAR_Model.md](1_STAR_Model.md)
- [2_STARMAP.md](2_STARMAP.md)
- [3_SMAT.md](3_SMAT.md)
- [4_SFT.md](4_SFT.md)
- [First_Principles.md](First_Principles.md)
- [Symbolic_Action_Principle.md](Symbolic_Action_Principle.md)

The `docs/` area contains additional research documents, figures, manuscripts, and computational material.

These documents describe proposed theory and historical development; the charter and registries determine how claims are treated within the controlled research program.

---

## Historical and exploratory material

The repository deliberately preserves earlier research.

This includes exploratory notebooks, legacy scripts, earlier mapping experiments, prototype physics implementations, and historical numerical results.

Preservation is important for scientific provenance, but **version control is not equivalent to validation**. Historical material should be interpreted according to its registry status and the evidence hierarchy rather than its age, sophistication, or numerical performance.

---

## Installation

Basic installation:

```bash
git clone https://github.com/LcosmosS/S.T.A.R.-Labs.git
cd S.T.A.R.-Labs
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e . --no-deps
```

For development/testing:

```bash
pytest -q
```

For TDA functionality, the repository requirements include GUDHI, POT, Ripser, and Persim. The controlled notebook workflow installs the same repository requirements before execution.

---

## Current research scope

The current program is organized around several registered research areas:

- arithmetic reconstruction and mapping;
- BSD-independent alternative mapping tests;
- rank/environment and rank/topology studies;
- TDA correspondence and null-model testing;
- SFR prediction;
- RTCH standard-physics recovery;
- ECC field/cohomology testing.

The corresponding registered experiments are currently marked **planned** until their dataset versions, parameter definitions, null models, and execution specifications are sufficiently fixed.

This distinction is intentional: the repository is being built so that future numerical results can be evaluated against predefined controls rather than retrofitted into the research record.

---

## Future directions

Longer-term directions include:

- expanded arithmetic-to-cosmic mapping studies;
- independent replication of controlled results;
- stronger observational data provenance;
- expanded TDA and null-model analysis;
- development of the RTCH theoretical and computational framework;
- empirical testing of ECC structures;
- SFR prediction and astronomical applications;
- continued development of S.T.A.R.M.A.P. and S.M.A.T. concepts.

These are research directions, not claims of completed validation.

---

## Citation

If you use S.T.A.R. Labs Research or associated software, please cite:

```text
McNamara, P. J. (2026).
S.T.A.R. Labs Research: A Symbolic–Topological–Arithmetic–Relativity Program.
GitHub Repository.
https://github.com/LcosmosS/S.T.A.R.-Labs
```

BibTeX:

```bibtex
@misc{mcnamara2026star,
  author       = {Patrick J. McNamara},
  title        = {S.T.A.R. Labs Research: A Symbolic--Topological--Arithmetic--Relativity Program},
  year         = {2026},
  howpublished = {\url{https://github.com/LcosmosS/S.T.A.R.-Labs}},
  note         = {Research framework combining ACSC, ECC, GLMPCT, RTCH, and related computational programs}
}
```

---

## Research governance

The **Research Charter** is the authoritative reference for the repository's current scientific-control policy.

When README descriptions, historical documents, exploratory notebooks, or older results differ from the charter, the charter governs the interpretation of controlled research.


