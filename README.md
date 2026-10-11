# Movies Analytics | Python & SQL

An end-to-end data analytics project using Python and MySQL to explore movie industry trends, financial performance, audience ratings, genres, and director performance.

## Project Overview

This project analyzes movie metadata to understand patterns in movie production, audience ratings, box-office gross, budget, and financial performance.

Python was used for data cleaning, exploratory data analysis (EDA), financial calculations, and visualizations. MySQL was used to perform structured data analysis through aggregations, filtering, common table expressions (CTEs), and window functions.

The goal is to extract meaningful insights from movie industry data while demonstrating practical Python and SQL skills for data analytics.

## Tools Used

- **Python** - Data cleaning, exploratory data analysis, and financial calculations
- **Pandas** - Data manipulation, missing-value analysis, grouping, and aggregation
- **NumPy** - Numerical analysis
- **Matplotlib & Seaborn** - Data visualization
- **MySQL** - Data querying and analytical investigations
- **SQL** - Aggregations, CTEs, window functions, ranking, and conditional logic
- **Git & GitHub** - Version control and project documentation

## Project Workflow

1. **Data Understanding** - Examined the movie dataset, its columns, and data quality.
2. **Data Cleaning** - Handled missing values, standardized text fields, removed exact duplicates, and converted columns to appropriate data types.
3. **Exploratory Data Analysis** - Investigated movie ratings, release years, genres, audience engagement, and financial variables using Python.
4. **SQL Analysis** - Used MySQL to analyze industry trends, compare budget categories, evaluate financial performance, and examine audience and director metrics.
5. **Financial Analysis** - Calculated simplified profit and return on investment (ROI) for movies with valid financial records.
6. **Insights & Documentation** - Organized analysis outputs and documented the methodology, findings, and limitations.

## Key Analysis Areas

### 1. Data Quality and Overview
- Examined dataset size and column structure.
- Investigated missing values and duplicate records.
- Checked financial data for invalid budgets and revenue values.
- Reviewed the range of release years and IMDb ratings.

### 2. Movie Industry Trends
- Analyzed movie counts and average ratings by release year.
- Compared movie production across countries.
- Examined common genre combinations.
- Compared average IMDb ratings across genre combinations.

### 3. Financial Performance
- Identified movies with high recorded box-office gross.
- Compared average budget, gross, and IMDb rating across budget categories.
- Calculated simplified profit and ROI.
- Ranked movies by ROI using SQL window functions.
- Classified movies using defined commercial and audience-success thresholds.

### 4. Audience and Director Analysis
- Examined audience engagement using vote counts and review metrics.
- Compared ratings across movies and directors.
- Investigated movie popularity using available Facebook-like metrics.
- Explored relationships between audience engagement and IMDb ratings.

## Selected Findings

The following are preliminary findings from the SQL analysis:

- **Financial subset:** 1,419 records met the criteria of a positive budget and nonnegative gross, with both values present.
- **Average IMDb rating:** The financially eligible subset had an average IMDb rating of 6.42 out of 10.
- **Budget comparison:** The low-budget category had the highest average IMDb rating in the initial comparison (6.85), but contained only 10 movies.
- **ROI ranking:** The initial ROI query ranked *Pinocchio* (1940) first, followed by *A Nightmare on Elm Street* (1984) and *The Karate Kid* (1984).

These results are based on the dataset's recorded values and the definitions used in the queries. Financial records, historical budgets, and ROI outliers should be validated before drawing strong conclusions.


## SQL Techniques

The project demonstrates several SQL techniques used in analytical workflows.

### 1. Common Table Expressions (CTEs)

Used to organize financial calculations into readable query stages.

```sql
WITH financial_movies AS (
    SELECT
        movie_title,
        title_year,
        budget,
        gross,
        gross - budget AS profit
    FROM movie
    WHERE budget > 0
      AND gross IS NOT NULL
)
SELECT *
FROM financial_movies
ORDER BY profit DESC;
```

### 2. Window Functions and Ranking

Used to rank movies by calculated ROI.

```sql
WITH financial_movies AS (
    SELECT
        movie_title,
        title_year,
        budget,
        gross,
        ROUND(
            (gross - budget) / budget * 100,
            2
        ) AS roi_percent
    FROM movie
    WHERE budget > 0
      AND gross IS NOT NULL
),
ranked_movies AS (
    SELECT
        *,
        RANK() OVER (
            ORDER BY roi_percent DESC
        ) AS roi_rank
    FROM financial_movies
)
SELECT *
FROM ranked_movies
WHERE roi_rank <= 10
ORDER BY roi_rank;
```

### 3. Aggregation and Conditional Logic

Used to compare financial metrics across budget categories and classify movies according to defined success thresholds.

The repository contains the complete SQL scripts used for data quality checks, industry trends, financial performance, and audience and director analysis.


## How to Run This Project

### Prerequisites

- Python 3
- MySQL Server and MySQL Workbench
- Required Python libraries listed in `requirements.txt`

### 1. Install Python Dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Prepare the Dataset

Obtain the original movie metadata dataset and place it in the expected project location. Refer to `data/README.md` for dataset details and file paths.

### 3. Run Data Cleaning and EDA

Run the Python cleaning script followed by the EDA script. Review the generated cleaned dataset, summary tables, and charts.

### 4. Load the Dataset into MySQL

Import the cleaned CSV into a MySQL table named `movie` in the `movie_analytics` database. Confirm the column names and data types match the SQL scripts.

### 5. Execute the SQL Analysis

Run the SQL files in MySQL Workbench and examine the result grids to reproduce the data quality, industry trend, financial, audience, and director analyses.

## Skills Demonstrated

- Python programming for data analysis
- Pandas and NumPy
- Data cleaning and preprocessing
- Exploratory data analysis (EDA)
- Data visualization
- MySQL and analytical SQL
- Aggregations, CTEs, and window functions
- Financial metric calculations
- Data quality validation
- Analytical reasoning and documentation

## Conclusion

This project demonstrates a reproducible data analytics workflow combining Python and SQL to investigate movie industry trends, financial performance, audience ratings, and director metrics.

It emphasizes data preparation, analytical querying, financial metric calculation, and evidence-based interpretation while recognizing the limitations of incomplete or inconsistent financial metadata.

## Author

**MJS Harshini**

harshinimogadala@gmail.com

Aspiring Data Analyst | Python | SQL | Data Analytics

[GitHub Profile](https://github.com/jana-sri-harshini)
