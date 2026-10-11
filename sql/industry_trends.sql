
-- MOVIE INDUSTRY ANALYTICS
-- FILE 2: INDUSTRY TRENDS

USE movie_analytics;

-- 1. Movie releases and average rating by year
SELECT
    title_year,
    COUNT(*) AS movie_count,
    ROUND(AVG(imdb_score), 2) AS average_rating
FROM movie
WHERE title_year IS NOT NULL
GROUP BY title_year
ORDER BY title_year;

-- 2. Top 10 years by number of movies
SELECT
    title_year,
    COUNT(*) AS movie_count
FROM movie
WHERE title_year IS NOT NULL
GROUP BY title_year
ORDER BY movie_count DESC
LIMIT 10;

-- 3. Top 10 countries by number of movies
SELECT
    country,
    COUNT(*) AS movie_count,
    ROUND(AVG(imdb_score), 2) AS average_rating
FROM movie
WHERE country IS NOT NULL
  AND TRIM(country) <> ''
GROUP BY country
ORDER BY movie_count DESC
LIMIT 10;

-- 4. Movie trends by decade
SELECT
    FLOOR(title_year / 10) * 10 AS release_decade,
    COUNT(*) AS movie_count,
    ROUND(AVG(imdb_score), 2) AS average_rating
FROM movie
WHERE title_year IS NOT NULL
GROUP BY FLOOR(title_year / 10) * 10
ORDER BY release_decade;

-- 5. Most common genre combinations
SELECT
    genres,
    COUNT(*) AS movie_count
FROM movie
WHERE genres IS NOT NULL
  AND TRIM(genres) <> ''
GROUP BY genres
ORDER BY movie_count DESC
LIMIT 15;

-- 6. Average rating by genre combination
SELECT
    genres,
    COUNT(*) AS movie_count,
    ROUND(AVG(imdb_score), 2) AS average_rating
FROM movie
WHERE genres IS NOT NULL
  AND TRIM(genres) <> ''
  AND imdb_score IS NOT NULL
GROUP BY genres
HAVING COUNT(*) >= 10
ORDER BY average_rating DESC
LIMIT 15;
