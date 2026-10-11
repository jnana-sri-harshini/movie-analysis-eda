
-- MOVIE INDUSTRY ANALYTICS
-- FILE 3: FINANCIAL PERFORMANCE

USE movie_analytics;

-- 1. Top 10 movies by gross revenue
SELECT
    movie_title,
    title_year,
    budget,
    gross,
    imdb_score
FROM movie
WHERE gross IS NOT NULL
ORDER BY gross DESC
LIMIT 10;

-- 2. Compare financial performance by budget category
SELECT
    CASE
        WHEN budget < 10000000 THEN 'Low Budget'
        WHEN budget < 50000000 THEN 'Medium Budget'
        ELSE 'High Budget'
    END AS budget_category,
    COUNT(*) AS movie_count,
    ROUND(AVG(budget), 2) AS average_budget,
    ROUND(AVG(gross), 2) AS average_gross,
    ROUND(AVG(imdb_score), 2) AS average_rating
FROM movie
WHERE budget > 0
  AND gross IS NOT NULL
GROUP BY
    CASE
        WHEN budget < 10000000 THEN 'Low Budget'
        WHEN budget < 50000000 THEN 'Medium Budget'
        ELSE 'High Budget'
    END
ORDER BY average_gross DESC;

-- 3. Top 10 movies by simplified ROI
SELECT
    movie_title,
    title_year,
    budget,
    gross,
    ROUND(
        ((gross - budget) / budget) * 100,
        2
    ) AS roi_percent
FROM movie
WHERE budget > 0
  AND gross IS NOT NULL
  AND gross >= 0
ORDER BY roi_percent DESC
LIMIT 10;

-- 4. Compare revenue and ratings by genre combination
SELECT
    genres,
    COUNT(*) AS movie_count,
    ROUND(AVG(gross), 2) AS average_gross,
    ROUND(AVG(imdb_score), 2) AS average_rating,
    SUM(gross) AS total_gross
FROM movie
WHERE genres IS NOT NULL
  AND TRIM(genres) <> ''
  AND gross IS NOT NULL
GROUP BY genres
HAVING COUNT(*) >= 10
ORDER BY average_gross DESC
LIMIT 15;

-- 5. Count movies by financial and audience success category
-- Thresholds are illustrative, not universal industry standards.
SELECT
    CASE
        WHEN gross > budget * 1.5 AND imdb_score >= 7
            THEN 'Commercial and Audience Success'
        WHEN gross > budget * 1.5
            THEN 'Commercial Success'
        WHEN imdb_score >= 7
            THEN 'Audience Success'
        ELSE 'Neither Threshold Met'
    END AS success_category,
    COUNT(*) AS movie_count
FROM movie
WHERE budget > 0
  AND gross IS NOT NULL
  AND gross >= 0
  AND imdb_score IS NOT NULL
GROUP BY
    CASE
        WHEN gross > budget * 1.5 AND imdb_score >= 7
            THEN 'Commercial and Audience Success'
        WHEN gross > budget * 1.5
            THEN 'Commercial Success'
        WHEN imdb_score >= 7
            THEN 'Audience Success'
        ELSE 'Neither Threshold Met'
    END
ORDER BY movie_count DESC;
