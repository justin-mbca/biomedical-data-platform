# Great Expectations — Data Quality

## Expectation Suites

| Suite | Purpose |
|-------|---------|
| `person_suite` | Basic OMOP person validation |
| `schema_drift_suite` | Schema drift detection |
| `null_rate_suite` | Null rate and format validation |
| `data_freshness_suite` | Data freshness and temporal checks |

## Usage

```bash
# Run validation (from project root)
python data_quality/run_validation.py --data data/omop/person.parquet --suite person_suite
```

## Example Checks

- **Schema drift**: `expect_table_columns_to_match_ordered_list`
- **Null rate**: `expect_column_values_to_not_be_null`
- **Data freshness**: `expect_column_values_to_be_dateutil_parseable`, temporal range checks
