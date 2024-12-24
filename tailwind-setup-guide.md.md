## **Setting Up Node.js and Tailwind**

1. **Install Node.js Dependencies:**
   In the project root (where `package.json` is located):
   ```bash
   npm install
   ```

2. **Build Tailwind CSS:**
   ```bash
   npm run build:css
   ```

3. **(Optional) Watch for Changes:**
   If you’re actively developing and editing templates or CSS, use this command to rebuild Tailwind CSS automatically when changes occur:
   ```bash
   npm run watch:css
   ```

---

## **For Tailwind Development**

1. **Editing Tailwind Styles:**
   - The input file for Tailwind is located at:
     ```
     IMBD_app/static/css/tailwind.css
     ```
   - Add your custom styles or utilities there.

2. **Rebuild Tailwind CSS:**
   When making changes to 'tailwind.css' run the following command:
   ```bash
   npm run build:css
   ```



