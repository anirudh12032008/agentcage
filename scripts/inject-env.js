const fs = require('fs');
const appJs = fs.readFileSync('frontend/app.js', 'utf-8');
const updated = appJs.replace('const API_BASE = "%%API_BASE%%"', `const API_BASE = "${process.env.API_BASE_URL}"`);
fs.writeFileSync('frontend/app.js', updated);
