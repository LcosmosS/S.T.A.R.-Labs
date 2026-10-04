def constraints_to_latex(constraints_dict, caption="Parameter constraints", label="tab:constraints"):
    """
    Convert a constraints dict into a LaTeX table.
    """
    lines = [
        "\\begin{table}[h!]",
        "\\centering",
        "\\begin{tabular}{lc}",
        "\\hline",
        "Parameter & Value \\\\",
        "\\hline"
    ]

    for key, value in constraints_dict.items():
        lines.append(f"{key} & {value:.4f} \\\\")

    lines += [
        "\\hline",
        "\\end{tabular}",
        f"\\caption{{{caption}}}",
        f"\\label{{{label}}}",
        "\\end{table}"
    ]

    return "\n".join(lines)
