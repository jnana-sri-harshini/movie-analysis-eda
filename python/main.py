
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. PROJECT SETUP
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "movie_metadata.csv"
OUTPUT_DIR = PROJECT_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_FILE}\n"
        "Place movie_metadata.csv in the same folder as main.py."
    )

print("=" * 60)
print("MOVIE INDUSTRY ANALYTICS PROJECT")
print("=" * 60)


# ============================================================
# 2. LOAD THE DATASET
# ============================================================

df = pd.read_csv(DATA_FILE, encoding="latin1")

print("\nSTEP 1: DATASET OVERVIEW")
print("-" * 40)

print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

print("\nFirst five records:")
print(df.head().to_string())

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes.to_string())

print("\nDataset information:")
df.info()


# ============================================================
# 3. CHECK MISSING VALUES
# ============================================================

print("\nSTEP 2: MISSING VALUE ANALYSIS")
print("-" * 40)

missing_report = pd.DataFrame({
    "Missing_Count": df.isna().sum(),
    "Missing_Percentage": (
        df.isna().mean() * 100
    ).round(2)
})

missing_report = missing_report.sort_values(
    by="Missing_Count",
    ascending=False
)

print(missing_report.to_string())

missing_report.to_csv(
    OUTPUT_DIR / "missing_values_report.csv"
)


# ============================================================
# 4. CHECK DUPLICATES
# ============================================================

print("\nSTEP 3: DUPLICATE ANALYSIS")
print("-" * 40)

print("Exact duplicate rows:", df.duplicated().sum())

# Check repeated movie titles without deleting them
if "movie_title" in df.columns:
    title_counts = df["movie_title"].value_counts(
        dropna=True
    )

    repeated_titles = title_counts[title_counts > 1]

    print(
        "Titles appearing more than once:",
        len(repeated_titles)
    )

    print("\nExample repeated titles:")
    print(repeated_titles.head(10).to_string())


# ============================================================
# 5. CLEAN TEXT FORMATTING
# ============================================================

print("\nSTEP 4: CLEANING TEXT FORMATTING")
print("-" * 40)

clean_df = df.copy()

# Clean whitespace in all text columns
text_columns = clean_df.select_dtypes(
    include=["object", "string"]
).columns

for col in text_columns:
    clean_df[col] = (
        clean_df[col]
        .astype("string")
        .str.replace("\u00a0", " ", regex=False)
        .str.strip()
    )

print("Text formatting cleaned.")

# Remove exact duplicate records after text normalization
duplicates_before = clean_df.duplicated().sum()

clean_df = clean_df.drop_duplicates().copy()

print("Exact duplicates removed:", duplicates_before)
print("Rows remaining:", len(clean_df))


# ============================================================
# 6. CONVERT NUMERIC COLUMNS
# ============================================================

print("\nSTEP 5: DATA TYPE VALIDATION")
print("-" * 40)

numeric_columns = [
    "budget",
    "gross",
    "duration",
    "imdb_score",
    "num_voted_users",
    "num_critic_for_reviews",
    "num_user_for_reviews",
    "movie_facebook_likes",
    "director_facebook_likes",
    "actor_1_facebook_likes",
    "actor_2_facebook_likes",
    "actor_3_facebook_likes",
]

for col in numeric_columns:
    if col in clean_df.columns:
        clean_df[col] = pd.to_numeric(
            clean_df[col],
            errors="coerce"
        )

if "title_year" in clean_df.columns:
    clean_df["title_year"] = pd.to_numeric(
        clean_df["title_year"],
        errors="coerce"
    ).astype("Int64")

print(clean_df.dtypes.to_string())


# ============================================================
# 7. CHECK INVALID VALUES
# ============================================================

print("\nSTEP 6: INVALID VALUE CHECKS")
print("-" * 40)

validation_results = {}

if "imdb_score" in clean_df.columns:
    validation_results["Invalid IMDb scores"] = int(
        (
            (clean_df["imdb_score"] < 0)
            | (clean_df["imdb_score"] > 10)
        ).sum()
    )

if "budget" in clean_df.columns:
    validation_results["Negative budgets"] = int(
        (clean_df["budget"] < 0).sum()
    )

if "gross" in clean_df.columns:
    validation_results["Negative gross values"] = int(
        (clean_df["gross"] < 0).sum()
    )

if "duration" in clean_df.columns:
    validation_results["Non-positive durations"] = int(
        (clean_df["duration"] <= 0).sum()
    )

if "title_year" in clean_df.columns:
    validation_results["Missing release years"] = int(
        clean_df["title_year"].isna().sum()
    )

for check, count in validation_results.items():
    print(f"{check}: {count}")

pd.DataFrame(
    list(validation_results.items()),
    columns=["Validation_Check", "Count"]
).to_csv(
    OUTPUT_DIR / "validation_report.csv",
    index=False
)


# ============================================================
# 8. INVESTIGATE EXTREME VALUES
# ============================================================

print("\nSTEP 7: OUTLIER INVESTIGATION")
print("-" * 40)

financial_columns = [
    col for col in ["movie_title", "title_year", "budget", "gross"]
    if col in clean_df.columns
]

if "budget" in clean_df.columns:
    print("\nTop 10 budgets:")
    print(
        clean_df.nlargest(10, "budget")[
            financial_columns
        ].to_string(index=False)
    )

