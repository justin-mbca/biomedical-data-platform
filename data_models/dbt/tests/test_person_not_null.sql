-- dbt test: person_id should not be null
select * from {{ ref('stg_person') }} where person_id is null
