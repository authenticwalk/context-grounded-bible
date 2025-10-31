# Website

This directory contains the static website for Context-Grounded Bible, hosted via GitHub Pages.

## Local Development

To test the website locally, you can use any simple HTTP server:

```bash
# Using Python
cd docs
python -m http.server 8000

# Using Node.js
npx serve docs

# Using PHP
cd docs
php -S localhost:8000
```

Then visit `http://localhost:8000` in your browser.

## GitHub Pages Setup

This site is configured to be served from the `/docs` directory on the main branch.

To enable GitHub Pages:
1. Go to your repository settings
2. Navigate to "Pages" in the left sidebar
3. Under "Source", select "Deploy from a branch"
4. Select the main branch and `/docs` folder
5. Click "Save"

Your site will be available at: `https://authenticwalk.github.io/context-grounded-bible/`

## Updating

### Logo
To add the original mybibletoolbox.com logo:
1. Place the logo image in this directory (e.g., `logo.png`)
2. Update the logo section in `index.html`:
   ```html
   <div class="logo">
       <img src="logo.png" alt="Context-Grounded Bible" height="40">
       <h1>Context-Grounded Bible</h1>
   </div>
   ```
3. Add CSS styling in `style.css` if needed

### Copyright Date
Once you confirm the original date from the Wayback Machine, update the footer in `index.html`:
```html
<p>&copy; YYYY-2025 Context-Grounded Bible Project</p>
```

Replace YYYY with the original year from mybibletoolbox.com (appears to be 1997 based on placeholder).
