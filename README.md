A business analyst practice project exploring the Kaggle "Superstore" sales dataset:
trends, segmentation and growth analysis.

## Project structure

| File | Purpose |
|---|---|
| `overall_performance.ipynb` | overall exploratory analysis, monthly and yearly trends + plots. |
| `segment_analysis.ipynb` | analysis by region, categories/sub-categories and top customers |
| `trend_timing.ipynb` | seasonality, fastest/slowest growth by region and category, shipping delays |
| `forecasting.ipynb` | simple monthly sales forecast (Holt-Winters exponential smoothing) |
| `eda.py` | Script version / scratch space for quick checks. |
| `metadata.py` | Data dictionary as a Python dict (`METADATA`) - column names, descriptions, and types. |
| `data/supermarket_sales.csv` | The dataset (not tracked in git - see below). |
| `requirements.txt` | Python dependencies. |

## Dataset

Source: [Kaggle - rohitsahoo/sales-forecasting](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting)
(the "Superstore" sales dataset). One row = one line item within an order.

The CSV isn't committed to this repo. To get it:

```bash
kaggle datasets download rohitsahoo/sales-forecasting --unzip
```

See `metadata.py` for a full column-by-column data dictionary.

## Setup

```bash
pip install -r requirements.txt
```

Requires Kaggle API credentials configured (`KAGGLE_USERNAME`/`KAGGLE_KEY` or
`KAGGLE_API_TOKEN` as an environment variable) if you need to re-download the data.

## What's covered so far

- Data cleaning: null checks, date type conversion, deduplication
- Monthly and yearly sales trends, with a fitted trend line
- Month-over-month and year-over-year growth rates
- Sales segmentation by region, category, sub-category, and top customers
- Seasonality (sales by month-of-year), fastest/slowest growing region and category
- Shipping delay analysis by ship mode and region
- A simple 3-month sales forecast, with caveats

As a next step, I plan to package the best charts and findings into a one-page summary
or dashboard.
