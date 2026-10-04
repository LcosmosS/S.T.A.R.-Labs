# 5. Generate paper figures for both runs

fig_pipeline_2015 = PaperFiguresPipeline(
    chain_2015,
    param_names,
    H_expr,
    data_paths={
        "planck": PLANCK_2015,
        "bao": DESI_BAO_DR1,
        "cc": COSMIC_CHRONOMETERS,
        "sn": PANTHEON_PLUS_FULL
    }
)

constraints_2015 = fig_pipeline_2015.run("paper_figures_planck2015")


fig_pipeline_2018 = PaperFiguresPipeline(
    chain_2018,
    param_names,
    H_expr,
    data_paths={
        "planck": PLANCK_2018_RECON,
        "bao": DESI_BAO_DR1,
        "cc": COSMIC_CHRONOMETERS,
        "sn": PANTHEON_PLUS_FULL
    }
)

constraints_2018 = fig_pipeline_2018.run("paper_figures_planck2018")

constraints_2015, constraints_2018

