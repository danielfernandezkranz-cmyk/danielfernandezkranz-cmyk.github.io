# danielfernandezkranz.com

Personal academic web site of Daniel Fernández-Kranz, published with GitHub Pages
from the `docs/` folder of this repository.

## How to update the site

1. Edit the content in `data/`:
   - `site.json` – intro text, news items, contact details and profile links
   - `working_papers.json` – working papers (title, status, co-authors, abstract, links)
   - `publications.json` – published papers, other publications, conferences
   - `teaching.json` – courses and teaching awards
   - `cv.json` – the CV summary shown on the CV page
   - `photo.jpg` – the portrait shown on the home page
2. To update the CV, replace `CV Daniel Fernandez-Kranz.pdf` in the root folder.
3. Run `python build.py` (Python 3, no extra packages needed). It rebuilds `docs/`.
4. Commit and push to `main`. GitHub Pages publishes `docs/` automatically.
