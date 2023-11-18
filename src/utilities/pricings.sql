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
    pc.plan_id,
    pr.age,
    pr.premium_single
FROM
    SelectedZip zc
    JOIN airbyte_ideon.plan_counties pc ON zc.county_id = pc.county_id
    AND pc._ab_source_file_url LIKE '%{state}/{year}/{quarter}%'
    JOIN airbyte_ideon.pricings pr ON pc.plan_id = pr.plan_id
    AND zc.rating_area_id = pr.rating_area_id
    AND pr._ab_source_file_url LIKE '%{state}/{year}/{quarter}%'