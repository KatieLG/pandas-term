"""Service for reading and writing dataframes from various sources."""

import sys
from pathlib import Path

import pandas as pd

from pandas_term.cli.options import OutputOptions


def read_dataframe(file: str) -> pd.DataFrame:
    """Read a dataframe from a file path or stdin ('-')."""
    if file == "-":
        return pd.read_csv(sys.stdin)

    path = Path(file)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file}")

    suffix = path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in [".xlsx", ".xls"]:
        return pd.read_excel(path)
    if suffix == ".json":
        return pd.read_json(path)
    if suffix == ".parquet":
        return pd.read_parquet(path)
    raise ValueError(f"Unsupported file format: {suffix}")


def write_dataframe(df: pd.DataFrame, output_opts: OutputOptions) -> None:
    """Write a dataframe to file if specified else stdout."""
    if output_opts.file is None:
        if output_opts.use_json:
            sys.stdout.write(df.to_json(orient="records", indent=2))
            sys.stdout.write("\n")
        else:
            df.to_csv(sys.stdout, index=False)
        return

    path = Path(output_opts.file)
    suffix = path.suffix.lower()

    if suffix == ".csv":
        df.to_csv(path, index=False)
    elif suffix in [".xlsx", ".xls"]:
        df.to_excel(path, index=False)
    elif suffix == ".json":
        df.to_json(path, orient="records", indent=2)
    elif suffix == ".parquet":
        df.to_parquet(path, index=False)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")
