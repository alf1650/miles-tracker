# SG Miles Credit Card Tracker

A single-page web app that helps you find the best miles-earning credit cards in Singapore. Compare cards across banks and spending categories to maximise your miles per dollar (mpd).

## Features

- **Search by Category** – Filter cards by name, bank, or spending category with sortable MPD columns
- **My Cards** – Save the cards you own and filter results to show only your cards across all categories
- **🤖 Card Advisor (AI)** – Describe a spending scenario and get personalised AI recommendations ranked by miles earned, powered by Cloudflare Workers AI
- **Remember Me** – Card selections persist across sessions via localStorage
- **Bank Badges** – Visual indicators for each issuing bank
- **Responsive Design** – Works on desktop and mobile

## Supported Banks

AMEX, BOC, Chocolate, Citi, DBS, HSBC, Maybank, OCBC, StanChart, UOB

## Project Structure

```
index.html          # Main application (HTML/CSS/JS, self-contained)
```

The Card Advisor backend is a separate Cloudflare Worker — see the `miles-tracker-worker/` directory in the parent repo.

## November 2026 Data Refresh

Checked MileLion on **7 November 2026**. Its category guide and the stored guide snapshot still show **8 October 2026**; newer articles and AMEX's issuer pages provide the following updates:

| Card | Updated rule |
| --- | --- |
| AMEX KrisFlyer Credit Card | Local and FCY earn rates increased from 1.1 to **1.3 mpd**, effective 1 November. |
| AMEX KrisFlyer Ascend | Local and FCY earn rates increased from 1.2 to **1.5 mpd**, effective 1 November. |
| AMEX PPS / Solitaire PPS | Local earn rates increased to **1.5 mpd**. FCY earns 1.5 mpd on the first S$3,800 per calendar month, then 2 / 2.4 mpd respectively on the excess only. PPS membership is required. |
| DBS Vantage | Local earn rate reduced from 1.5 to **1.4 mpd**, effective 2 November. FCY remains 2.2 mpd. |
| Maybank Horizon Visa Signature | **3.2 mpd** on CNY/HKD/IDR/JPY/MYR/TWD/KRW/THB spending from 1 November 2026 to 31 January 2027; other FCY remains 2.8 mpd. Requires S$800 eligible spending per calendar month; otherwise 1.2 mpd. |

Existing government-services, private-hospital and Chubb-only insurance entries use the revised AMEX base rates without changing their eligibility restrictions. AMEX's 2 mpd SIA/Scoot entries are unchanged. Local and FCY entries were added for the existing PPS cards, and FCY entries for KrisFlyer/Ascend.

The tables and both advisors share `DATA` in [index.html](./index.html), so no Worker data deployment is needed. Maybank's conditional 3.2 mpd promotion and PPS's higher FCY tiers are shown in the rate display and remarks; sorting and advisor estimates retain 2.8 and 1.5 mpd respectively rather than assuming currency eligibility or prior monthly spending. These are conservative estimates, not a full promotion/threshold calculator.

Sources:

- [AMEX KrisFlyer earn-rate increase](https://milelion.com/2026/11/03/amex-krisflyer-credit-card-increases-earn-rates-to-1-3-mpd/)
- [AMEX Ascend changes, including PPS earn-rate comparisons](https://milelion.com/2026/11/02/nerfed-amex-krisflyer-ascend-boosts-earn-rate-to-1-5-mpd-but-removes-hilton-free-night-voucher/)
- [AMEX PPS issuer page](https://www.americanexpress.com/sg/credit-cards/singapore-airlines-pps-club/) and [Solitaire PPS issuer page](https://www.americanexpress.com/sg/credit-cards/singapore-airlines-solitaire-pps-card/)
- [DBS Vantage changes effective in November](https://milelion.com/2026/09/29/dbs-vantage-card-cuts-local-earn-rates-to-1-4-mpd-adds-free-limo-rides-and-annual-fee-waiver/)
- [Maybank Horizon November–January promotion](https://milelion.com/2026/10/31/maybank-horizon-visa-signature-offering-3-2-mpd-on-selected-fcy-spend-2/)

Other November news does not change the unconditional card earn rates tracked here: DBS/HSBC welcome offers, AMEX Accor status, DBS Treasures limo/fee-waiver benefits, Ascend's removal of Hilton benefits, [targeted OCBC 8% FCY cashback](https://milelion.com/2026/11/01/ocbc-credit-cards-offering-8-cashback-on-fcy-spending-with-very-few-exclusions/), and [Pelago's additional Kris+ miles](https://milelion.com/2026/11/05/earn-up-to-12-mpd-on-pelago-bookings-for-november-2026/). Targeted cashback and merchant/platform miles are not added to general card rates.

The scheduled [MileLion checker](./scripts/check_milelion.py) compares only the category guide; it does not monitor individual articles or automatically apply effective-dated changes. The snapshot is deliberately unchanged because the live guide has not changed.

## Getting Started

Open `index.html` in any modern browser — no build step or server required. The Card Advisor feature requires the deployed Cloudflare Worker endpoint.

## License

MIT
