WITH SelectedZip AS (
    SELECT
        *
    FROM
        airbyte_ideon.zip_counties
    WHERE
        zip_code_id = '{zip_code}'
        AND _ab_source_file_url LIKE '%{state}/{year}/{quarter}%'
)
SELECT
    p.*
FROM
    SelectedZip zc
    JOIN airbyte_ideon.plan_counties pc ON zc.county_id = pc.county_id
    AND pc._ab_source_file_url LIKE '%{state}/{year}/{quarter}%'
    JOIN airbyte_ideon.plans p ON pc.plan_id = p.id
    AND p._ab_source_file_url LIKE '%{state}/{year}/{quarter}%';