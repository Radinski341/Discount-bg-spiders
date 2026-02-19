# Discount BG Spiders

Scrapy-based web scraping project for collecting **discounted products** from Bulgarian e-commerce websites.

This repository powers the product-ingestion side of **Discount BG** - a Bulgarian-market dropshipping platform focused on discounted offers.

## What This Project Does

- Crawls selected online stores
- Extracts products with active discounts
- Normalizes prices and discount fields in a shared pipeline
- Exports ready-to-use JSON datasets for downstream import in the Discount BG commerce stack

## Target Websites

Production-oriented spiders in this repo:

- `emag` (`emag.bg`)
- `emag2` (`emag.bg`, second category set)
- `magazinabg` (`magazinabg.com`)
- `makasa` (`makasa.org`)
- `praktiker` (`praktiker.bg`)

Additional spiders:

- `testspider` (single product debugging on eMAG)
- `amazon` (experimental/non-BG source, includes debug HTML capture)

## Tech Stack

- Python 3
- Scrapy
- BeautifulSoup (`beautifulsoup4`)
- Requests

## Project Structure

```text
Discount-bg-spiders/
├── scrapy.cfg
├── discountbg/
│   ├── settings.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── spiders/
│   │   ├── emag.py
│   │   ├── emag2.py
│   │   ├── magazinabg.py
│   │   ├── makasa.py
│   │   ├── praktiker.py
│   │   ├── amazon.py
│   │   └── testspider.py
│   ├── data/                  # main exported JSON files
│   └── php/normalize-json.py  # JSON chunking helper script
└── README.md
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/Discount-bg-spiders.git
cd Discount-bg-spiders
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install scrapy beautifulsoup4 requests
```

## Running Spiders

From the project root, run:

```bash
scrapy crawl <spider_name> -O discountbg/data/<output_file>.json
```

Examples:

```bash
scrapy crawl emag -O discountbg/data/emag.json
scrapy crawl emag2 -O discountbg/data/emag2.json
scrapy crawl magazinabg -O discountbg/data/magazinabg.json
scrapy crawl makasa -O discountbg/data/makasa.json
scrapy crawl praktiker -O discountbg/data/praktiker.json
```

Quick debug run:

```bash
scrapy crawl testspider -O discountbg/data/test.json
```

## Where the Data Goes

- Main output is written to `discountbg/data/*.json` when you use `-O ...`.
- Existing example exports are already present in `discountbg/data/`.
- The `amazon` spider stores failed page snapshots in `discountbg/spiders/debug_html/` for troubleshooting.

## Data Format (Short)

Each product is exported as a JSON object (array item), typically containing:

- `website`, `website-url`, `website-id`
- `product-url`, `title`
- `old-price`, `new-price`, `discount-percent`
- `images` (pipe-separated URLs)
- `categories`
- `description-html`
- `is-product-choice` (variant/option item flag)

## Processing and Normalization

`discountbg/pipelines.py` standardizes values during crawl:

- Cleans and converts price fields to numbers
- Cleans discount percentage values
- Calculates discount where needed
- Applies spider-specific adjustments (for example: Amazon and Makasa formatting cases)

## Integration With Discount BG

This repository acts as the **data acquisition layer** for Discount BG:

1. Scrapers collect discounted product data from source stores.
2. Data is normalized into a common schema.
3. JSON exports are consumed by the downstream Discount BG e-commerce project.

The helper script `discountbg/php/normalize-json.py` can split large JSON files into smaller chunks (250 records per file) for easier import workflows.

## Important Notes

- `settings.py` currently includes a `SCRAPEOPS_API_KEY` and middleware setup for rotating browser headers.
- Some scripts/spiders use hardcoded absolute paths or large category lists; update them to your environment as needed.
- Respect website terms of service and applicable legal requirements when scraping.

---

If you are reviewing this repository from my GitHub profile: this is the real ingestion engine behind Discount BG’s discount-focused catalog pipeline for the Bulgarian market.
