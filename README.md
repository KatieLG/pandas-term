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
| `pd merge`        | `pd.merge()`             | Merge two dataframes           |
| `pd batch`        | `df.iloc[]`              | Split dataframe into batches   |
| `pd query`        | `df.query()`             | Filter using query expressions |
| `pd head`         | `df.head()`              | Get first n rows               |
| `pd tail`         | `df.tail()`              | Get last n rows                |
| `pd sample`       | `df.sample()`            | Random sample of rows          |
| `pd dropna`       | `df.dropna()`            | Drop rows with null values     |
| `pd describe`     | `df.describe()`          | Descriptive statistics         |
| `pd info`         | `df.info()`              | DataFrame information          |
| `pd unique`       | `df[col].unique()`       | Unique values in column        |
| `pd size`         | `df.size`                | Total number of elements       |
| `pd shape`        | `df.shape`               | Dimensions (rows, columns)     |
| `pd columns`      | `df.columns`             | Column names                   |
| `pd memory`       | `df.memory_usage()`      | Memory usage of each column    |
| `pd value-counts` | `df[col].value_counts()` | Count unique values            |
| `pd groupby`      | `df.groupby().agg()`     | Group by and aggregate         |

## Usage

All commands accept an input file path (or `-` for stdin) and an optional `-o/--output` flag for the output file (or `-` for stdout).

### Transform commands

```bash
# Select specific columns (comma-separated)
pd select name,age data.csv

# Drop columns (comma-separated)
pd drop unwanted_column data.csv

# Sort by columns (comma-separated for multiple)
pd sort age data.csv --ascending
pd sort "age,name" data.csv --descending

# Remove duplicate rows
pd dedup data.csv
pd dedup --subset name,email data.csv

# Merge two dataframes
pd merge left.csv right.csv --on user_id --how inner
pd merge left.csv right.csv --left-on id --right-on user_id --how left

# Split dataframe into batches
pd batch 100 data.csv -o "output_batch_{}.csv"
```

### Filter commands

```bash
# Filter using pandas query expressions
pd query "age > 30 and city == 'NYC'" data.csv

# First N rows
pd head --n 100 data.csv

# Last N rows
pd tail --n 50 data.csv

# Random sample
pd sample --n 100 data.csv
pd sample --frac 0.1 --seed 42 data.csv

# Drop rows with null values in any column
pd dropna data.csv

# Drop rows with null values in specific column
pd dropna --column column_name data.csv
```

### Stats commands

```bash
# Descriptive statistics
pd describe data.csv

# DataFrame information
pd info data.csv

# Unique values in a column
pd unique country data.csv

# Total number of elements
pd size data.csv

# Dimensions (rows, columns)
pd shape data.csv

# Column names
pd columns data.csv

# Memory usage of each column
pd memory data.csv
pd memory --deep data.csv
```

### Aggregate commands

```bash
# Count unique values
pd value-counts city data.csv
pd value-counts department data.csv --normalize

# Group by and aggregate (comma-separated for multiple group columns)
pd groupby department data.csv --col salary --agg sum
pd groupby "city,department" data.csv --col age --agg mean
```

### Piping

All commands support piping through stdin/stdout. When piping, you can omit the input file argument (it defaults to stdin):

```bash
cat data.csv | pd head --n 100 | pd select name,age | pd query "age > 30"

# Or chain commands directly
pd sort stars github.csv --descending | pd head --n 10 | pd select name,stars
```

### Output Formats

When writing to a file, the format is determined by the file extension:

```bash
pd select name,age data.csv -o output.xlsx
pd query "age > 30" data.json -o filtered.parquet
```

For stdout output (default is CSV), use `--json` to output as JSON:

```bash
pd head --n 10 data.csv --json
pd query "age > 30" data.csv --json | jq '.[] | .name'
```

Supported formats: CSV, XLSX, JSON, Parquet (file output) / CSV, JSON (stdout)

## Development

| Command         | Description                               |
| --------------- | ----------------------------------------- |
| `make format`   | Format code with ruff                     |
| `make lint`     | Run linting checks (ruff + type checking) |
| `make test`     | Run pytest tests                          |
| `make check`    | Format, lint, and run tests               |
| `make coverage` | Run tests with coverage report            |
| `make compile`  | Compile standalone binary with Nuitka     |
