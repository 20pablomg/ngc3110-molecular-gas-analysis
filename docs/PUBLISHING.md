# Publishing this repository on GitHub

1. Confirm that **you own the source code** and that your institution and collaborators permit its release. The raw IRAM observations, ALMA FITS files, SSC maps, full thesis PDF and third-party images are not part of this distribution.
2. Read [REPRODUCIBILITY.md](REPRODUCIBILITY.md). Python code has been syntax-checked and the table converter tested, but the observational pipeline was not rerun; some original scientific checks remain unresolved. Do **not** claim complete reproducibility.
3. Inspect the selected original output figures embedded in notebooks, and confirm you have permission to publish those derived visualizations. Remove them if permissions are uncertain.
4. Download/extract the project ZIP and open a terminal in the extracted `ngc3110-molecular-gas-analysis` directory. Create a **new empty private** GitHub repository of the same name (do not automatically initialize it with README).
5. With Git installed, run:

   ```bash
   git init
   git add .
   git status
   git commit -m "Publish scientific analysis source and documentation"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ngc3110-molecular-gas-analysis.git
   git push -u origin main
   ```

   Authenticate through your GitHub account/Git Credential Manager; never commit credentials.
6. Check GitHub's notebook previews and the rendered README. Confirm no `.fits`, `.30m`, private `.dat`, personal paths, sensitive metadata or unauthorized figures were uploaded. If needed, remove any questionable material from the repository **before** making it public; merely deleting a file after it was committed may leave it in Git history.
7. Once checked, go to **Settings → General → Danger Zone → Change repository visibility → Public**. Pin it on your profile and link it from your CV and LinkedIn.

No license is included pending a rights review. A public GitHub repository does **not** by itself grant everyone permission to reuse its code.
