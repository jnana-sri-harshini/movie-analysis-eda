
-- MOVIE INDUSTRY ANALYTICS
-- FILE 1: DATA QUALITY AND OVERVIEW

USE movie_analytics;

-- 1. Check total number of movies
SELECT COUNT(*) AS total_movies
FROM movie;

-- 2. Inspect columns and data types
DESCRIBE movie;

-- 3. Check missing values in important columns
SELECT
    COUNT(*) AS total_rows,
    SUM(movie_title IS NULL OR TRIM(movie_title) = '') AS missing_titles,
    SUM(director_name IS NULL OR TRIM(director_name) = '') AS missing_directors,
    SUM(budget IS NULL) AS missing_budgets,
    SUM(gross IS NULL) AS missing_gross,
    SUM(imdb_score IS NULL) AS missing_ratings,
    SUM(title_year IS NULL) AS missing_years
FROM movie;

-- 4. Check the release year range
SELECT
    MIN(title_year) AS earliest_year,
    MAX(title_year) AS latest_year,
    COUNT(DISTINCT title_year) AS distinct_years
FROM movie;

-- 5. Check duplicate groups using important movie fields
SELECT
    movie_title,
    director_name,
    title_year,
    COUNT(*) AS record_count
FROM movie
GROUP BY
    movie_title,
    director_name,
    title_year
HAVING COUNT(*) > 1
ORDER BY record_count DESC;
