import sys

PYTHON = sys.executable


rule all:
    input:
        "data/processed/cleaned_samples.csv",
        "data/processed/feature_table.tsv",
        "data/processed/site_stage_counts.tsv",
        "results/summary_metrics.tsv",
        "results/summary_figure.png",
        "results/report.md"


rule clean_samples:
    input:
        raw="data/raw/messy_samples.csv",
        script="scripts/clean_samples.py"
    output:
        "data/processed/cleaned_samples.csv"
    log:
        "logs/clean_samples.log"
    shell:
        """
        {PYTHON:q} {input.script:q} \
            --input {input.raw:q} \
            --output {output:q} \
            > {log:q} 2>&1
        """

rule query_patient_features:
    input:
        database="data/raw/cohort.db",
        script="scripts/build_feature_table.py",
        gene_sql="scripts/query1_gene_counts.sql",
        site_sql="scripts/query2_site_stage_counts.sql"
    output:
        features="data/processed/feature_table.tsv",
        site_stage="data/processed/site_stage_counts.tsv"
    params:
        output_dir="data/processed"
    log:
        "logs/query_patient_features.log"
    shell:
        """
        {PYTHON:q} {input.script:q} \
            --db {input.database:q} \
            --output-dir {params.output_dir:q} \
            > {log:q} 2>&1
        """

rule create_summary:
    input:
        samples="data/processed/cleaned_samples.csv",
        features="data/processed/feature_table.tsv",
        script="scripts/create_summary.py"
    output:
        metrics="results/summary_metrics.tsv",
        figure="results/summary_figure.png"
    log:
        "logs/create_summary.log"
    shell:
        """
        {PYTHON:q} {input.script:q} \
            --samples {input.samples:q} \
            --features {input.features:q} \
            --metrics {output.metrics:q} \
            --figure {output.figure:q} \
            > {log:q} 2>&1
        """

rule render_report:
    input:
        metrics="results/summary_metrics.tsv",
        figure="results/summary_figure.png",
        script="scripts/render_report.py"
    output:
        "results/report.md"
    log:
        "logs/render_report.log"
    shell:
        """
        {PYTHON:q} {input.script:q} \
            --metrics {input.metrics:q} \
            --figure {input.figure:q} \
            --output {output:q} \
            > {log:q} 2>&1
        """

