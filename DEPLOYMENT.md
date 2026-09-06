# FarmIntel deployment checklist

1. Merge `feature/sih-upgrade` into `main`.
2. In GitHub repository Settings → Pages, select **GitHub Actions** as the source if Pages is not already enabled.
3. The `Deploy FarmIntel to GitHub Pages` workflow runs on pushes to `main`.
4. Wait for the deployment job to complete successfully.
5. GitHub will expose the project site URL from the Pages deployment environment.
6. A custom domain can be configured later after purchasing and controlling the domain; do not add a CNAME until DNS is configured.
