from flask import Flask, render_template, request, send_file
import os
import pandas as pd
from utils.visualization import (
    sales_by_category, sales_trend, region_sales, top_products, 
    sales_by_segment, profit_by_category, top_customers, correlation_heatmap
)
from utils.insights import generate_insights
from utils.preprocessing import (
    remove_duplicates,
    remove_missing,
    rename_columns,
    convert_dates,
    encode_categorical
)
from utils.report_generator import generate_pdf_report
from pandas.api.types import is_numeric_dtype
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import (r2_score, mean_absolute_error, mean_squared_error, accuracy_score, precision_score, recall_score, f1_score)
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsClassifier
import joblib
import numpy as np
from utils.feature_importance import create_feature_importance
from utils.ai_assistant import answer_question
from utils.forecast import generate_forecast
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from plotly import express as px


app = Flask(__name__)

df = None

best_model_name = "Not Trained"
best_model_score = "N/A"

# Upload folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- HOME PAGE ----------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/analytics")
def analytics():
    global df

    if df is None:
        return "Please upload a dataset first."

    category_chart = sales_by_category(df)
    trend_chart = sales_trend(df)
    region_chart = region_sales(df)
    segment_chart = sales_by_segment(df)
    profit_chart = profit_by_category(df)
    customer_chart = top_customers(df)
    heatmap = correlation_heatmap(df)

    return render_template(
        "analytics.html",
        category_chart=category_chart,
        trend_chart=trend_chart,
        region_chart=region_chart,
        segment_chart=segment_chart,
        profit_chart=profit_chart,
        customer_chart=customer_chart,
        heatmap=heatmap
    )


@app.route("/preprocessing")
def preprocessing():
    global df

    if df is None:
        return "Please upload a dataset first."

    rows = df.head(10).to_html(
        classes="table table-striped table-bordered",
        index=False
    )

    return render_template(
        "preprocessing.html",
        table=rows,
        rows_count=df.shape[0],
        columns_count=df.shape[1],
        missing_values=df.isnull().sum().sum(),
        duplicate_rows=df.duplicated().sum()
    )


@app.route("/insights")
def insights():
    global df

    if df is None:
        return "Please upload a dataset first."

    ai_insights = generate_insights(df)

    return render_template(
        "insights.html",
        insights=ai_insights,
        rows_count=df.shape[0],
        columns_count=df.shape[1],
        missing_values=df.isnull().sum().sum(),
        duplicate_rows=df.duplicated().sum()
    )


@app.route("/forecast")
def forecast():
    global df

    if df is None:
        return "Please upload a dataset first."

    return render_template(
        "forecast.html",
        columns=df.columns.tolist()
    )


@app.route("/reports")
def reports():
    return render_template("reports.html")


@app.route("/download_predictions")
def download_predictions():
    return send_file(
        "reports/predictions.csv",
        as_attachment=True
    )


@app.route("/download_model")
def download_model():
    return send_file(
        "models/best_model.pkl",
        as_attachment=True
    )


