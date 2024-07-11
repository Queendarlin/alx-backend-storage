-- 3-glam_rock.sql

-- This script lists Glam rock bands ranked by their longevity until 2022.
SELECT
    band_name, (IFNULL(split, 2022) - formed) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%';
