# SG Miles Credit Card Tracker

A single-page web app that helps you find the best miles-earning credit cards in Singapore. Compare cards across banks and spending categories to maximise your miles per dollar (mpd).

## Features

- **Search by Category** – Filter cards by name, bank, or spending category with sortable MPD columns
- **My Cards** – Save the cards you own and filter results to show only your cards across all categories
- **🤖 Card Advisor (AI)** – Describe a spending scenario and get personalised AI recommendations ranked by miles earned, powered by Cloudflare Workers AI (Llama 3.1)
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

## Getting Started

Open `index.html` in any modern browser — no build step or server required. The Card Advisor feature requires the deployed Cloudflare Worker endpoint.

## License

MIT
