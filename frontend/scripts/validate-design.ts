import { chromium } from "playwright";
import * as path from "path";
import * as fs from "fs";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const PROJECT_ROOT = path.resolve(__dirname, "..", "..");
const OUTPUT_DIR = path.join(PROJECT_ROOT, "docs", "validation");
const REFERENCE_HTML = `file:///${path.join(PROJECT_ROOT, "code.html").replace(/\\/g, "/")}`;
const DEV_URL = "http://localhost:3000";

async function main() {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
  const browser = await chromium.launch();

  console.log(`Reference: ${REFERENCE_HTML}`);

  // ── Screenshot 1: code.html (referencia) ──
  const refCtx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const refPage = await refCtx.newPage();
  await refPage.goto(REFERENCE_HTML);
  await refPage.waitForTimeout(2500);
  await refPage.screenshot({ path: path.join(OUTPUT_DIR, "reference-code-html.png"), fullPage: true });
  await refCtx.close();
  console.log("1/4 reference-code-html.png");

  // ── Screenshot 2: Next.js frontend ──
  const devCtx = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const devPage = await devCtx.newPage();
  await devPage.goto(DEV_URL, { timeout: 15000 });
  await devPage.waitForTimeout(2500);
  await devPage.screenshot({ path: path.join(OUTPUT_DIR, "implementation-nextjs.png"), fullPage: true });
  await devCtx.close();
  console.log("2/4 implementation-nextjs.png");

  // ── Screenshot 3: Mobile reference ──
  const refMobile = await browser.newContext({ viewport: { width: 375, height: 812 } });
  const refMPage = await refMobile.newPage();
  await refMPage.goto(REFERENCE_HTML);
  await refMPage.waitForTimeout(2000);
  await refMPage.screenshot({ path: path.join(OUTPUT_DIR, "reference-mobile.png"), fullPage: true });
  await refMobile.close();
  console.log("3/4 reference-mobile.png");

  // ── Screenshot 4: Mobile implementation ──
  const devMobile = await browser.newContext({ viewport: { width: 375, height: 812 } });
  const devMPage = await devMobile.newPage();
  await devMPage.goto(DEV_URL, { timeout: 15000 });
  await devMPage.waitForTimeout(2000);
  await devMPage.screenshot({ path: path.join(OUTPUT_DIR, "implementation-mobile.png"), fullPage: true });
  await devMobile.close();
  console.log("4/4 implementation-mobile.png");

  await browser.close();
  console.log(`\n✅ Done — ${OUTPUT_DIR}/`);
}

main();
