import os
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By

def capture():
    output_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    os.makedirs(output_dir, exist_ok=True)

    edge_options = EdgeOptions()
    edge_options.add_argument("--headless=new")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--window-size=1440,1100")

    driver = webdriver.Edge(options=edge_options)
    try:
        url = "http://127.0.0.1:8000/"
        print(f"Loading {url}...")
        driver.get(url)
        time.sleep(3)

        # 1. Main Dashboard (32 Bangladesh Jelas)
        path1 = os.path.join(output_dir, "01_main_dashboard_bangladesh_jelas.png")
        driver.save_screenshot(path1)
        print(f"Captured: {path1}")

        # 2. Click preset: Dhaka -> Chattogram
        print("Selecting preset Dhaka ➔ Chattogram...")
        # Uncheck animation to instantly render
        try:
            anim = driver.find_element(By.ID, "animateToggle")
            if anim.is_selected():
                anim.click()
        except Exception:
            pass

        # Select A* and click compute
        btn = driver.find_element(By.ID, "findRouteBtn")
        btn.click()
        time.sleep(2)

        # Scroll slightly to see both map route and metrics
        driver.execute_script("window.scrollTo(0, 350);")
        time.sleep(1)
        path2 = os.path.join(output_dir, "02_a_star_route_dhaka_to_chattogram.png")
        driver.save_screenshot(path2)
        print(f"Captured: {path2}")

        # 3. 4-Way Comparison: BFS vs DFS vs Dijkstra vs A*
        print("Running 4-Way Comparison...")
        compare_radio = driver.find_element(By.CSS_SELECTOR, "input[name='algorithm'][value='compare']")
        compare_radio.click()
        btn = driver.find_element(By.ID, "findRouteBtn")
        btn.click()
        time.sleep(2)

        driver.execute_script("document.getElementById('resultsSection').scrollIntoView();")
        time.sleep(1)
        path3 = os.path.join(output_dir, "03_four_way_comparison_bfs_dfs_dijkstra_astar.png")
        driver.save_screenshot(path3)
        print(f"Captured: {path3}")

        # 4. Projector View (Light Theme)
        print("Toggling Projector View...")
        theme_btn = driver.find_element(By.ID, "themeToggleBtn")
        theme_btn.click()
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        path4 = os.path.join(output_dir, "04_projector_day_view.png")
        driver.save_screenshot(path4)
        print(f"Captured: {path4}")

        print("All screenshots successfully captured!")

    finally:
        driver.quit()

if __name__ == "__main__":
    capture()
