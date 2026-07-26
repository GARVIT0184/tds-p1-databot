
import pandas as pd
import duckdb
import matplotlib.pyplot as plt


def load_csv(path):
    """
    Load a CSV file.
    """
    return pd.read_csv(path)


def dataset_summary(df):
    """
    Basic information about a dataframe.
    """
    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": list(df.columns),
        "missing_values": df.isnull().sum().to_dict()
    }


def numeric_summary(df):
    """
    Summary statistics for numeric columns.
    """
    return df.describe().to_dict()


def correlation(df):
    """
    Correlation matrix of numeric columns.
    """
    return df.corr(numeric_only=True).to_dict()


def sql_query(df, query):
    """
    Run SQL on a dataframe using DuckDB.
    Example:
        SELECT AVG(age) FROM df
    """
    con = duckdb.connect()
    con.register("df", df)
    result = con.execute(query).fetchdf()
    con.close()
    return result.to_dict(orient="records")


def create_plot(df, x, y, filename="plot.png"):
    """
    Create a simple line plot.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(df[x], df[y])
    plt.xlabel(x)
    plt.ylabel(y)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    return filename
