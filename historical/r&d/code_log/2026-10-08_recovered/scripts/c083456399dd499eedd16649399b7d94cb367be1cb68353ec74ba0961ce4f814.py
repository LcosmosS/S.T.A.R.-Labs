"""
LaTeX constraints table generator
"""


def constraints_to_latex(
    constraints_dict, caption="Cosmological Constraints", label="tab:constraints"
):
    """Convert constraints dictionary to LaTeX table with safe formatting"""
    lines = [
        "\\begin{table}[h!]",
        "\\centering",
        f"\\caption{{{caption}}}",
        f"\\label{{{label}}}",
        "\\begin{tabular}{lc}",
        "\\hline",
        "Parameter & Value \\\\",
        "\\hline",
    ]

    for key, value in constraints_dict.items():
        # Handle different value types safely
        if isinstance(value, (int, float)):
            val_str = f"{value:.4f}"
        elif isinstance(value, str):
            val_str = value
        elif isinstance(value, (list, tuple)) and len(value) >= 1:
            val_str = (
                f"{value[0]:.4f}"
                if isinstance(value[0], (int, float))
                else str(value[0])
            )
        else:
            val_str = str(value)

        lines.append(f"{key} & {val_str} \\\\")

    lines += ["\\hline", "\\end{tabular}", "\\end{table}"]

    return "\n".join(lines)
