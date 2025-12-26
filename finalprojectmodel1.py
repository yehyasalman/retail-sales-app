import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, RobustScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import r2_score
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingRegressor

df = pd.read_csv(r"C:\Downloads\3abousi\retail_store_sales.csv")
df.drop(columns=["Transaction ID", "Customer ID",'Item'], inplace=True)
df.dropna(subset=['Total Spent'], inplace=True)

df["Transaction Date"] = pd.to_datetime(df["Transaction Date"])
df["month"] = df["Transaction Date"].dt.month.astype(str)
df["weekday"] = df["Transaction Date"].dt.weekday.astype(str)
df.drop(columns=["Transaction Date"], inplace=True)

cat_cols = ['Category', 'Payment Method', 'Location', 'month', 'weekday'] 
num_cols = ['Price Per Unit', 'Quantity', 'Discount Applied']

for col in cat_cols:
    df[col] = df[col].astype(str)

X = df.drop(columns="Total Spent")
y = df["Total Spent"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

preprocessor = ColumnTransformer(transformers=[
    ("cat", Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]), cat_cols),
    
    ("num", Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", RobustScaler())
    ]), num_cols)
])

model = Pipeline(steps=[
    ("pre", preprocessor),
    ("reg", GradientBoostingRegressor(
        random_state=42,
        n_estimators=300,
        max_depth=5
    ))
])

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(f"R2 Score: {r2_score(y_test, y_pred):.4f}")

with open("retail_sales_model.pkl", "wb") as f:
    pickle.dump(model, f)