@app.route("/download_pdf")
def download_pdf():
    global df
    global best_model_name
    global best_model_score

    if df is None:
        return "Please upload a dataset first."

    os.makedirs("reports", exist_ok=True)

    pdf_path = "reports/business_report.pdf"

    doc = SimpleDocTemplate(pdf_path)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph("<b>AI BUSINESS INTELLIGENCE REPORT</b>", styles["Title"])
    )

    story.append(
        Paragraph(
            f"Generated On: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph("<br/>", styles["Normal"])
    )

    story.append(
        Paragraph("<b>Dataset Summary</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(f"Rows : {df.shape[0]}", styles["Normal"])
    )

    story.append(
        Paragraph(f"Columns : {df.shape[1]}", styles["Normal"])
    )

    story.append(
        Paragraph(
            f"Missing Values : {df.isnull().sum().sum()}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Duplicate Rows : {df.duplicated().sum()}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph("<br/>", styles["Normal"])
    )

    story.append(
        Paragraph("<b>Machine Learning Summary</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            f"Best Model : {best_model_name}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            f"Best Score : {best_model_score}",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph("<br/>", styles["Normal"])
    )

    story.append(
        Paragraph("<b>Developed By</b>", styles["Heading2"])
    )

    story.append(
        Paragraph(
            "SWAPNA",
            styles["Normal"]
        )
    )

    story.append(
        Paragraph(
            "AI Business Intelligence Dashboard",
            styles["Normal"]
        )
    )

    doc.build(story)

    return send_file(
        pdf_path,
        as_attachment=True
    )


@app.route("/about")
def about():
    return render_template("about.html")


# ---------------- FILE UPLOAD ----------------
@app.route("/upload", methods=["POST"])
def upload():
    global df
    print(request.form)
    print(request.form.keys())

    if "file" not in request.files:
        return "No file uploaded."

    file = request.files["file"]

    if file.filename == "":
        return "Please select a file."

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    if file.filename.endswith(".csv"):
        df = pd.read_csv(filepath)

    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(filepath)

    else:
        return "Only CSV and Excel files are supported."

    insights = generate_insights(df)

    rows_count = df.shape[0]
    columns_count = df.shape[1]
    missing_values = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()
    numeric_columns = df.select_dtypes(include="number").shape[1]
    categorical_columns = df.select_dtypes(include="object").shape[1]

    memory_usage = round(
        df.memory_usage(deep=True).sum() / (1024 * 1024),
        2
    )

    rows = df.head().to_html(
        classes="table table-striped table-bordered table-hover",
        index=False
    )

    category_chart = sales_by_category(df)
    trend_chart = sales_trend(df)
    region_chart = region_sales(df)
    product_chart = top_products(df)
    segment_chart = sales_by_segment(df)
    profit_chart = profit_by_category(df)
    customer_chart = top_customers(df)

    return render_template(
        "dashboard.html",
        table=rows,
        shape=df.shape,
        columns=df.columns.tolist(),
        rows_count=rows_count,
        columns_count=columns_count,
        missing_values=missing_values,
        duplicate_rows=duplicate_rows,
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,
        memory_usage=memory_usage,
        category_chart=category_chart,
        trend_chart=trend_chart,
        region_chart=region_chart,
        product_chart=product_chart,
        insights=insights,
        segment_chart=segment_chart,
        profit_chart=profit_chart,
        customer_chart=customer_chart
    )


@app.route("/clean_data", methods=["POST"])
def clean_data():
    global df

    if df is None:
        return "Please upload a dataset first."

    if "remove_duplicates" in request.form:
        df.drop_duplicates(inplace=True)

    if "fill_missing" in request.form:
        for col in df.columns:
            if is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())
            else:
                mode = df[col].mode()
                if not mode.empty:
                    df[col] = df[col].fillna(mode.iloc[0])

    if "encode_categorical" in request.form:
        encoder = LabelEncoder()
        for col in df.select_dtypes(include="object").columns:
            if "date" in col.lower():
                continue
            df[col] = encoder.fit_transform(df[col].astype(str))

    rows = df.head(10).to_html(
        classes="table table-striped table-bordered",
        index=False
    )

    return render_template(
        "preprocessing.html",
        table=rows,
        rows_count=df.shape[0],
        columns_count=df.shape[1],
        missing_values=df.isnull().sum().sum(),
        duplicate_rows=df.duplicated().sum(),
        columns=df.columns.tolist()
    )


@app.route("/download_cleaned")
def download_cleaned():
    global df

    if df is None:
        return "No dataset available."

    output_path = "reports/cleaned_dataset.csv"
    df.to_csv(output_path, index=False)

    return send_file(
        output_path,
        as_attachment=True
    )


@app.route("/rename_column", methods=["POST"])
def rename_column():
    global df

    if df is None:
        return "Please upload a dataset first."

    old_name = request.form["old_name"]
    new_name = request.form["new_name"].strip()

    if new_name:
        df.rename(columns={old_name: new_name}, inplace=True)

    rows = df.head(10).to_html(
        classes="table table-striped table-bordered",
        index=False
    )

    return render_template(
        "preprocessing.html",
        table=rows,
        rows_count=df.shape[0],
        columns_count=df.shape[1],
        missing_values=df.isnull().sum().sum(),
        duplicate_rows=df.duplicated().sum(),
        columns=df.columns.tolist()
    )


@app.route("/data_profile")
def data_profile():
    global df

    if df is None:
        return "Please upload a dataset first."

    profile = pd.DataFrame({
        "Column": df.columns,
        "Data Type": df.dtypes.astype(str),
        "Missing Values": df.isnull().sum().values,
        "Unique Values": df.nunique().values
    })
    table = profile.to_html(
        classes="table table-striped table-bordered table-hover",
        index=False
    )
    stats = df.describe(include="all").fillna("").to_html(
        classes="table table-striped table-bordered",
        index=True
    )
    return render_template(
        "data_profile.html",
        table=table,
        stats=stats,
        rows=df.shape[0],
        columns=df.shape[1],
        memory=round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
        missing=df.isnull().sum().sum(),
        duplicates=df.duplicated().sum()
    )


@app.route("/visualization")
def visualization():
    global df

    if df is None:
        return "Please upload a dataset first."

    return render_template(
        "visualization.html",
        columns=df.columns.tolist()
    )


@app.route("/generate_chart", methods=["POST"])
def generate_chart():
    global df

    if df is None:
        return "Please upload a dataset first."

    x = request.form["x"]
    y = request.form["y"]
    chart = request.form["chart"]

    fig = None

    if chart == "Bar":
        data = df.groupby(x)[y].sum().reset_index()
        fig = px.bar(data, x=x, y=y, color=x, title=f"{y} by {x}")

    elif chart == "Line":
        data = df.groupby(x)[y].sum().reset_index()
        fig = px.line(data, x=x, y=y, markers=True, title=f"{y} by {x}")

    elif chart == "Scatter":
        fig = px.scatter(df, x=x, y=y, color=x, title=f"{y} vs {x}")

    elif chart == "Pie":
        data = df.groupby(x)[y].sum().reset_index()
        fig = px.pie(data, names=x, values=y, title=f"{y} by {x}")

    chart_html = fig.to_html(full_html=False)

    return render_template(
        "visualization.html",
        columns=df.columns.tolist(),
        chart=chart_html
    )


@app.route("/machine_learning")
def machine_learning():
    global df

    if df is None:
        return "Please upload a dataset first."

    return render_template(
        "machine_learning.html",
        columns=df.columns.tolist()
    )


@app.route("/train_model", methods=["POST"])
def train_model():
    global df
    global best_model_name
    global best_model_score

    if df is None:
        return "Please upload a dataset first."

    target = request.form["target"]
    problem = request.form["problem"]

    data = df.copy()
    data = data.dropna(subset=[target])

    X = data.drop(columns=[target])
    y = data[target]

    drop_cols = ["Row ID", "Order ID", "Customer ID"]
    X = X.drop(columns=[c for c in drop_cols if c in X.columns], errors="ignore")

    for col in X.columns:
        if "date" in col.lower():
            X[col] = pd.to_datetime(X[col], errors="coerce")
            X[col] = X[col].map(lambda x: x.toordinal() if pd.notnull(x) else 0)

    X = pd.get_dummies(X, drop_first=True)

    joblib.dump(X.columns.tolist(), "models/model_columns.pkl")
    joblib.dump(target, "models/target.pkl")
    joblib.dump(problem, "models/problem.pkl")

    X = X.fillna(0)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    if problem == "Regression":
        models = {
            "Linear Regression": LinearRegression(),
            "Decision Tree": DecisionTreeRegressor(random_state=42),
            "Random Forest": RandomForestRegressor(n_estimators=20, random_state=42, n_jobs=-1),
            "Gradient Boosting": GradientBoostingRegressor(n_estimators=50, random_state=42)
        }

        results = []
        best_model = None
        best_score = float("-inf")
        best_model_name = ""

        for name, model in models.items():
            model.fit(X_train, y_train)
            prediction = model.predict(X_test)
            r2 = r2_score(y_test, prediction)
            mae = mean_absolute_error(y_test, prediction)
            rmse = np.sqrt(mean_squared_error(y_test, prediction))

            results.append({
                "name": name,
                "r2": round(r2, 4),
                "mae": round(mae, 2),
                "rmse": round(rmse, 2)
            })

            if r2 > best_score:
                best_score = r2
                best_model = model
                best_model_name = name
                best_model_score = round(best_score, 4)

        os.makedirs("models", exist_ok=True)
        joblib.dump(best_model, "models/best_model.pkl")

        importance_chart = None
        try:
            importance_chart = create_feature_importance(best_model, X.columns)
        except:
            pass

        return render_template(
            "machine_learning.html",
            columns=df.columns.tolist(),
            results=results,
            best_model=best_model_name,
            best_score=best_model_score,
            importance_chart=importance_chart
        )

    if problem == "Classification":
        le = LabelEncoder()
        y = le.fit_transform(y.astype(str))

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        models = {
            "Logistic Regression": LogisticRegression(max_iter=200),
            "Decision Tree": DecisionTreeClassifier(random_state=42),
            "Random Forest": RandomForestClassifier(n_estimators=20, random_state=42, n_jobs=-1),
            "KNN": KNeighborsClassifier()
        }

        class_results = []
        best_model = None
        best_accuracy = 0
        best_classifier = ""

        for name, model in models.items():
            model.fit(X_train, y_train)
            prediction = model.predict(X_test)
            accuracy = accuracy_score(y_test, prediction)
            precision = precision_score(y_test, prediction, average="weighted", zero_division=0)
            recall = recall_score(y_test, prediction, average="weighted", zero_division=0)
            f1 = f1_score(y_test, prediction, average="weighted", zero_division=0)

            class_results.append({
                "name": name,
                "accuracy": round(accuracy, 4),
                "precision": round(precision, 4),
                "recall": round(recall, 4),
                "f1": round(f1, 4)
            })

            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_model = model
                best_classifier = name
                best_model_name = best_classifier
                best_model_score = round(best_accuracy, 4)

        os.makedirs("models", exist_ok=True)
        joblib.dump(best_model, "models/best_classifier.pkl")

        return render_template(
            "machine_learning.html",
            columns=df.columns.tolist(),
            class_results=class_results,
            best_classifier=best_classifier,
            best_accuracy=round(best_accuracy, 4)
        )


@app.route("/prediction")
def prediction():
    return render_template("prediction.html")


@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return "No file uploaded."

    file = request.files["file"]

    if file.filename == "":
        return "Please select a file."

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    if file.filename.endswith(".csv"):
        new_df = pd.read_csv(filepath)
    elif file.filename.endswith(".xlsx"):
        new_df = pd.read_excel(filepath)
    else:
        return "Only CSV and Excel files are supported."

    drop_cols = ["Row ID", "Order ID", "Customer ID"]
    new_df = new_df.drop(columns=[c for c in drop_cols if c in new_df.columns], errors="ignore")

    for col in new_df.columns:
        if "date" in col.lower():
            new_df[col] = pd.to_datetime(new_df[col], errors="coerce")
            new_df[col] = new_df[col].map(lambda x: x.toordinal() if pd.notnull(x) else 0)

    target = joblib.load("models/target.pkl")

    if target in new_df.columns:
        new_df.drop(columns=[target], inplace=True)

    new_df = pd.get_dummies(new_df, drop_first=True)
    new_df = new_df.fillna(0)

    model_columns = joblib.load("models/model_columns.pkl")
    new_df = new_df.reindex(columns=model_columns, fill_value=0)

    problem = joblib.load("models/problem.pkl")

    if problem == "Regression":
        model = joblib.load("models/best_model.pkl")
    else:
        model = joblib.load("models/best_classifier.pkl")

    predictions = model.predict(new_df)
    new_df["Prediction"] = predictions

    prediction_path = "reports/predictions.csv"
    new_df.to_csv(prediction_path, index=False)

    table = new_df.head(20).to_html(
        classes="table table-striped table-bordered",
        index=False
    )

    return render_template(
        "prediction.html",
        table=table
    )


@app.route("/generate_report")
def generate_report():
    global df
    global best_model_name
    global best_model_score

    if df is None:
        return "Please upload a dataset first."

    filepath = "reports/AI_Report.pdf"

    generate_pdf_report(
        filepath=filepath,
        rows=df.shape[0],
        columns=df.shape[1],
        missing=df.isnull().sum().sum(),
        duplicates=df.duplicated().sum(),
        best_model=best_model_name,
        score=best_model_score
    )

    return send_file(
        filepath,
        as_attachment=True
    )


@app.route("/chat")
def chat():
    return render_template("chat.html")


@app.route("/ask_ai", methods=["POST"])
def ask_ai():
    global df

    if df is None:
        return "Please upload a dataset first."

    question = request.form["question"]
    answer = answer_question(df, question)

    return render_template(
        "chat.html",
        answer=answer
    )


@app.route("/run_forecast", methods=["POST"])
def run_forecast():
    global df

    if df is None:
        return "Please upload a dataset first."

    date_col = request.form["date_column"]
    target_col = request.form["target_column"]
    periods = request.form["period"]

    chart, forecast = generate_forecast(df, date_col, target_col, periods)

    table = forecast.to_html(
        classes="table table-striped table-bordered",
        index=False
    )

    return render_template(
        "forecast.html",
        columns=df.columns.tolist(),
        forecast_chart=chart,
        forecast_table=table
    )


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)