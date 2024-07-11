-- 3-glam_rock.sql

-- This script lists Glam rock bands ranked by their longevity until 2022.
SELECT
    band_name,
    FLOOR((2022 - formed) / 1) AS lifespan
FROM
    metal_bands
WHERE
    style = 'Glam rock'
ORDER BY
    lifespan DESC;
