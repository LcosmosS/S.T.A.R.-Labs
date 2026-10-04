        sage -python - <<'EOF'
        from src.data.sky_survey_dataset_builder import SkySurveyDatasetBuilder
        builder = SkySurveyDatasetBuilder(downsample=200)
        builder.save("sky_surveys_ci.parquet")
        EOF
