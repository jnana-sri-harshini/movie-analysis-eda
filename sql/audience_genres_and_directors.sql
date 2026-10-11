
-- MOVIE INDUSTRY ANALYTICS
-- FILE 4: AUDIENCE, GENRES AND DIRECTORS

USE movie_analytics;

-- 1. Audience vote groups and average ratings
SELECT
    CASE
        WHEN num_voted_users < 10000 THEN 'Low Votes'
        WHEN num_voted_users < 100000 THEN 'Medium Votes'
        ELSE 'High Votes'
    END AS vote_category,
    COUNT(*) AS movie_count,
    ROUND(AVG(imdb_score), 2) AS average_rating,
    ROUND(AVG(gross), 2) AS average_gross
FROM movie
WHERE num_voted_users IS NOT NULL
  AND num_voted_users >= 0
GROUP BY
    CASE
        WHEN num_voted_users < 10000 THEN 'Low Votes'
        WHEN num_voted_users < 100000 THEN 'Medium Votes'
        ELSE 'High Votes'
    END
ORDER BY average_rating DESC;

-- 2. Directors with at least five rated movies
SELECT
    director_name,
    COUNT(*) AS movie_count,
    ROUND(AVG(imdb_score), 2) AS average_rating,
    ROUND(AVG(gross), 2) AS average_gross
FROM movie
WHERE director_name IS NOT NULL
  AND TRIM(director_name) <> ''
  AND imdb_score IS NOT NULL
GROUP BY director_name
HAVING COUNT(*) >= 5
ORDER BY average_rating DESC
LIMIT 15;

-- 3. Compare critic-review groups
SELECT
    CASE
        WHEN num_critic_for_reviews < 50
            THEN 'Fewer than 50 critic reviews'
        WHEN num_critic_for_reviews < 200
            THEN '50-199 critic reviews'
        ELSE '200+ critic reviews'
    END AS critic_review_group,
    COUNT(*) AS movie_count,
    ROUND(AVG(imdb_score), 2) AS average_rating,
    ROUND(AVG(gross), 2) AS average_gross
FROM movie
WHERE num_critic_for_reviews IS NOT NULL
  AND num_critic_for_reviews >= 0
GROUP BY
    CASE
        WHEN num_critic_for_reviews < 50
            THEN 'Fewer than 50 critic reviews'
        WHEN num_critic_for_reviews < 200
            THEN '50-199 critic reviews'
        ELSE '200+ critic reviews'
    END
ORDER BY average_rating DESC;

-- 4. Top 20 movies by audience votes
SELECT
    movie_title,
    title_year,
    imdb_score,
    num_voted_users,
    movie_facebook_likes,
    gross
FROM movie
WHERE num_voted_users IS NOT NULL
ORDER BY num_voted_users DESC
LIMIT 20;

-- 5. Compare Facebook likes and ratings by engagement group
SELECT
    CASE
        WHEN movie_facebook_likes < 1000 THEN 'Low Likes'
        WHEN movie_facebook_likes < 10000 THEN 'Medium Likes'
        ELSE 'High Likes'
    END AS engagement_category,
    COUNT(*) AS movie_count,
    ROUND(AVG(imdb_score), 2) AS average_rating,
    ROUND(AVG(gross), 2) AS average_gross
FROM movie
WHERE movie_facebook_likes IS NOT NULL
  AND movie_facebook_likes >= 0
GROUP BY
    CASE
        WHEN movie_facebook_likes < 1000 THEN 'Low Likes'
        WHEN movie_facebook_likes < 10000 THEN 'Medium Likes'
        ELSE 'High Likes'
    END
ORDER BY average_rating DESC;
