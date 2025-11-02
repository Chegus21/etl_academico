from __future__ import annotations
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_hist(df: pd.DataFrame, col: str, out_dir: str | Path) -> Path:
    out = Path(out_dir) / f"hist_{col}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6,4))
    sns.histplot(df[col].dropna(), kde=True)
    plt.title(f"Histograma de {col}")
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out

def plot_trend(df: pd.DataFrame, x: str, y: str, out_dir: str | Path) -> Path:
    out = Path(out_dir) / f"trend_{x}_{y}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(6,4))
    sns.lineplot(data=df, x=x, y=y)
    plt.title(f"Tendencia {y} por {x}")
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out
