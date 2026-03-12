-- stg_person: Standardized person from raw OMOP
{{
  config(
    materialized='view',
    unique_key='person_id',
  )
}}

with source as (
  select * from {{ source('omop_raw', 'person') }}
),
standardized as (
  select
    person_id, gender_concept_id, year_of_birth,
    race_concept_id, ethnicity_concept_id,
    person_source_value, gender_source_value,
    current_timestamp as _loaded_at
  from source
  where person_id is not null
)
select * from standardized
