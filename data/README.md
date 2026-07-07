# Data Sources

Raw datasets are not committed to this repository. Many datasets are hosted on
Kaggle and may require a Kaggle account, API token, or manual download.

Place raw files under:

```text
data/raw/
```

Place cleaned or derived files under:

```text
data/processed/
```

The notebooks should not assume that raw data files are already present. When a
file is missing, the notebook should print a clear instruction with the expected
download link and local path.

## Kaggle Setup

1. Create or sign in to a Kaggle account.
2. Create an API token from your Kaggle account settings.
3. Save `kaggle.json` in the location required by your operating system.
4. Install the course environment with `uv sync`.
5. Download the dataset manually or with the Kaggle CLI through `uv run`.

Example:

```powershell
uv run kaggle competitions download -c titanic -p data/raw/titanic
uv run kaggle competitions download -c house-prices-advanced-regression-techniques -p data/raw/house-prices
uv run kaggle competitions download -c bike-sharing-demand -p data/raw/bike-sharing
uv run kaggle datasets download -d unsdsn/world-happiness -p data/raw/world-happiness
uv run kaggle datasets download -d zhangluyuan/ab-testing -p data/raw/ab-testing
```

Some Kaggle competitions require accepting competition rules in the browser
before the CLI download succeeds.

## Recommended Course Datasets

| Dataset | Course use | Link |
| --- | --- | --- |
| Titanic | Conditional probability, classification framing, risk communication | https://www.kaggle.com/c/titanic |
| House Prices | Continuous variables, estimation, regression-oriented capstone option | https://www.kaggle.com/c/house-prices-advanced-regression-techniques |
| Bike Sharing Demand | Count/time features, Poisson-style thinking, prediction and uncertainty | https://www.kaggle.com/c/bike-sharing-demand |
| World Happiness Report | Estimation, intervals, group comparisons, communication | https://www.kaggle.com/datasets/unsdsn/world-happiness |
| A/B Testing | Hypothesis testing, proportions, experiment interpretation | https://www.kaggle.com/datasets/zhangluyuan/ab-testing |

## Data Ethics And Licensing

Students must cite every dataset and follow the license or competition rules
for each source. Capstone reports should include a short data ethics note
covering privacy, representation, known biases, and limitations of the dataset.
