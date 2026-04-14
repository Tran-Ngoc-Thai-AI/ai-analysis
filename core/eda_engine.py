# def run_eda(df):
#     eda = {
#         "n_rows": df.shape[0],
#         "n_cols": df.shape[1],
#         "columns": list(df.columns),
#         "numeric_cols": df.select_dtypes(include="number").columns.tolist(),
#         "categorical_cols": df.select_dtypes(exclude="number").columns.tolist(),
#         "missing": df.isnull().sum().to_dict(),
#         "describe": df.describe(include="all").to_dict()
#     }
#     return eda


def run_eda(df):

    num_cols = df.select_dtypes(include="number").columns
    cat_cols = df.select_dtypes(exclude="number").columns

    eda = {
        "schema": {
            "n_rows": df.shape[0],
            "n_cols": df.shape[1],
            "columns": list(df.columns),
            "numeric_cols": num_cols.tolist(),
            "categorical_cols": cat_cols.tolist(),
        },

        "data_quality": {
            "missing": df.isnull().sum().to_dict(),
            "duplicate_rows": df.duplicated().sum()
        },

        "distribution": {
            "describe": df.describe(include="all").to_dict(),
            "skewness": df[num_cols].skew().to_dict()
        },

        "categorical_summary": {
            c: df[c].value_counts().head(10).to_dict()
            for c in cat_cols
        },

        "correlation": df.corr(numeric_only=True).to_dict(),

        # 10-row preview to support prompt requests without passing full df
        "data_preview": df.head(10).to_dict(orient="records")
    }

    return eda