if "gross" in clean_df.columns:
    print("\nTop 10 gross revenue values:")
    print(
        clean_df.nlargest(10, "gross")[
            financial_columns
        ].to_string(index=False)
    )

# Save descriptive statistics for numeric columns
numeric_summary = clean_df.describe(
    include=[np.number]
).T

numeric_summary.to_csv(
    OUTPUT_DIR / "numeric_summary.csv"
)

print("\nNumeric summary:")
print(numeric_summary.to_string())


# ============================================================
# 9. CREATE FINANCIAL ANALYSIS DATASET
# ============================================================

print("\nSTEP 8: FINANCIAL ANALYSIS")
print("-" * 40)

required_financial_columns = {"budget", "gross"}

if required_financial_columns.issubset(clean_df.columns):

    # Keep records with valid, positive budgets and
    # available, non-negative gross revenue.
    financial_df = clean_df[
        clean_df["budget"].notna()
        & clean_df["gross"].notna()
        & (clean_df["budget"] > 0)
        & (clean_df["gross"] >= 0)
    ].copy()

    financial_df["profit"] = (
        financial_df["gross"] - financial_df["budget"]
    )

    financial_df["roi_percent"] = (
        financial_df["profit"]
        / financial_df["budget"]
    ) * 100

    print(
        "Movies available for financial analysis:",
        len(financial_df)
    )

    print("\nHighest gross revenue movies:")
    print(
        financial_df.nlargest(10, "gross")[
            financial_columns
        ].to_string(index=False)
    )

    print("\nHighest ROI movies:")
    print(
        financial_df.nlargest(10, "roi_percent")[
            financial_columns + ["profit", "roi_percent"]
        ].to_string(index=False)
    )

    financial_df.to_csv(
        OUTPUT_DIR / "movie_financial_analysis.csv",
        index=False
    )

else:
    print("Budget or gross column is missing.")
    financial_df = pd.DataFrame()


# ============================================================
# 10. CREATE RELEASE DECADE
# ============================================================

print("\nSTEP 9: FEATURE ENGINEERING")
print("-" * 40)

if "title_year" in clean_df.columns:

    clean_df["decade"] = (
        (clean_df["title_year"] // 10) * 10
    ).astype("Int64")

    print("Release decade column created.")

    print("\nMovies by decade:")
    print(
        clean_df["decade"]
        .value_counts()
        .sort_index()
        .to_string()
    )


# ============================================================
# 11. SAVE CLEANED DATASETS
# ============================================================

print("\nSTEP 10: SAVE OUTPUT FILES")
print("-" * 40)

clean_df.to_csv(
    OUTPUT_DIR / "movie_metadata_cleaned.csv",
    index=False
)

print("Cleaned dataset saved.")
print("Output folder:", OUTPUT_DIR.resolve())


# ============================================================
# 12. CREATE BASIC VISUALIZATIONS
# ============================================================

print("\nSTEP 11: GENERATING VISUALIZATIONS")
print("-" * 40)

sns.set_theme(style="whitegrid")

# Movie production over time
if "title_year" in clean_df.columns:

    yearly_movies = (
        clean_df.dropna(subset=["title_year"])
        .groupby("title_year")
        .size()
    )

    plt.figure(figsize=(12, 6))
    yearly_movies.plot(kind="line")

    plt.title("Number of Movies by Release Year")
    plt.xlabel("Release Year")
    plt.ylabel("Number of Movies")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "movies_by_year.png",
        dpi=150
    )
    plt.close()

# Budget versus gross revenue
if not financial_df.empty:

    # Sample large datasets for a readable scatter plot
    plot_df = financial_df.sample(
        n=min(1500, len(financial_df)),
        random_state=42
    )

    plt.figure(figsize=(10, 6))

    sns.scatterplot(
        data=plot_df,
        x="budget",
        y="gross",
        alpha=0.6
    )

    plt.title("Movie Budget vs Gross Revenue")
    plt.xlabel("Budget")
    plt.ylabel("Gross Revenue")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "budget_vs_gross.png",
        dpi=150
    )
    plt.close()

# IMDb score distribution
if "imdb_score" in clean_df.columns:

    ratings = clean_df["imdb_score"].dropna()

    plt.figure(figsize=(10, 6))

    sns.histplot(
        ratings,
        bins=20,
        kde=True
    )

    plt.title("Distribution of IMDb Ratings")
    plt.xlabel("IMDb Score")
    plt.ylabel("Number of Movies")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "imdb_rating_distribution.png",
        dpi=150
    )
    plt.close()

print("Charts saved to output folder.")


# ============================================================
# 13. PROJECT COMPLETION SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("DATA UNDERSTANDING AND CLEANING COMPLETED")
print("=" * 60)

print("Original rows:", len(df))
print("Cleaned rows:", len(clean_df))
print("Cleaned columns:", len(clean_df.columns))
print("Financial analysis rows:", len(financial_df))

print("\nGenerated files:")
for file in sorted(OUTPUT_DIR.iterdir()):
    print("-", file.name)

print("\nNext stage: SQL business analysis")



# Create a MySQL import-ready CSV
import_df = clean_df.copy()

# Convert missing values to empty CSV fields
import_df = import_df.astype(object).where(
    import_df.notna(), ""
)

import_file = OUTPUT_DIR / "movie_metadata_mysql_import.csv"

import_df.to_csv(
    import_file,
    index=False,
    encoding="utf-8",
    na_rep=""
)

print("MySQL import file created:", import_file)
