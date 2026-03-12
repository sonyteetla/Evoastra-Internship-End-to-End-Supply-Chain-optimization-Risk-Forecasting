# 📦 DataCo Supply Chain Analysis and Forecasting

## 📌 Project Overview
This project analyzes the **DataCo Supply Chain dataset** to identify factors contributing to **late deliveries** and to build predictive models for **delivery risk and sales forecasting**.

The analysis combines **data preprocessing, feature engineering, exploratory data analysis, statistical testing, machine learning models, and time-series forecasting** to generate actionable business insights.

---

# 📊 Dataset
The dataset contains supply chain transaction information including:

- Order details
- Shipping information
- Customer details
- Product information
- Sales and profit metrics

The data is used to analyze **delivery performance, customer purchasing patterns, and operational efficiency**.

---

# 🔄 Project Workflow

The project follows a structured data science pipeline:

1. Data Cleaning and Preprocessing  
2. Feature Engineering  
3. Exploratory Data Analysis (EDA)  
4. Statistical Hypothesis Testing  
5. Machine Learning Modeling  
6. Model Evaluation  
7. Feature Importance Analysis  
8. Time Series Forecasting  
9. Business Risk Assessment  

---

# ⚙️ Feature Engineering

New features were created to improve model performance and capture operational patterns within the supply chain.

### Key Engineered Features

- Shipping Delay  
- Processing Time  
- Late Shipment Flag  
- Order Month and Year  
- Weekend Indicator  
- Profit Margin  
- Sales per Item  
- Order Size  
- Discount Amount  
- Customer Order Frequency  
- Average Customer Order Value  
- Product Demand  
- Category Demand  

These features provide **better representation of operational and financial patterns** in the dataset.

---

# 📈 Exploratory Data Analysis (EDA)

Exploratory analysis was performed to understand dataset structure and identify patterns affecting **sales performance and delivery efficiency**.

### Key Analyses

- Sales Distribution
- Monthly Sales Trends
- Late Delivery by Shipping Mode
- Late Delivery by Region
- Profit vs Discount Analysis
- Top Products by Sales

EDA helps uncover **business insights and operational bottlenecks** in the supply chain.

---

# 📊 Statistical Analysis

Statistical tests were conducted to validate relationships between supply chain variables.

### Hypothesis Testing

| Hypothesis | Test Used | Purpose |
|------------|-----------|--------|
| Shipping Mode vs Delivery Delay | ANOVA | Evaluate logistics performance |
| Customer Segment vs Sales | ANOVA | Compare purchasing behavior |
| Product Category vs Late Delivery Risk | Chi-Square | Identify category-level risks |
| Seasonal Demand | ANOVA | Detect monthly demand variation |
| Shipping Delay vs Sales Trend | Granger Causality | Evaluate temporal impact |

---

### Weekend vs Weekday Sales

A **t-test** was used to determine whether sales differ between weekends and weekdays.

- **p < 0.05** → Significant difference  
- **p > 0.05** → No significant difference

---

### Correlation Analysis

A correlation matrix was used to examine relationships among numerical variables such as:

- Sales
- Order Quantity
- Profit Margin
- Shipping Delay

---

# ⏱ Granger Causality Test

The Granger causality test evaluated whether **shipping delays influence sales trends over time**.

Results show **no significant causality**, indicating that sales trends are primarily influenced by **demand patterns, pricing strategies, and seasonal factors rather than delivery delays**.

---

# 🤖 Machine Learning Models

Two classification models were implemented to predict **late delivery risk**:

- Logistic Regression
- Random Forest

Random Forest demonstrated **better predictive performance** in identifying late deliveries.

---

# 📉 Regression & Forecasting Models

Several regression models were used to predict sales performance:

- Linear Regression
- Ridge Regression (reduces overfitting)
- Lasso Regression (performs feature selection)

Models were evaluated using:

- RMSE
- MAE
- R² Score
- 5-fold Cross Validation

---

# ⏳ ARIMA Time Series Forecasting

An **ARIMA(1,1,1)** model was implemented to forecast future sales trends.

Key observation:

- The **Moving Average (MA) component is statistically significant**, suggesting that short-term demand fluctuations influence sales more than long-term trends.

ARIMA effectively captures **temporal demand patterns in supply chain data**.

---

# 🧪 Model Evaluation

Regression models produced **similar performance results**, with low R² values (~0.03), indicating that simple linear models capture only a small portion of sales variation.

Therefore, **time-series forecasting provides better insights for demand prediction**.

---

# 🏆 Model Selection

The **ARIMA forecasting model** was selected because it captures **temporal demand patterns that regression models cannot fully explain**.

This model supports:

- Demand forecasting
- Inventory planning
- Supply chain optimization

---

# 🔍 Feature Importance Analysis

Feature importance was analyzed using:

- Pearson Correlation
- Spearman Correlation
- Mutual Information
- SHAP values

### Key Findings

- **Order item quantity** has the strongest relationship with sales
- **Profit margin** contributes through non-linear relationships
- **Order month** reflects seasonal demand patterns
- **Shipping delay** and weekend indicators have minimal impact on sales prediction

These insights highlight that **product demand and pricing factors drive sales performance**.

---

# ⚠️ Business Risk Assessment

Supply chain risk was analyzed based on shipping delays and potential financial impact.

### Key Insights

- Most orders fall into **low-risk delivery categories**
- **High-risk deliveries** may lead to significant revenue exposure
- Monte Carlo simulation estimates potential financial losses caused by delivery disruptions

These insights help organizations **manage supply chain risks and optimize logistics planning**.

---

# 💡 Key Business Insights

- Shipping delay is a major indicator of **late delivery risk**
- Sales trends are influenced more by **product demand and seasonal patterns**
- Forecasting models help anticipate **future supply chain demand and operational risks**

---

# 🛠 Tools & Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- Statsmodels
- Matplotlib
- Seaborn
- Jupyter Notebook

---

# 📌 Conclusion

This project demonstrates how **data analysis, machine learning, and time-series forecasting** can improve supply chain decision-making.

The insights generated help organizations:

- Predict demand trends
- Improve delivery performance
- Optimize inventory planning
- Reduce supply chain risks