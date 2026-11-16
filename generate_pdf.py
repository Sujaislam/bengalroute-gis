import os
import base64
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions

def generate_pdf():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(base_dir, "pdf_template.html")
    pdf_out1 = os.path.join(base_dir, "PathFinder_GIS_Bangladesh_Documentation.pdf")
    artifact_dir = r"C:\Users\suja\.gemini\antigravity-cli\brain\3281888d-5118-4784-9542-5b35db51cbfd"
    pdf_out2 = os.path.join(artifact_dir, "PathFinder_GIS_Bangladesh_Documentation.pdf")

    edge_options = EdgeOptions()
    edge_options.add_argument("--headless=new")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--allow-file-access-from-files")
    edge_options.add_argument("--enable-local-file-accesses")

    driver = webdriver.Edge(options=edge_options)
    try:
        file_url = f"file:///{html_path.replace(os.sep, '/')}"
        print(f"Loading {file_url}...")
        driver.get(file_url)
        time.sleep(3)  # Wait for images to load into DOM

        print_params = {
            "landscape": False,
            "displayHeaderFooter": False,
            "printBackground": True,
            "preferCSSPageSize": True,
            "marginTop": 0.4,
            "marginBottom": 0.4,
            "marginLeft": 0.4,
            "marginRight": 0.4,
        }

        print("Generating PDF via CDP Page.printToPDF...")
        result = driver.execute_cdp_cmd("Page.printToPDF", print_params)
        pdf_bytes = base64.b64decode(result["data"])

        with open(pdf_out1, "wb") as f:
            f.write(pdf_bytes)
        print(f"Successfully saved PDF to: {pdf_out1} ({len(pdf_bytes)} bytes)")

        if os.path.exists(artifact_dir):
            with open(pdf_out2, "wb") as f:
                f.write(pdf_bytes)
            print(f"Successfully saved PDF to artifact dir: {pdf_out2}")

    finally:
        driver.quit()

if __name__ == "__main__":
    generate_pdf()
