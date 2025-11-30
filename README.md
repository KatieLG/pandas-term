# pandas-cli

A CLI for applying common pandas functions to data files in the terminal.

## Installation

```bash
uv sync
```

## Command Reference

| CLI Command       | Pandas Function          | Description                    |
| ----------------- | ------------------------ | ------------------------------ |
| `pd select`       | `df[columns]`            | Select specific columns        |
| `pd drop`         | `df.drop()`              | Drop columns                   |
| `pd sort`         | `df.sort_values()`       | Sort by columns                |
| `pd dedup`        | `df.drop_duplicates()`   | Remove duplicate rows          |
| `pd reset-index`  | `df.reset_index()`       | Reset the dataframe index      |
| `pd merge`        | `pd.merge()`             | Merge two dataframes           |
| `pd batch`        | `df.iloc[]`              | Split dataframe into batches   |
| `pd query`        | `df.query()`             | Filter using query expressions |
| `pd head`         | `df.head()`              | Get first n rows               |
| `pd tail`         | `df.tail()`              | Get last n rows                |
| `pd sample`       | `df.sample()`            | Random sample of rows          |
| `pd dropna`       | `df.dropna()`            | Drop rows with null values     |
| `pd describe`     | `df.describe()`          | Descriptive statistics         |
| `pd info`         | `df.info()`              | DataFrame information          |
| `pd value-counts` | `df[col].value_counts()` | Count unique values            |
| `pd groupby`      | `df.groupby().agg()`     | Group by and aggregate         |
| `pd unique`       | `df[col].unique()`       | Unique values in column        |

## Usage

All commands accept an input file path (or `-` for stdin) and an optional `-o/--output` flag for the output file (or `-` for stdout).

### Transform commands

```bash
# Select specific columns
pd select data.csv name age

# Drop columns
pd drop data.csv unwanted_column

# Sort by columns
pd sort data.csv age --ascending
pd sort data.csv age name --descending

# Remove duplicate rows
pd dedup data.csv
pd dedup data.csv --subset name email

# Reset the dataframe index
pd reset-index data.csv

# Merge two dataframes
pd merge left.csv right.csv --on user_id --how inner
pd merge left.csv right.csv --left-on id --right-on user_id --how left

# Split dataframe into batches
pd batch data.csv 100 -o "output_batch_{}.csv"
```

### Filter commands

```bash
# Filter using pandas query expressions
pd query data.csv "age > 30 and city == 'NYC'"

# First N rows
pd head data.csv --n 100

# Last N rows
pd tail data.csv --n 50

# Random sample
pd sample data.csv --n 100
pd sample data.csv --frac 0.1 --seed 42

# Drop rows with null values in any column
pd dropna data.csv

# Drop rows with null values in specific column
pd dropna data.csv --column column_name
```

### Stats commands

```bash
# Descriptive statistics
pd describe data.csv

# DataFrame information
pd info data.csv

# Count unique values
pd value-counts data.csv city
pd value-counts data.csv department --normalize

# Group by and aggregate
pd groupby data.csv department --col salary --agg sum
pd groupby data.csv city --col age --agg mean

# Unique values in a column
pd unique data.csv country
```

### Piping

All commands support piping through stdin/stdout:

```bash
cat data.csv | pd head --n 100 | pd select name age | pd query "age > 30"
```

### Output Formats

Specify output format with the file extension:

```bash
pd select data.csv name age -o output.xlsx
pd query data.json "age > 30" -o filtered.csv
```

Supported formats: CSV, XLSX, JSON, Parquet

## Development

```bash
# Format and lint
make check

# Run tests
make test

# Run coverage
make coverage
```
