# 🚀 GitHub Repository Setup Instructions

## Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill in the repository details:
   - **Repository name**: `EY_DataAnalytics_Portfolio` (or your preferred name)
   - **Description**: `Comprehensive data analytics portfolio showcasing advanced analytics capabilities for EY consulting roles`
   - **Visibility**: Public (required for free Streamlit deployment)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)

## Step 2: Connect Local Repository to GitHub

After creating the repository on GitHub, copy the repository URL and run these commands:

```bash
# Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/EY_DataAnalytics_Portfolio.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy to Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `YOUR_USERNAME/EY_DataAnalytics_Portfolio`
5. Choose the main file: `01_Financial_Risk_Analytics/financial_risk_dashboard.py`
6. Click "Deploy"

## Step 4: Deploy Other Dashboards (Optional)

You can deploy each dashboard separately:

1. **Supply Chain Dashboard**: `02_Supply_Chain_Optimization/supply_chain_dashboard.py`
2. **Customer Analytics**: `03_Customer_Analytics/customer_analytics_dashboard.py`
3. **ESG Analytics**: `04_ESG_Analytics/esg_dashboard.py`

## Quick Commands Summary

After creating the GitHub repository, run:

```bash
git remote add origin https://github.com/YOUR_USERNAME/EY_DataAnalytics_Portfolio.git
git branch -M main
git push -u origin main
```

Then visit [share.streamlit.io](https://share.streamlit.io) to deploy!