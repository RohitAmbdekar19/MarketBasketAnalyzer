# 🛒 Market Basket Analyzer

A Data Science mini-project that analyzes customer shopping transactions to discover frequently purchased products and identify shopping patterns using the **Apriori Algorithm** and **Association Rule Mining**.

## 📌 Project Overview

Market Basket Analyzer helps understand which products customers frequently purchase together. It analyzes transaction data and generates frequent itemsets and association rules that can help businesses make better decisions about product placement, combo offers, and cross-selling.

The application provides an interactive web interface built using Streamlit, allowing users to enter transactions, adjust analysis settings, and view shopping patterns.

## 🎯 Objectives

- Identify frequently purchased products and product combinations.
- Discover relationships between products in shopping transactions.
- Calculate support and confidence for association rules.
- Generate useful business recommendations from shopping patterns.
- Demonstrate the practical application of Data Science in retail.

## ✨ Features

- **Interactive Web Interface:** Simple and user-friendly Streamlit application.
- **Transaction Management:** Add customer transactions using comma-separated product names.
- **Input Validation:** Prevents invalid product entries.
- **Frequent Itemset Mining:** Identifies product combinations that frequently occur together.
- **Association Rule Mining:** Discovers relationships between products.
- **Adjustable Parameters:** Change minimum support and minimum confidence.
- **Shopping Pattern Insights:** Displays the strongest discovered shopping patterns.
- **Business Recommendations:** Generates recommendations based on the discovered rules.
- **Dynamic Analysis:** Results update according to the entered transactions and selected settings.

## 🧠 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application interface |
| Pandas | Data handling and tabular results |
| MLxtend | Apriori algorithm and association rule mining |
| Apriori Algorithm | Finds frequent itemsets |
| Association Rule Mining | Identifies relationships between products |

## ⚙️ Algorithms and Concepts

### 1. Apriori Algorithm

The Apriori algorithm identifies frequent itemsets in transaction data based on a minimum support threshold.

### 2. Support

Support measures how frequently a product or product combination appears in all transactions.

**Formula:**

Support(A) = Transactions containing A / Total transactions

### 3. Confidence

Confidence measures how often customers purchase product B when they also purchase product A.

**Formula:**

Confidence(A → B) = Support(A ∪ B) / Support(A)

For example, if 4 out of 5 transactions contain bread and 3 of those transactions also contain juice, the confidence of Bread → Juice is 75%.

## 📁 Project Structure

```text
Market-Basket-Analyzer/
│
├── app.py
└── README.md
```

## 🚀 Installation and Setup

### Prerequisites

- Python installed on your computer
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/RohitAmbdekar19/MarketBasketAnalyzer.git
```

### Step 2: Open the Project Folder

```bash
cd MarketBasketAnalyzer
```

### Step 3: Install Dependencies

```bash
pip install streamlit pandas mlxtend
```

### Step 4: Run the Application

```bash
streamlit run app.py
```

The application will open in your default browser. If it does not, open the local URL displayed in the terminal, usually `http://localhost:8501`.

## 🛍️ How to Use

1. Launch the application.
2. Enter a shopping transaction using comma-separated product names, such as `Bread, Milk, Butter`.
3. Add multiple transactions to build the dataset.
4. Select the minimum support and minimum confidence.
5. Run or view the analysis provided by the application.
6. Explore frequent itemsets and association rules.
7. Review shopping pattern insights and business recommendations.

## 📊 Example Use Case

Suppose a store records transactions containing bread, milk, butter, cheese, and juice.

The analyzer may discover a rule such as:

**Bread → Juice**

If the confidence is 75%, it means that 75% of the transactions containing bread also contain juice.

A retailer could use this information to consider placing these products nearby or creating a suitable combo offer. Recommendations depend on the actual transaction data and selected thresholds.

## 🌍 Real-World Applications

- Supermarkets and grocery stores
- E-commerce product recommendations
- Product placement optimization
- Combo offers and promotional planning
- Cross-selling strategies
- Customer purchasing-pattern analysis

## 🔮 Future Enhancements

- Import transactions from CSV files.
- Store transaction history in a database.
- Add interactive charts and visual analytics.
- Use larger real-world retail datasets.
- Export analysis reports.
- Develop a more advanced recommendation system.

## 👨‍🎓 Academic Purpose

This project was developed as a Data Science lab mini-project to demonstrate data preprocessing, frequent itemset mining, association rule generation, and the practical use of data-driven insights in retail.

---

**Project Name:** Market Basket Analyzer  
**Domain:** Data Science  
**Algorithm:** Apriori Algorithm  
**Interface:** Streamlit  
**Repository:** https://github.com/RohitAmbdekar19/MarketBasketAnalyzer
