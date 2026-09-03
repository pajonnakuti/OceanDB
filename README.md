# INCOIS ARGO CORE + BGC Real Data Explorer (GitHub Pages Edition)

Interactive Web Application & SQL Console for **6 Real INCOIS ARGO Floats** operating in the **Arabian Sea** and **Bay of Bengal**.

---

## 🚀 Deployment Instructions for GitHub Pages (`github.io`)

Follow these 3 simple steps to publish this repository live on GitHub Pages:

### Step 1: Initialize Git & Push to GitHub
Open your terminal in this folder (`D:\O\2026\Teaching`) and run:

```bash
git init
git add .
git commit -m "Deploy INCOIS ARGO Web App to GitHub Pages"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
git push -u origin main
```

*(Replace `YOUR_GITHUB_USERNAME` and `YOUR_REPOSITORY_NAME` with your actual GitHub account and repository name).*

---

### Step 2: Enable GitHub Pages in Repository Settings
1. Go to your GitHub repository on [github.com](https://github.com).
2. Click **Settings** ⚙️ at the top right of your repository.
3. Click **Pages** in the left sidebar menu under *Code and automation*.
4. Under **Build and deployment**:
   - **Source**: Select **GitHub Actions** (or select `Deploy from a branch` -> `main` / `/ (root)`).
5. Click **Save**.

---

### Step 3: View Live Website
Your application will automatically build and publish live at:
```
https://YOUR_GITHUB_USERNAME.github.io/YOUR_REPOSITORY_NAME/
```

---

## 📄 Application Features
- **Client-Side SQL Engine**: Powered by AlaSQL to run complex SQL queries directly inside any browser with zero backend server required.
- **Interactive Single Profile Selector**: Dynamically filter by WMO ID and Cycle Number.
- **Geographic Station Map**: Powered by Leaflet.js with dark ocean basemap and custom profile markers.
- **Vertical CTD & BGC Depth Profiles**: Plotly.js line plots for Temperature, Salinity, Dissolved Oxygen ($O_2$), and Chlorophyll-a ($Chl\text{-}a$).
- **Streamlit WebAssembly Option**: Access `stlite.html` for Streamlit compiled to Pyodide Wasm directly in the browser!
