
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "output" / "movie_metadata_cleaned.csv"
OUTPUT_DIR = PROJECT_DIR / "eda_output"

OUTPUT_DIR.mkdir(exist_ok=True)

# Load cleaned dataset
df = pd.read_csv(DATA_FILE, encoding="utf-8")

# Convert important columns to numeric safely
numeric_columns = [
    "title_year", "budget", "gross", "duration",
    "imdb_score", "num_voted_users",
    "num_critic_for_reviews", "num_user_for_reviews",
    "movie_facebook_likes"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

print("=" * 55)
print("MOVIE INDUSTRY ANALYTICS - PYTHON EDA")
print("=" * 55)

print("\nDataset shape:", df.shape)

print("\nFirst five rows:")
print(df.head().to_string())

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes.to_string())

print("\nStatistical summary:")
print(df.describe().to_string())

print("\nEDA setup completed.")


# STEP 3: DATA QUALITY ANALYSIS

missing_report = pd.DataFrame({
    "missing_count": df.isna().sum(),
    "missing_percentage": (df.isna().mean() * 100).round(2)
}).sort_values("missing_count", ascending=False)

print("\nMissing value report:")
print(missing_report.to_string())

missing_report.to_csv(
    OUTPUT_DIR / "missing_values_eda.csv"
)

# Visualize missing values
missing_to_plot = missing_report[
    missing_report["missing_count"] > 0
].head(15).sort_values("missing_percentage")

if not missing_to_plot.empty:
    plt.figure(figsize=(10, 7))
    plt.barh(
        missing_to_plot.index,
        missing_to_plot["missing_percentage"]
    )
    plt.xlabel("Missing values (%)")
    plt.title("Top 15 Columns by Missing Value Percentage")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "missing_values.png", dpi=150)
    plt.show()
    plt.close()

# Check invalid ratings and negative financial values
print("\nInvalid IMDb ratings:",
      ((df["imdb_score"] < 0) | (df["imdb_score"] > 10)).sum())

print("Negative budgets:", (df["budget"] < 0).sum())
print("Negative gross values:", (df["gross"] < 0).sum())

print("\nData quality analysis completed.")



# STEP 4: INDUSTRY TRENDS

yearly = (
    df.dropna(subset=["title_year"])
    .groupby("title_year")
    .agg(
        movie_count=("movie_title", "count"),
        average_rating=("imdb_score", "mean")
    )
    .reset_index()
)

yearly["average_rating"] = yearly["average_rating"].round(2)

print("\nMovie releases by year:")
print(yearly.tail(15).to_string(index=False))

yearly.to_csv(OUTPUT_DIR / "yearly_trends.csv", index=False)

# Movies released each year
plt.figure(figsize=(12, 6))
plt.plot(
    yearly["title_year"],
    yearly["movie_count"],
    marker="o",
    markersize=3
)
plt.title("Number of Movies by Release Year")
plt.xlabel("Release Year")
plt.ylabel("Number of Movies")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "movies_by_year.png", dpi=150)
plt.show()
plt.close()

# Average IMDb rating by year
plt.figure(figsize=(12, 6))
plt.plot(
    yearly["title_year"],
    yearly["average_rating"],
    marker="o",
    markersize=3
)
plt.title("Average IMDb Rating by Release Year")
plt.xlabel("Release Year")
plt.ylabel("Average IMDb Rating")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "ratings_by_year.png", dpi=150)
plt.show()
plt.close()


# STEP 5: FINANCIAL ANALYSIS

financial = df[
    df["budget"].notna()
    & df["gross"].notna()
    & (df["budget"] > 0)
    & (df["gross"] >= 0)
].copy()

financial["profit_before_other_costs"] = (
    financial["gross"] - financial["budget"]
)

financial["roi_percent"] = (
    financial["profit_before_other_costs"]
    / financial["budget"]
) * 100

print("\nFinancial records available:", len(financial))

print("\nFinancial summary:")
print(
    financial[
        ["budget", "gross", "profit_before_other_costs", "roi_percent"]
    ].describe().round(2).to_string()
)

