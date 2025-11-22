# pandas-cli

A CLI for applying common pandas functions to data files in the terminal.

## Installation

```bash
uv sync
```

## Usage

All commands accept an input file path (or `-` for stdin) and an optional `-o/--output` flag for the output file (or `-` for stdout).

### Transform Commands

```bash
# Select specific columns
pd select data.csv name age

# Drop columns
pd drop data.csv unwanted_column

# Sort by columns
pd sort data.csv age --ascending
pd sort data.csv age --descending

# Remove duplicate rows
pd dedup data.csv
pd dedup data.csv --subset name email

# Reset the dataframe index
pd reset-index data.csv
```

### Filter Commands

```bash
# Filter using pandas query expressions
pd query data.csv "age > 30 and city == 'NYC'"

# Get first/last n rows
pd head data.csv --n 10
pd tail data.csv --n 5

# Random sample
pd sample data.csv --n 100
pd sample data.csv --frac 0.1 --seed 42

# Drop rows with null values
pd dropna data.csv column_name
```

### Statistics Commands

```bash
# Descriptive statistics
pd describe data.csv

# DataFrame information
pd info data.csv

# Count unique values
pd value-counts data.csv city
pd value-counts data.csv department --normalize

# Group by and aggregate
pd groupby data.csv department --agg-column salary --agg-func sum
pd groupby data.csv city --agg-column age --agg-func mean

# Correlation matrix
pd corr data.csv
pd corr data.csv --columns age --columns salary

# Missing values analysis
pd missing data.csv

# Unique values in a column
pd unique data.csv city
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
