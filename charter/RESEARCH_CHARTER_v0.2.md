# S.T.A.R. Research Charter v0.2

## Purpose

The S.T.A.R. Program is a research framework for testing proposed relationships among arithmetic invariants, geometric/topological structure, symbolic fields, and physical/cosmological observables.

This repository separates theory, claims, evidence, and experiments so that speculative statements are not silently treated as established results.

## Scientific posture

- ACSC, ECC, GLMPCT, RTCH, and related constructions are research hypotheses and formal models under test.
- BSD is used as inspiration, structural analogy, and a computational source of arithmetic objects; this project does not claim to prove BSD and empirical tests must remain BSD-independent where the registry specifies that requirement.
- A mapping is not assumed to be a bijection between all elliptic curves and observed cosmic structures. Projection families, degeneracy, many-to-one behavior, and isogeny classes must be recorded explicitly.
- Historical exploratory results are retained as R&D artifacts but are not automatically evidence for a preregistered claim.

## Evidence hierarchy

1. Reproducible controlled experiment
2. Independent replication
3. Robustness/null-model evidence
4. Exploratory computational result
5. Analytic/theoretical proposal
6. Historical or illustrative artifact

## Registry requirements

Every controlled experiment should identify Experiment_ID, Claim_IDs, Dataset_ID, Parameter_Set_ID, and Null_ID, plus analysis/provenance information sufficient to reproduce the result.

Parameter values discovered after seeing outcomes must not be relabeled as preregistered values.

## Repository workflow

Changes to scientific claims, registry definitions, controlled analysis code, and notebooks should be reviewable in a pull request. CI must validate software and registry integrity without modifying the research source of record.

Generated data belong in CI artifacts or explicitly versioned datasets, not automatic commits from CI.

## Current scope

This charter governs the repository restructuring and controlled experiment framework. The Data Provenance Registry is intentionally a subsequent work item and is not defined by this charter revision.
