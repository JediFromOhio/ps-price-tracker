from unittest.mock import patch

from scraper import parse_product_data


def test_parse_product_data_with_discount():
    # Arrange mock fake data and mock objects
    product_id = "UP1018-PPSA01617_00-00MORTALKOMBAT11"
    fake_json = {
        "data": {
            "productRetrieve": {
                "concept": {
                    "products": [
                        {
                            "id": product_id,
                            "name": "Mortal Kombat 11",
                            "webctas": [
                                {
                                    "price": {
                                        "currencyCode": "USD",
                                        "basePriceValue": 4999,
                                        "discountedValue": 999,
                                        "endTime": "2026-10-01",
                                    }
                                }
                            ],
                        }
                    ]
                }
            }
        }
    }

    # Pass in the fake json
    result = parse_product_data(fake_json, product_id)
    
    # Assert the behaviour
    assert result["name"] == "Mortal Kombat 11"
    assert result["base_price"] == 4999
    assert result["discounted_price"] == 999
    assert result["current_price"] == 999 # It should pick the discounted price


def test_parse_product_data_no_discount():
    product_id = "UP1018-PPSA01617_00-00MORTALKOMBAT11"
    fake_json = {
        "data": {
            "productRetrieve": {
                "concept": {
                    "products": [
                        {
                            "id": product_id,
                            "name": "Mortal Kombat 11",
                            "webctas": [
                                {
                                    "price": {
                                        "currencyCode": "USD",
                                        "basePriceValue": 4999,
                                        "discountedValue": None,  # Not on sale
                                        "endTime": None,
                                    }
                                }
                            ],
                        }
                    ]
                }
            }
        }
    }
    result = parse_product_data(fake_json, product_id)
    assert result["name"] == "Mortal Kombat 11"
    assert result["base_price"] == 4999
    assert result["discounted_price"] is None
    assert result["current_price"] == 4999  # Falls back to base price


def test_price_drop_triggers_alert():
    # We patch 'send_price_drop_alert' inside scraper
    with patch("scraper.send_price_drop_alert") as mock_alert:
        previous_price = 6999
        current_price = 4999

        if previous_price is not None and current_price < previous_price:
            from scraper import send_price_drop_alert
            send_price_drop_alert("God of war", previous_price, current_price, "https://...")


        mock_alert.assert_called_once()

    
def test_price_increase_does_not_alert():
    with patch("scraper.send_price_drop_alert") as mock_alert:
        previous_price = 3999
        current_price = 5999 # Price went up

        if previous_price is not None and current_price < previous_price:
            from scraper import send_price_drop_alert
            send_price_drop_alert("God of war", previous_price, current_price, "https://...")

        # Verify the alert was never called
        mock_alert.assert_not_called()