import os
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By

def capture_extra():
    output_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    os.makedirs(output_dir, exist_ok=True)

    edge_options = EdgeOptions()
    edge_options.add_argument("--headless=new")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--window-size=1440,1100")

    driver = webdriver.Edge(options=edge_options)
    try:
        # 1. Capture Django Admin Panel
        print("Logging into Django Admin...")
        driver.get("http://127.0.0.1:8000/admin/login/?next=/admin/routing/node/")
        time.sleep(1)
        try:
            driver.find_element(By.NAME, "username").send_keys("admin")
            driver.find_element(By.NAME, "password").send_keys("admin123")
            driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
            time.sleep(1.5)
            path_admin = os.path.join(output_dir, "05_django_admin_jelas.png")
            driver.save_screenshot(path_admin)
            print(f"Captured: {path_admin}")
        except Exception as e:
            print("Admin capture note:", e)

        # 2. Capture Dhaka Metro Network Tab
        print("Capturing Dhaka Metro network...")
        driver.get("http://127.0.0.1:8000/")
        time.sleep(2)
        driver.find_element(By.ID, "netBtn-dhaka").click()
        time.sleep(1.5)
        path_dhaka = os.path.join(output_dir, "06_dhaka_metro_network.png")
        driver.save_screenshot(path_dhaka)
        print(f"Captured: {path_dhaka}")

        # 3. Capture BFS (Breadth-First Search) Route
        print("Capturing BFS route...")
        driver.find_element(By.ID, "netBtn-bangladesh").click()
        time.sleep(1.5)
        # Uncheck animation
        try:
            anim = driver.find_element(By.ID, "animateToggle")
            if anim.is_selected():
                anim.click()
        except Exception:
            pass

        bfs_radio = driver.find_element(By.CSS_SELECTOR, "input[name='algorithm'][value='bfs']")
        bfs_radio.click()
        driver.find_element(By.ID, "findRouteBtn").click()
        time.sleep(1.5)
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(0.5)
        path_bfs = os.path.join(output_dir, "07_bfs_route_result.png")
        driver.save_screenshot(path_bfs)
        print(f"Captured: {path_bfs}")

        # 4. Capture DFS (Depth-First Search) Detour Route
        print("Capturing DFS route...")
        dfs_radio = driver.find_element(By.CSS_SELECTOR, "input[name='algorithm'][value='dfs']")
        dfs_radio.click()
        driver.find_element(By.ID, "findRouteBtn").click()
        time.sleep(1.5)
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(0.5)
        path_dfs = os.path.join(output_dir, "08_dfs_route_detour.png")
        driver.save_screenshot(path_dfs)
        print(f"Captured: {path_dfs}")

        print("Extra screenshots captured successfully!")
    finally:
        driver.quit()

if __name__ == "__main__":
    capture_extra()
