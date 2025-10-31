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
The website is configured to use the original Bible Toolbox logo. To add it:

1. Download the logo from the Wayback Machine:
   - Visit: https://web.archive.org/web/20010401083600im_/http://www.authenticwalk.com/bibletoolbox/images/bible-toolbox-bottom.gif
   - Save the image as `logo.gif` in this directory (`docs/logo.gif`)
   - Or use your browser to save it directly

2. Alternative download methods:
   ```bash
   # Using wget with user agent
   wget -O docs/logo.gif --user-agent="Mozilla/5.0" "https://web.archive.org/web/20010401083600im_/http://www.authenticwalk.com/bibletoolbox/images/bible-toolbox-bottom.gif"

   # Or download manually from browser and place in docs/
   ```

The HTML and CSS are already configured to display the logo at 40px height next to the site title.

### Copyright Date
The copyright has been updated to reflect the original date: **2001-2025**
