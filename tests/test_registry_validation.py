"""Unit tests for the CSV reader embedded in the registry-validation workflow."""

import ast
import csv
import re
import textwrap
from pathlib import Path

import pytest


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHANGED_REGISTRY_TABLES = [
    "data_provenance_registry_v0.1.csv",
    "dataset_registry_v0.1.csv",
    "experiment_registry_v0.2.csv",
    "null_registry_v0.1.csv",
    "parameter_registry_v0.1.csv",
    "placeholder_tbd_reconciliation_matrix_v0.1.csv",
]


def _registry_validation_script():
    """Return the exact Python heredoc used by the registry-validation job."""
    workflow = (REPOSITORY_ROOT / ".github" / "workflows" / "ci.yml").read_text(
        encoding="utf-8"
    )
    job = workflow.split("- name: Validate registry tables", maxsplit=1)[1]
    heredoc = job.split("python - <<'PY'\n", maxsplit=1)[1]
    script = heredoc.split("\n          PY", maxsplit=1)[0]
    return textwrap.dedent(script)


def _load_rows_function(root):
    """Load only rows() so semantic registry checks do not obscure its behavior."""
    module = ast.parse(_registry_validation_script())
    rows_function = next(
        node
        for node in module.body
        if isinstance(node, ast.FunctionDef) and node.name == "rows"
    )
    namespace = {"csv": csv, "root": root}
    function_module = ast.Module(body=[rows_function], type_ignores=[])
    exec(compile(function_module, filename="ci.yml:rows", mode="exec"), namespace)
    return namespace["rows"]


def _write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        csv.writer(stream).writerows(rows)


def test_pr_changed_registry_tables_have_consistent_field_counts():
    rows = _load_rows_function(REPOSITORY_ROOT / "registry")

    for name in CHANGED_REGISTRY_TABLES:
        assert rows(name), f"expected at least one record in {name}"


def test_returns_header_keyed_records_for_quoted_multiline_values(tmp_path):
    _write_csv(
        tmp_path / "example.csv",
        [["id", "description", "optional"], ["1", "alpha, beta\nsecond line", ""]],
    )

    records = _load_rows_function(tmp_path)("example.csv")

    assert records == [
        {"id": "1", "description": "alpha, beta\nsecond line", "optional": ""}
    ]


@pytest.mark.parametrize("data_row", [1, 2], ids=["first-row", "later-row"])
@pytest.mark.parametrize("field_delta", [-1, 1], ids=["missing-field", "extra-field"])
def test_rejects_inconsistent_field_counts_with_file_and_row(
    tmp_path, data_row, field_delta
):
    name = "example.csv"
    path = tmp_path / name
    table = [["id", "value"], ["1", "alpha"], ["2", "beta"]]
    expected_fields = len(table[0])
    if field_delta < 0:
        table[data_row] = table[data_row][:-1]
    else:
        table[data_row].append("unexpected")
    _write_csv(path, table)

    with pytest.raises(AssertionError) as error:
        _load_rows_function(tmp_path)(name)

    actual_fields = expected_fields + field_delta
    assert str(error.value) == (
        f"CSV field-count mismatch: {name}:{data_row + 1} "
        f"expected {expected_fields} fields, got {actual_fields}"
    )


def test_rejects_blank_data_record(tmp_path):
    name = "example.csv"
    _write_csv(tmp_path / name, [["id", "value"], ["1", "alpha"], []])

    message = re.escape(
        f"CSV field-count mismatch: {name}:3 expected 2 fields, got 0"
    )
    with pytest.raises(AssertionError, match=message):
        _load_rows_function(tmp_path)(name)
