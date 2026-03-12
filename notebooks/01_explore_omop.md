# Notebook: Explore OMOP Data

Place Jupyter notebooks here for exploratory analysis.

Example notebooks to add:

- `01_explore_omop.ipynb` — Load OMOP Parquet, basic demographics
- `02_variant_analysis.ipynb` — Variant distribution, gene burden
- `03_rag_retrieval.ipynb` — Test RAG retrieval over guidelines

## Sample Code (Python)

```python
import pyarrow.parquet as pq

person = pq.read_table("data/omop/person.parquet")
print(person.to_pandas().head())
```
