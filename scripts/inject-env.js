const fs = require('fs');
const path = require('path');

const appJsPath = path.join(__dirname, '../frontend/app.js');
const appJs = fs.readFileSync(appJsPath, 'utf-8');
const apiBase = process.env.API_BASE_URL || 'http://127.0.0.1:8000';
const updated = appJs.replace('"%%API_BASE%%"', `"${apiBase}"`);
fs.writeFileSync(appJsPath, updated);
console.log(`✓ Injected API_BASE=${apiBase}`);