financial.to_csv(
    OUTPUT_DIR / "financial_analysis_eda.csv",
    index=False
)

# Budget vs gross revenue
plot_financial = financial[
    (financial["budget"] > 0) & (financial["gross"] > 0)
].copy()

plt.figure(figsize=(10, 6))
plt.scatter(
    plot_financial["budget"],
    plot_financial["gross"],
    alpha=0.5
)
plt.xscale("log")
plt.yscale("log")
plt.title("Movie Budget vs Gross Revenue")
plt.xlabel("Budget (log scale)")
plt.ylabel("Gross Revenue (log scale)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "budget_vs_gross.png", dpi=150)
plt.show()
plt.close()

# Correlation between budget and gross
correlation = financial[["budget", "gross"]].corr().iloc[0, 1]

print("\nBudget-gross Pearson correlation:", round(correlation, 3))

# Top movies by simplified ROI
print("\nTop 10 movies by simplified ROI:")
print(
    financial.nlargest(10, "roi_percent")[
        ["movie_title", "title_year", "budget", "gross", "roi_percent"]
    ].to_string(index=False)
)


# STEP 6: INDIVIDUAL GENRE ANALYSIS

genre_df = df[
    df["genres"].notna()
    & (df["genres"].str.strip() != "")
].copy()

genre_df["genre"] = genre_df["genres"].str.split("|")

genre_df = genre_df.explode("genre")

genre_df["genre"] = genre_df["genre"].str.strip()

genre_df = genre_df[genre_df["genre"] != ""]

genre_summary = (
    genre_df.groupby("genre")
    .agg(
        movie_count=("movie_title", "count"),
        average_rating=("imdb_score", "mean"),
        average_gross=("gross", "mean"),
        total_gross=("gross", "sum")
    )
    .reset_index()
)

genre_summary["average_rating"] = (
    genre_summary["average_rating"].round(2)
)

genre_summary["average_gross"] = (
    genre_summary["average_gross"].round(2)
)

genre_summary["total_gross"] = (
    genre_summary["total_gross"].round(2)
)

genre_summary.to_csv(
    OUTPUT_DIR / "genre_analysis.csv",
    index=False
)

# Require at least 20 movies for the comparison
popular_genres = genre_summary[
    genre_summary["movie_count"] >= 20
].copy()

print("\nGenre performance:")
print(
    popular_genres.sort_values(
        "average_rating", ascending=False
    ).to_string(index=False)
)

# Highest-rated genres
top_rated = popular_genres.sort_values(
    "average_rating", ascending=False
).head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_rated["genre"], top_rated["average_rating"])
plt.gca().invert_yaxis()
plt.title("Top Genres by Average IMDb Rating")
plt.xlabel("Average IMDb Rating")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "genre_ratings.png", dpi=150)
plt.show()
plt.close()

# Highest average gross by genre
top_gross = popular_genres.sort_values(
    "average_gross", ascending=False
).head(10)

plt.figure(figsize=(10, 6))
plt.barh(top_gross["genre"], top_gross["average_gross"])
plt.gca().invert_yaxis()
plt.title("Top Genres by Average Gross Revenue")
plt.xlabel("Average Gross Revenue")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "genre_revenue.png", dpi=150)
plt.show()
plt.close()



# STEP 7: AUDIENCE ENGAGEMENT

engagement_columns = [
    "imdb_score",
    "num_voted_users",
    "movie_facebook_likes",
    "num_critic_for_reviews",
    "num_user_for_reviews",
    "gross"
]

engagement_columns = [
    col for col in engagement_columns if col in df.columns
]

correlations = df[engagement_columns].corr(
    method="pearson"
)

print("\nAudience engagement correlation matrix:")
print(correlations.round(3).to_string())

correlations.to_csv(
    OUTPUT_DIR / "engagement_correlations.csv"
)

plt.figure(figsize=(10, 7))
sns.heatmap(
    correlations,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0
)
plt.title("Movie Ratings, Engagement and Revenue Correlations")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "engagement_correlation_heatmap.png", dpi=150)
plt.show()
plt.close()

