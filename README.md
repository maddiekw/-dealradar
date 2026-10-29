# DealRadar — personal deal discovery

DealRadar can show **real community-reported listings** collected from Slickdeals RSS feeds. It does **not** scrape or verify retailer checkout prices, calculate reliable discounts without comparison prices, or confirm local clearance inventory.

## Start locally

Run `python update_deals.py` (requires internet), then `python -m http.server 8000` and open `http://localhost:8000`. Browser `file://` previews may block fetch requests.

## Publish and refresh automatically

1. Create a GitHub repository and upload **the contents of this folder**, including `.github/workflows/refresh.yml`.
2. Enable GitHub Pages for the repository (Settings → Pages → Deploy from branch → main/root).
3. Run the **Refresh public deal feeds** workflow once under Actions to create `deals.json`.
4. The workflow is configured to check the feeds about every three hours. GitHub scheduled jobs may be delayed or paused. Pages deployment may take a few minutes.
5. Open your published Pages URL in Safari and use Share → Add to Home Screen.

This is a publicly reachable static website if hosted on GitHub Pages, even if you intend to use it personally. Avoid storing sensitive notes in the website. Bookmarks/manual deals remain in each browser's localStorage, not synced.

Feed terms and availability can change. The updater preserves existing data when all feeds fail. Store-specific local inventory and genuine price-error verification require additional authorized data sources.
