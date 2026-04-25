# TrendScope — Time Series Dashboard

Interactive dashboard for visualising Actual vs Forecasted time-series data across multiple sections (PT, ED, Oven), subfolders, and parameters.

---

## 📁 How to Add Your Data

Your CSV files must follow this exact structure:

```
data/
├── PT/
│   └── DI_Water/
│       ├── Conductivity.csv
│       └── Spray_Flow.csv
├── ED/
│   └── YourSubFolder/
│       └── YourParameter.csv
└── Oven/
    └── YourSubFolder/
        └── YourParameter.csv
```

Each CSV must have exactly **3 columns**:
```
timestamp,actual,forecasted
2026-04-25 01:03:04,5.9063,5.331639
2026-04-25 01:03:14,5.8342,5.498522
```

---

## 🖥️ Running Locally

### Step 1 — Install Python
Download Python 3.10+ from https://www.python.org/downloads/

### Step 2 — Install dependencies
Open a terminal/command prompt in the project folder and run:
```bash
pip install -r requirements.txt
```

### Step 3 — Run the app
```bash
python app.py
```

### Step 4 — Open in browser
Go to: http://localhost:5000

---

## 🌐 Free Online Deployment (Render.com)

Deploy for **free** with no credit card needed.

### Step 1 — Create a GitHub account
Go to https://github.com and sign up (free).

### Step 2 — Create a new repository
1. Click the **+** icon → **New repository**
2. Name it: `timeseries-dashboard`
3. Make it **Public**
4. Click **Create repository**

### Step 3 — Upload your project files
1. On the repository page, click **uploading an existing file**
2. Drag and drop ALL files from this project folder
3. Click **Commit changes**

### Step 4 — Deploy on Render
1. Go to https://render.com and sign up (free, use GitHub login)
2. Click **New +** → **Web Service**
3. Connect your GitHub repository
4. Fill in these settings:
   - **Name**: timeseries-dashboard (or anything you like)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free
5. Click **Create Web Service**
6. Wait ~2 minutes — Render gives you a live URL like:
   `https://timeseries-dashboard.onrender.com`

**That's it!** Share the URL with anyone.

---

## 📝 Notes

- The free Render plan sleeps after 15 minutes of inactivity. First load after sleep takes ~30 seconds.
- Add as many subfolders and CSV files as you want — the app auto-discovers them.
- Sections (PT, ED, Oven) are fixed but subfolders and parameters are fully dynamic.

---

## 🛠️ Customising Sections

To rename or add sections (e.g., add a 4th section "Paint"), edit `app.py`:

```python
SECTIONS = ['PT', 'ED', 'Oven', 'Paint']
```

Then create the `data/Paint/` folder and update the icons/subtitles in `templates/index.html`.
