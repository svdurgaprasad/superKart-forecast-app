# ---------------------------------------------------------
# 1. Clean categorical values
# ---------------------------------------------------------
def clean_categories(X):
    X = X.copy()
    X["Product_Sugar_Content"] = (
        X["Product_Sugar_Content"]
        .str.strip().replace({"reg": "Regular"})
    )
    return X