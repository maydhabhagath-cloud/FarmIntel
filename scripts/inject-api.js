const fs = require('fs');
const path = require('path');
const file = path.join(process.cwd(), 'index.html');
let html = fs.readFileSync(file, 'utf8');
const tag = '<script src="/frontend-api.js"></script>';
if (!html.includes('frontend-api.js')) {
  html = html.replace('</body>', `  ${tag}\n</body>`);
  fs.writeFileSync(file, html, 'utf8');
  console.log('FarmIntel API bridge injected into index.html');
} else {
  console.log('FarmIntel API bridge already present');
}
