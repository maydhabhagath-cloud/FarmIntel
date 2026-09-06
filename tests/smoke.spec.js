const { test, expect } = require('@playwright/test');

test.describe('FarmIntel smoke tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://127.0.0.1:8080/');
  });

  test('page loads', async ({ page }) => {
    await expect(page).toHaveTitle(/FarmIntel/);
  });

  test('navigation works', async ({ page }) => {
    await page.click('button[data-view="markets"]');
    await expect(page.locator('#markets')).toBeVisible();
    await page.click('button[data-view="dashboard"]');
    await expect(page.locator('#dashboard')).toBeVisible();
  });

  test('add crop lot opens and validates', async ({ page }) => {
    await page.click('#addLotBtn');
    await expect(page.locator('#lotCrop')).toBeVisible();
    await page.click('button[type="submit"]');
    await page.selectOption('#lotCrop', 'Tomato');
    await page.fill('#lotQty', '10');
    await page.selectOption('#lotUnit', 'q');
    await page.fill('#lotDate', '2026-09-15');
    await page.selectOption('#lotQuality', 'Grade A');
    await page.click('button[type="submit"]');
    await expect(page.locator('#lotsList')).toContainText('Tomato');
  });

  test('market intelligence renders', async ({ page }) => {
    await page.click('button[data-view="markets"]');
    await expect(page.locator('#marketsTableArea')).toBeVisible();
    await expect(page.locator('table')).toContainText('Net realizable');
  });

  test('sell smart recommendation renders', async ({ page }) => {
    await page.click('button[data-view="sell"]');
    await expect(page.locator('#recScore')).toBeVisible();
  });

  test('buyer matches and offers render', async ({ page }) => {
    await page.click('button[data-view="buyers"]');
    await expect(page.locator('#buyersArea')).toBeVisible();
    await page.click('button[data-view="offers"]');
    await expect(page.locator('#offersArea')).toBeVisible();
  });

  test('accept offer changes state', async ({ page }) => {
    await page.click('button[data-view="offers"]');
    const accept = page.locator('button[data-action="accept-offer"]').first();
    if (await accept.count() === 0) test.skip();
    await accept.click();
    await expect(page.locator('#offersArea')).toContainText(/accepted/i);
  });
});
