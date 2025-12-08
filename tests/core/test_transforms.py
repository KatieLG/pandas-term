import pandas as pd

from pandas_term.core import transforms


def test_batch_dataframe_single_size(sample_df: pd.DataFrame) -> None:
    """Test splitting dataframe of size 6 into batches of 2."""
    batches = transforms.batch_dataframe(sample_df, sizes=[2])
    assert len(batches) == 3
    assert len(batches[0]) == 2
    assert len(batches[1]) == 2
    assert len(batches[2]) == 2


def test_batch_dataframe_variable_sizes(sample_df: pd.DataFrame) -> None:
    """Test batching with variable sizes that repeat last size."""
    batches = transforms.batch_dataframe(sample_df, sizes=[1, 2])
    assert len(batches) == 4
    assert len(batches[0]) == 1
    assert len(batches[1]) == 2
    assert len(batches[2]) == 2
    assert len(batches[3]) == 1


def test_batch_dataframe_uneven_division(sample_df: pd.DataFrame) -> None:
    """Test batching when size doesnt divide evenly."""
    df = sample_df.head(3)
    batches = transforms.batch_dataframe(df, sizes=[2])
    assert len(batches) == 2
    assert len(batches[0]) == 2
    assert len(batches[1]) == 1
