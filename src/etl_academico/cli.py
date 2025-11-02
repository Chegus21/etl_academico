from __future__ import annotations
from pathlib import Path
import typer
import pandas as pd
from .transform import load_csv, normalize_columns, drop_outliers, save_parquet
from .plot import plot_hist, plot_trend

app = typer.Typer(help="ETL académico ligero con pandas.")

@app.command()
def ingest(src: str, out: str = "data/output/bronze.parquet"):
    """Carga CSV, normaliza columnas y guarda en Parquet."""
    df = load_csv(src)
    df = normalize_columns(df)
    save_parquet(df, out)
    typer.echo(f"Bronce guardado en {out}")

@app.command()
def clean(src: str = "data/output/bronze.parquet",
          out: str = "data/output/silver.parquet",
          metrics: str = "promedio,calificacion"):
    """Limpia outliers de columnas numéricas (IQR) y guarda."""
    cols = [c.strip() for c in metrics.split(",") if c.strip()]
    df = pd.read_parquet(src)
    df = drop_outliers(df, cols)
    save_parquet(df, out)
    typer.echo(f"Plata guardado en {out}")

@app.command()
def report(src: str = "data/output/silver.parquet", out_dir: str = "data/output"):
    """Genera gráficos básicos y CSV de resumen."""
    df = pd.read_parquet(src)
    numeric_cols = df.select_dtypes("number").columns.tolist()
    if numeric_cols:
        plot_hist(df, numeric_cols[0], out_dir)
    if len(numeric_cols) >= 2:
        plot_trend(df.reset_index(), x=df.index.name or "index", y=numeric_cols[0], out_dir=out_dir)
    summary = df.describe(include="all")
    summary.to_csv(Path(out_dir) / "resumen.csv")
    typer.echo(f"Reporte generado en {out_dir}")

if __name__ == "__main__":
    app()
