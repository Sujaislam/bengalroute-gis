import os
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By

def capture_all():
    output_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    os.makedirs(output_dir, exist_ok=True)

    edge_options = EdgeOptions()
    edge_options.add_argument("--headless=new")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--window-size=1440,1100")

    driver = webdriver.Edge(options=edge_options)
    try:
        url = "http://127.0.0.1:8000/"
        print(f"Loading {url} with Google Maps API Key...")
        driver.get(url)
        time.sleep(4)  # Wait for Google Maps tiles to render

        # 1. Dashboard with Live Google Map
        p1 = os.path.join(output_dir, "01_dashboard_google_maps_live.png")
        driver.save_screenshot(p1)
        print(f"Captured: {p1}")

        # Uncheck animation toggle for instant captures
        try:
            anim = driver.find_element(By.ID, "animateToggle")
            if anim.is_selected():
                anim.click()
        except Exception:
            pass

        # 2. A* Route (Dhaka -> Chattogram) on Google Map
        print("Computing A* route on Google Map...")
        driver.find_element(By.CSS_SELECTOR, "input[name='algorithm'][value='a_star']").click()
        driver.find_element(By.ID, "findRouteBtn").click()
        time.sleep(2.5)
        driver.execute_script("window.scrollTo(0, 320);")
        time.sleep(1)
        p2 = os.path.join(output_dir, "02_a_star_path_google_map.png")
        driver.save_screenshot(p2)
        print(f"Captured: {p2}")

        # 3. Dijkstra Route
        print("Computing Dijkstra route...")
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "input[name='algorithm'][value='dijkstra']").click()
        driver.find_element(By.ID, "findRouteBtn").click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 320);")
        time.sleep(1)
        p3 = os.path.join(output_dir, "03_dijkstra_path_route.png")
        driver.save_screenshot(p3)
        print(f"Captured: {p3}")

        # 4. BFS Route
        print("Computing BFS route...")
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "input[name='algorithm'][value='bfs']").click()
        driver.find_element(By.ID, "findRouteBtn").click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 320);")
        time.sleep(1)
        p4 = os.path.join(output_dir, "04_bfs_shortest_hops_route.png")
        driver.save_screenshot(p4)
        print(f"Captured: {p4}")

        # 5. DFS Route Detour
        print("Computing DFS route...")
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "input[name='algorithm'][value='dfs']").click()
        driver.find_element(By.ID, "findRouteBtn").click()
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 320);")
        time.sleep(1)
        p5 = os.path.join(output_dir, "05_dfs_deep_detour_route.png")
        driver.save_screenshot(p5)
        print(f"Captured: {p5}")

        # 6. Part C 4-Way Comparison Table & Progress Bars
        print("Computing Part C 4-Way Comparison...")
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        driver.find_element(By.CSS_SELECTOR, "input[name='algorithm'][value='compare']").click()
        driver.find_element(By.ID, "findRouteBtn").click()
        time.sleep(2.5)
        driver.execute_script("document.getElementById('resultsSection').scrollIntoView();")
        time.sleep(1)
        p6 = os.path.join(output_dir, "06_four_way_comparison_matrix.png")
        driver.save_screenshot(p6)
        print(f"Captured: {p6}")

        # 7. Projector View (Light Theme on Google Map)
        print("Toggling Projector View...")
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        driver.find_element(By.ID, "themeToggleBtn").click()
        time.sleep(1.5)
        p7 = os.path.join(output_dir, "07_projector_day_view_google_map.png")
        driver.save_screenshot(p7)
        print(f"Captured: {p7}")

        # Switch back to dark theme
        driver.find_element(By.ID, "themeToggleBtn").click()
        time.sleep(0.5)

        # 8. Dhaka Metro Network
        print("Switching to Dhaka Metro Network...")
        driver.find_element(By.ID, "netBtn-dhaka").click()
        time.sleep(3)
        p8 = os.path.join(output_dir, "08_dhaka_metro_network_google_map.png")
        driver.save_screenshot(p8)
        print(f"Captured: {p8}")

        # 9. Django Admin Panel
        print("Capturing Django Admin...")
        driver.get("http://127.0.0.1:8000/admin/login/?next=/admin/routing/node/")
        time.sleep(1)
        try:
            driver.find_element(By.NAME, "username").send_keys("admin")
            driver.find_element(By.NAME, "password").send_keys("admin123")
            driver.find_element(By.CSS_SELECTOR, "input[type='submit']").click()
            time.sleep(2)
            p9 = os.path.join(output_dir, "09_django_admin_database_models.png")
            driver.save_screenshot(p9)
            print(f"Captured: {p9}")
        except Exception as e:
            print("Admin capture note:", e)

        print("All pointable object screenshots captured successfully!")

    finally:
        driver.quit()

if __name__ == "__main__":
    capture_all()
