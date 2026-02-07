# Columnify 📚

**Columnify** is a lightweight tool that transforms 2-column medical PDFs into a single-column layout optimized for tablets and mobile. It automatically fixes page rotation and uses smart centering to ensure text is never cut off, even in imperfect scans. By manipulating PDF metadata instead of converting to images, it preserves 100% of the original text sharpness and searchability. No Python installation or admin rights required—just select, name, and process.



## ✨ Why Columnify?
* **Smart Split:** Automatically centers the cut based on page dimensions to avoid slicing through text.
* **Auto-Rotation:** Detects and fixes page orientation metadata before splitting.
* **Lossless Quality:** No OCR or image conversion. It manipulates the PDF `MediaBox`, keeping text 100% sharp, searchable, and selectable.
* **User-Friendly:** Standalone GUI that requires no technical knowledge and **no administrative rights**.

## 🚀 How to Use
1.  **Select PDF:** Use the "Browse PDF" button to pick your textbook.
2.  **Name Output:** Type the full name for the new file (e.g., `Biology_Mobile.pdf`).
3.  **Process:** Click "Process PDF". The progress bar will track the page count and percentage.

---

## 🛠 Developer Guide

To run this project locally or modify the source code, follow these steps:

### 1. Download the Project
First, clone this repository to your local machine:
```bash
git clone [https://github.com/AM2201NE/Columnify.git](https://github.com/AM2201NE/Columnify.git)

```

*Alternatively, click the green **"Code"** button at the top of this page and select **"Download ZIP"**, then extract the files.*

### 2. Requirements

Navigate to the project folder and install the necessary libraries. You must have Python installed.

```bash
cd Columnify
pip install pypdf pyinstaller

```

### 3. Run the Script

To launch the app directly from the source code:

```bash
python Columnify.py

```

### 4. Build Standalone EXE (Packaging)

To create a single `.exe` file that you can share with others (works without Python installed and without Admin rights):

```bash
pyinstaller --noconsole --onefile --clean --name "Columnify" Columnify.py

```

*After running this, look in the **dist/** folder for your `Columnify.exe`.*

---

## ⚖️ License

This project is licensed under the MIT License - see the LICENSE file for details.
