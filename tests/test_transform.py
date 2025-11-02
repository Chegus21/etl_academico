import pandas as pd
from etl_academico.transform import normalize_columns, drop_outliers

def test_normalize_columns():
    df = pd.DataFrame({" Col A ": [1], "Col-B": [2]})
    out = normalize_columns(df)
    assert "col_a" in out.columns
    assert "col-b" in out.columns

def test_drop_outliers():
    df = pd.DataFrame({"x":[1,2,3,100]})
    out = drop_outliers(df, ["x"], k=1.5)
    assert out["x"].max() < 100
