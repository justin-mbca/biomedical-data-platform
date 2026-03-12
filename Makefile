# Biomedical Data Platform — Convenience targets
.PHONY: deps data fhir genomics rag rna-seq dashboard test lint

deps:
	pip install -r requirements.txt

data:
	python scripts/generate_rna_seq_sample.py
	python scripts/generate_synthetic_oncology.py

fhir:
	python -m pipelines.fhir_ingestion.run --config config/fhir_demo.yaml

genomics:
	@echo "Run: python -m pipelines.genomics.variant_pipeline --input <vcf>"

rag:
	python -m pipelines.rag.build_index --sources docs/guidelines/

rna-seq:
	cd workflows/snakemake && snakemake -j 2

dashboard:
	streamlit run apps/analytics_dashboard/app.py

test:
	pytest tests/ -v

lint:
	ruff check src pipelines apps
	black --check src pipelines apps
