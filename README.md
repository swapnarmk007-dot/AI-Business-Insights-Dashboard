🤖 AI Business Intelligence Dashboard
An end-to-end AI-powered Business Intelligence Dashboard built using Flask, Python, Machine Learning, and Plotly. The application enables users to upload business datasets, perform data preprocessing, visualize insights, train machine learning models, generate predictions, forecast future trends, and download analytical reports—all through an interactive web interface.

🚀 Live Demo
Application: https://ais-pre-xbgnhf7djifqxgdhy2c2e7-643499324128.asia-east1.run.app/

📌 Features
📂 Dataset Upload
Upload CSV and Excel datasets
Automatic dataset preview
Dataset summary statistics
🧹 Data Preprocessing
Remove duplicate records
Fill missing values
Encode categorical variables
Rename columns
Download cleaned dataset
📊 Interactive Dashboard
Dataset KPIs
Number of rows
Number of columns
Missing values
Duplicate rows
Numeric columns
Categorical columns
Memory usage
Interactive Plotly visualizations
Business analytics charts
📈 Data Visualization
Sales by Category
Sales Trend Analysis
Region-wise Sales
Top Products Analysis
Customer Insights
🤖 Machine Learning (AutoML)
Supports both:

Regression
Linear Regression
Decision Tree Regressor
Random Forest Regressor
Gradient Boosting Regressor
Evaluation Metrics:

R² Score
MAE
RMSE
Classification
Logistic Regression
Decision Tree Classifier
Random Forest Classifier
K-Nearest Neighbors (KNN)
Evaluation Metrics:

Accuracy
Precision
Recall
F1 Score
Automatically selects the best-performing model and saves it for prediction.

🔮 Prediction
Upload new dataset
Load trained model
Generate predictions
Download prediction results
📉 Forecasting
Time series forecasting using Linear Regression
User-selectable target column
User-selectable date column
Forecast future values
Interactive Plotly forecast visualization
📄 Reports
Generate downloadable reports containing:

Dataset Summary
Best Machine Learning Model
Model Performance
Business Insights
💡 AI Insights
Automatically generates business insights from uploaded datasets, helping users identify:

Sales trends
High-performing categories
Regional performance
Data quality observations
Business recommendations
🛠️ Technologies Used
Programming Language
Python
Web Framework
Flask
Data Analysis
Pandas
NumPy
Machine Learning
Scikit-learn
Joblib
Data Visualization
Plotly
Frontend
HTML5
CSS3
Bootstrap 5
Bootstrap Icons
Jinja2
Deployment
Railway
📂 Project Structure
AI_Business/
│
├── app.py
├── requirements.txt
├── models/
├── reports/
├── uploads/
├── static/
│   ├── css/
│   ├── images/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   ├── analytics.html
│   ├── preprocessing.html
│   ├── machine_learning.html
│   ├── prediction.html
│   ├── forecast.html
│   ├── reports.html
│   ├── insights.html
│   └── about.html
│
└── utils/
⚙️ Installation
Clone the repository

git clone https://github.com/yourusername/AI_Business_Intelligence_Dashboard.git
Navigate to project directory

cd AI_Business_Intelligence_Dashboard
Create virtual environment

python -m venv venv
Activate virtual environment

Windows

venv\Scripts\activate
Linux / Mac

source venv/bin/activate
Install dependencies

pip install -r requirements.txt
Run application

python app.py
Open browser

http://127.0.0.1:5000
📊 Workflow
Upload Dataset
Preprocess Data
Explore Dashboard
Analyze Charts
Train Machine Learning Models (Upload cleaned dataset)
Compare Model Performance
Select Best Model
Generate Predictions
Forecast Future Trends
Download Reports
📈 Machine Learning Workflow
Upload Dataset
       │
       ▼
Data Cleaning
       │
       ▼
Feature Encoding
       │
       ▼
Train/Test Split
       │
       ▼
Train Multiple Models
       │
       ▼
Compare Performance
       │
       ▼
Best Model Selection
       │
       ▼
Prediction
🌐 Deploymen
This application is deployed on Google Cloud Run.

Live Application: https://ais-pre-xbgnhf7djifqxgdhy2c2e7-643499324128.asia-east1.run.app/

📷 Application Modules
Home
Dashboard
Analytics
Data Preprocessing
Machine Learning
Prediction
Forecast
Reports
AI Insights
About
🎯 Future Enhancements
XGBoost Integration
LightGBM Support
Deep Learning Models
SHAP Explainability
PDF Dashboard Export
User Authentication
Database Integration
Cloud Storage Support
Auto Feature Engineering
Advanced Forecasting Models (ARIMA, Prophet)
👩‍💻 Developed By
swapna v

Data Science | Machine Learning | Business Intelligence

⭐ If you found this project useful, consider giving it a star!
