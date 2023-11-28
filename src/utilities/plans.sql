SELECT
    plans.*
FROM
    airbyte_ideon.plans as plans
    LEFT JOIN airbyte_ideon.plan_counties as plan_counties ON plans.id = plan_counties.plan_id
    LEFT JOIN airbyte_ideon.service_area_zip_counties as sazc ON sazc.county_id = plan_counties.county_id
WHERE
    plans.service_area_id = sazc.service_area_id
    AND sazc.zip_code_id = '{zip_code}'
    AND plan_counties._ab_source_file_url LIKE '%{state}/{year}/{quarter}%'
    AND sazc._ab_source_file_url LIKE '%{state}/{year}/{quarter}%'
    AND plans._ab_source_file_url LIKE '%{state}/{year}/{quarter}%'
ORDER BY
    plans.display_name ASC;