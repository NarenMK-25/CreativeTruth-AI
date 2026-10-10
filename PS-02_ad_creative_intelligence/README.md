# CreativeTruth AI 📈
### Beyond Clicks. Beyond Guesswork.

CreativeTruth AI is an AI-powered advertising intelligence platform built for the **PS-02 Ad Creative Intelligence Challenge**.

Marketers often know *which* ads perform well, but rarely understand *why* beyond instinct and guesswork. CreativeTruth AI bridges this gap by automatically extracting visual attributes—known as **Creative DNA**—from advertising images and combining them with campaign performance data to uncover statistically supported, evidence-first marketing insights.

The platform helps marketers compare competing brands, identify patterns in creative performance, detect misleading engagement signals, and generate actionable recommendations for future campaigns.

## ✨ Key Features

- **🛡️ Strict Integrity Gate**  
  Automatically validates image formats and relevance to prevent corrupted or irrelevant assets from contaminating the analysis dataset.

- **🧬 Creative DNA Extraction**  
  Uses OpenCV to extract visual attributes such as brightness, contrast, and visual complexity through edge-density analysis—without requiring manual labeling.

- **📊 Competitive Intelligence**  
  Compares key advertising performance metrics, including average Click-Through Rate (CTR), Conversion Rate (CVR), and Return on Ad Spend (ROAS), across competing brands.

- **⚖️ Pattern Discovery & Evidence Debt**  
  Evaluates relationships between visual attributes and campaign performance using statistical tests, including t-tests. Findings are classified transparently as:
  - `SUPPORTED`
  - `PRELIMINARY`
  - `NO CLEAR ASSOCIATION`
  - `INSUFFICIENT DATA`

  Reports include effect sizes and sample sizes to help users interpret findings responsibly, without relying on fabricated confidence scores.

- **⚠️ Creative Illusion Detector**  
  Identifies ads that generate high engagement (high CTR) but have comparatively low conversion rates (CVR), highlighting a potential gap between clicks and actual conversions.

- **🚀 Launch Window Advisor**  
  Evaluates available historical demand and seasonality data to help identify promising campaign launch windows.

- **📝 Creative Brief Generator**  
  Converts statistical findings into actionable, human-readable recommendations for design teams and proposes counterfactual experiments, including A/B testing ideas.

## 🛠️ Tech Stack

### Backend — Analysis Engine & API

| Technology | Purpose |
|---|---|
| Python 3.x | Core programming language |
| Flask | Lightweight backend API server |
| Pandas | Data ingestion, cleaning, and manipulation |
| NumPy | Numerical computations |
| OpenCV (`opencv-python-headless`) | Image processing and visual attribute extraction |
| SciPy | Statistical analysis and significance testing |

### Frontend — Interactive Dashboard

| Technology | Purpose |
|---|---|
| HTML5 | Dashboard structure |
| Vanilla JavaScript | Frontend interactions and API communication |
| Tailwind CSS | Responsive UI styling |
| Chart.js | Interactive charts and data visualization |

## 📂 Project Structure

```text
CreativeTruth_AI/
├── server.py                       # Flask server and API routing
├── engine.py                       # Core logic: image analysis, metrics, statistics
├── tests.py                        # Automated tests for metric validation
├── requirements.txt                # Python dependencies
├── templates/
│   └── index.html                  # Frontend dashboard
└── PS-02_ad_creative_intelligence/
    ├── creative_performance.csv    # Campaign performance data
    └── creatives/                  # PNG/JPG advertisement images
```

> **Important:** Place the complete `PS-02_ad_creative_intelligence` dataset folder in the project root. Ensure that `creative_performance.csv` and the `creatives/` directory follow the expected structure.

## 🚀 Installation & Setup

### Prerequisites

- Python 3.x
- Git
- The PS-02 Ad Creative Intelligence dataset

### 1. Clone the Repository

Replace `YOUR_USERNAME` with your GitHub username or the appropriate repository owner.

```bash
git clone https://github.com/YOUR_USERNAME/CreativeTruth_AI.git
cd CreativeTruth_AI
```

### 2. Add the Dataset

Place the entire `PS-02_ad_creative_intelligence` folder inside the project root.

Verify that the directory structure looks like this:

```text
CreativeTruth_AI/
└── PS-02_ad_creative_intelligence/
    ├── creative_performance.csv
    └── creatives/
        ├── ad_001.jpg
        ├── ad_002.png
        └── ...
```

Ensure that the image filenames and CSV references match the format expected by the application.

### 3. Create a Virtual Environment (Recommended)

Create a virtual environment to isolate project dependencies.

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 5. Run the Application

Start the Flask backend server:

```bash
python server.py
```

Once the server starts successfully, open your browser and navigate to:

**http://127.0.0.1:5000**

### 6. Analyze the Dataset

1. Open the CreativeTruth AI dashboard.
2. Verify that the dataset is available and loaded correctly.
3. Click **Run Complete Analysis** in the dashboard sidebar.
4. Allow the application to validate the images, extract Creative DNA features, calculate performance metrics, and perform statistical analysis.
5. Review the resulting competitive comparisons, evidence classifications, and recommendations.

## 🧪 Testing

CreativeTruth AI includes an automated test suite to verify mathematical calculations and the Creative Illusion Detector's behavior.

Run the tests with:

```bash
python -m pytest tests.py
```

Review the test results to confirm that the tested functionality behaves as expected.

## 📊 Key Performance Metrics

The platform uses advertising performance metrics to compare campaigns and interpret creative effectiveness.

| Metric | Meaning |
|---|---|
| **CTR — Click-Through Rate** | Percentage of impressions that result in clicks |
| **CVR — Conversion Rate** | Percentage of clicks or other defined eligible interactions that result in conversions |
| **ROAS — Return on Ad Spend** | Revenue attributed to advertising divided by advertising spend |

Metric calculations depend on the definitions and fields available in the supplied dataset. Comparisons should account for sample sizes and differences in campaign conditions.

## 🔬 Evidence-First Analysis

CreativeTruth AI is designed to distinguish observed patterns from conclusions that the available data cannot support.

- **Supported:** Evidence meets the application's defined criteria for a supported finding.
- **Preliminary:** A potentially useful pattern exists, but additional evidence is needed.
- **No Clear Association:** The analysis does not establish a clear relationship.
- **Insufficient Data:** The available observations are inadequate for a meaningful assessment.

Statistical significance alone does not establish causation. Findings should be interpreted alongside effect sizes, sample sizes, uncertainty, and relevant campaign conditions.

## 🎯 Project Objective

CreativeTruth AI aims to move advertising analysis beyond basic performance rankings by connecting **what an advertisement looks like** with **how its campaign performs**.

By combining image analysis, competitive benchmarking, statistical evaluation, and actionable recommendations, the platform helps marketers make more informed creative decisions.

**CreativeTruth AI — Beyond Clicks. Beyond Guesswork.**

---

*Developed for the PS-02 Ad Creative Intelligence Challenge.*