# IMDb rating vs audience votes
plot_df = df[
    df["imdb_score"].notna()
    & df["num_voted_users"].notna()
    & (df["num_voted_users"] > 0)
].copy()

plt.figure(figsize=(10, 6))
plt.scatter(
    plot_df["num_voted_users"],
    plot_df["imdb_score"],
    alpha=0.4
)
plt.xscale("log")
plt.title("IMDb Rating vs Number of Votes")
plt.xlabel("Number of Votes (log scale)")
plt.ylabel("IMDb Rating")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "ratings_vs_votes.png", dpi=150)
plt.show()
plt.close()



# STEP 8: DIRECTOR ANALYSIS

director_df = df[
    df["director_name"].notna()
    & (df["director_name"].str.strip() != "")
    & df["imdb_score"].notna()
].copy()

director_summary = (
    director_df.groupby("director_name")
    .agg(
        movie_count=("movie_title", "count"),
        average_rating=("imdb_score", "mean"),
        average_gross=("gross", "mean"),
        total_gross=("gross", "sum")
    )
    .reset_index()
)

director_summary = director_summary[
    director_summary["movie_count"] >= 5
].copy()

director_summary["average_rating"] = (
    director_summary["average_rating"].round(2)
)

director_summary.to_csv(
    OUTPUT_DIR / "director_analysis.csv",
    index=False
)

top_directors = director_summary.sort_values(
    "average_rating", ascending=False
).head(15)

print("\nTop directors by average IMDb rating:")
print(top_directors.to_string(index=False))

plt.figure(figsize=(10, 7))
plt.barh(
    top_directors["director_name"],
    top_directors["average_rating"]
)
plt.gca().invert_yaxis()
plt.title("Directors with Highest Average IMDb Ratings")
plt.xlabel("Average IMDb Rating")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "director_ratings.png", dpi=150)
plt.show()
plt.close()


# STEP 9: DECADE ANALYSIS

decade_df = df.dropna(subset=["title_year"]).copy()

decade_df["decade"] = (
    decade_df["title_year"] // 10 * 10
).astype(int)

decade_summary = (
    decade_df.groupby("decade")
    .agg(
        movie_count=("movie_title", "count"),
        average_rating=("imdb_score", "mean"),
        average_budget=("budget", "mean"),
        average_gross=("gross", "mean")
    )
    .reset_index()
)

decade_summary = decade_summary.round(2)

print("\nMovie performance by decade:")
print(decade_summary.to_string(index=False))

decade_summary.to_csv(
    OUTPUT_DIR / "decade_analysis.csv",
    index=False
)

plt.figure(figsize=(10, 6))
plt.bar(
    decade_summary["decade"].astype(str),
    decade_summary["movie_count"]
)
plt.title("Number of Movies by Decade")
plt.xlabel("Decade")
plt.ylabel("Movie Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "movies_by_decade.png", dpi=150)
plt.show()
plt.close()



# STEP 10: SAVE A SUMMARY

summary = {
    "total_movie_records": len(df),
    "missing_budget_records": int(df["budget"].isna().sum()),
    "missing_gross_records": int(df["gross"].isna().sum()),
    "missing_rating_records": int(df["imdb_score"].isna().sum()),
    "financial_analysis_records": len(financial),
    "individual_genres_found": int(genre_summary["genre"].nunique()),
    "directors_with_at_least_5_rated_movies": len(director_summary),
    "budget_gross_correlation": round(
        financial[["budget", "gross"]].corr().iloc[0, 1], 3
    ) if len(financial) > 1 else None
}

summary_df = pd.DataFrame(
    list(summary.items()),
    columns=["metric", "value"]
)

summary_df.to_csv(
    OUTPUT_DIR / "eda_summary.csv",
    index=False
)

print("\n" + "=" * 55)
print("PYTHON EDA COMPLETED")
print("=" * 55)
print(summary_df.to_string(index=False))
print("\nCharts and reports saved in:")
print(OUTPUT_DIR.resolve())
