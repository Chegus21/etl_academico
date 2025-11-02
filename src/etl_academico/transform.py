from __future__ import annotations
from pathlib import Path
from typing import Iterable, Optional
import pandas as pd
import numpy as np

def load_csv(path: str | Path, dtype: Optional[dict] = None) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=dtype)
    return df

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip().str.lower().str.replace(" ", "_").str.normalize("NFKD")
    )
    return df

def drop_outliers(df: pd.DataFrame, cols: Iterable[str], k: float = 1.5) -> pd.DataFrame:
    df = df.copy()
    for c in cols:
        if c in df.select_dtypes(include=[np.number]).columns:
            q1 = df[c].quantile(0.25)
            q3 = df[c].quantile(0.75)
            iqr = q3 - q1
            low, high = q1 - k * iqr, q3 + k * iqr
            df = df[(df[c] >= low) & (df[c] <= high)]
    return df

def save_parquet(df: pd.DataFrame, out_path: str | Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)
