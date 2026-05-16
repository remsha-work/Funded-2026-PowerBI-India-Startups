# 💰 Funded2026 - Business Development Analytics Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://remsha-funded2026.streamlit.app)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Funded2026** is an interactive Business Development dashboard built with Streamlit to analyze funding trends, track leads, and visualize sales KPIs for 2026. This project demonstrates data-driven decision making for BD roles.

🔗 **Live Demo:** [remsha-funded2026.streamlit.app](https://remsha-funded2026.streamlit.app)
🔗 **Portfolio:** https://remsha-ansari.lovable.app/

## 📸 Dashboard Preview

| Overview | Lead Analysis | Revenue Trends |
| --- | --- | --- |
| KPI cards + YoY growth | Funnel & conversion rates | Monthly MRR tracking |

## ✨ Key Features

- **Real-time KPI Tracking**: Total Funding, Active Leads, Conversion Rate, MRR
- **Interactive Filters**: Filter by date range, industry, funding stage, region
- **Data Visualizations**: Plotly charts for funnel analysis, cohort retention, geo mapping
- **Lead Scoring Model**: Prioritize high-value prospects using custom metrics
- **Export Reports**: Download filtered data as CSV/PDF for stakeholder meetings
- **Responsive Design**: Mobile-friendly UI for on-the-go BD analysis

## 🛠️ Tech Stack

| Category | Tools |
| --- | --- |
| **Framework** | Streamlit 1.35+ |
| **Language** | Python 3.9+ |
| **Data Viz** | Plotly, Matplotlib, Seaborn |
| **Data Processing** | Pandas, NumPy |
| **Deployment** | Streamlit Community Cloud |
| **Version Control** | Git, GitHub |

## 📂 Project Architecture

Funded2026/
├── app.py                  # Main Streamlit application
├── pages/
│   ├── 1_Overview.py       # KPI dashboard & summary metrics
│   ├── 2_Lead_Analysis.py  # Funnel & lead scoring
│   └── 3_Revenue.py        # MRR, ARR & forecasting
├── data/
│   ├── funding_2026.csv    # Sample dataset - funding rounds
│   └── leads.csv           # Sample dataset - BD leads
├── utils/
│   ├── charts.py           # Plotly chart functions
│   └── data_loader.py      # CSV loading & preprocessing
├── assets/
│   └── logo.png            # Dashboard branding
├── requirements.txt        # Python dependencies
└── README.md               # You are here

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Funded2026.git
cd Funded2026
### 2. Install Dependencies
pip install -r requirements.txt
### 3. Run the App Locally
streamlit run app.py
App will open at `http://localhost:8501`

## 📊 Dataset

The dashboard uses sample BD data for 2026 including:
- *funding_2026.csv*: 500+ funding rounds with columns: `company`, `industry`, `stage`, `amount`, `date`, `investors`
- *leads.csv*: BD pipeline data with: `lead_id`, `source`, `status`, `deal_size`, `last_contact`, `score`

_Note: All data is synthetic and created for portfolio demonstration purposes._

## 🎯 Use Cases for Business Development

1. *Pipeline Management*: Track leads from MQL → SQL → Opportunity → Closed Won
2. *Market Analysis*: Identify trending industries and funding stages for 2026
3. *Performance Review*: Monitor individual/team KPIs vs monthly targets
4. *Client Presentations*: Use live dashboard during investor/BD meetings

## 🔮 Future Enhancements

- [ ] Integrate with HubSpot/Salesforce API for live CRM data
- [ ] Add ML-based lead scoring using scikit-learn
- [ ] Email automation for follow-ups via SMTP
- [ ] User authentication for team access

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a PR for improvements.

1. Fork the project
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

## 📧 Contact

*Remsha Ansari* - Business Development Analyst
- *Dashboard*: [remsha-funded2026.streamlit.app](https://remsha-funded2026.streamlit.app)

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
*Built with ❤️ for Business Development | Data-Driven Decisions for 2026*
