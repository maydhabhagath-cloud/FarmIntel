# FarmIntel — Smart Market Intelligence for Farmers

FarmIntel is a prototype for **SIH26132: Strengthening market linkages and price discovery for farmers**.

## Core idea

FarmIntel helps farmers compare selling opportunities using more than the headline price. The prototype considers indicative offered price, estimated logistics cost, demand, quantity and quality fit to surface a **Net Realizable Price** and an explainable Sell Smart recommendation.

## Prototype modules

- Farmer Dashboard
- My Crop Lots
- Market Intelligence
- Sell Smart recommendation
- Buyer Matches
- Offers
- Buyer Portal
- FPO aggregation view
- Logistics view
- Add Crop Lot with validation

## Important demo limitation

This repository contains a demonstration prototype with mock data. It does not claim live government market feeds, real buyer verification, guaranteed price forecasts, certified quality grading, real payments, or production logistics integrations.

## Local run

Install dependencies and start the static server:

```bash
npm install
npm run start
```

Open `http://127.0.0.1:8080/`.

For Playwright smoke tests:

```bash
npx playwright install
npm test
```

## Deployment

The repository contains a GitHub Actions Pages workflow at `.github/workflows/deploy-pages.yml`. It is configured to deploy the static site when changes reach `main`, subject to GitHub Pages being enabled for the repository.

## Technology

- Semantic HTML
- CSS
- Vanilla JavaScript
- GitHub Pages
- Playwright for smoke testing

## SIH

**Problem ID:** SIH26132  
**Theme:** Agriculture, FoodTech & Rural Development  
**Category:** Software
