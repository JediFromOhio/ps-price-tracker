from playwright.sync_api import sync_playwright

TARGET_HASH = "a3674adcab1c43cc5847002da67e12a2d138f3ad9dc67dd362452220ea492b26"

PRODUCTS = [
    { "url": "https://store.playstation.com/en-us/product/UP1018-PPSA01617_00-00MORTALKOMBAT11", "product_id": "UP1018-PPSA01617_00-00MORTALKOMBAT11"},
    { "url": "https://store.playstation.com/en-us/product/UP0006-PPSA19534_00-SANTIAGOSTANDARD", "product_id": "UP0006-PPSA19534_00-SANTIAGOSTANDARD"},
    { "url": "https://store.playstation.com/en-us/product/EP3969-PPSA11386_00-007FIRSTLIGHT000", "product_id": "EP3969-PPSA11386_00-007FIRSTLIGHT000"}
]

def fetch_product_data(page, product_url: str, product_id: str):
    with page.expect_response(lambda response: TARGET_HASH in response.url) as response_info:
        page.goto(product_url)

    response = response_info.value
    data = response.json()

    products = data["data"]["productRetrieve"]["concept"]["products"]
    product = next(p for p in products if p["id"] == product_id)

    price_info = product["webctas"][0]["price"]

    result = {
        "name": product["name"],
        "currency": price_info.get("currencyCode"),
        "base_price": price_info.get("basePriceValue"),
        "discounted_price": price_info.get("discountedValue"),
        "end_time": price_info.get("endTime"),
    }
    result["current_price"] = result["discounted_price"] or result["base_price"] 
    return result



def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        results = []
        failures = []
        for item in PRODUCTS:
            page = browser.new_page()
            try:
                data = fetch_product_data(page, item["url"], item["product_id"])
                results.append(data)  
                print(data)      
            except Exception as e:
                print(f"Failed to fetch {item['product_id']}: {e}")
                failures.append({"product_id": item["product_id"], "error": str(e)})
            finally:
                page.close()

        browser.close()

    if failures:
        print(f"{len(failures)} title(s) failed this run:", failures)

    return results

if __name__ == "__main__":
    run()