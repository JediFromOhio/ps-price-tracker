import boto3

SENDER_EMAIL = 'thatgamedevjedi@gmail.com'
RECIPIENT_EMAIL = 'thatgamedevjedi@gmail.com'

def send_price_drop_alert(item_name, old_price, new_price, product_url):
    session = boto3.Session(profile_name="ps-price-tracker")
    ses_client = session.client("ses", region_name="us-east-1")

    subject = f"Price Drop Alert: {item_name}"
    body = (
        f"{item_name} has dropped in price.\n\n"
        f"Old Price: ${old_price / 100:.2f}\n"
        f"New Price: ${new_price / 100:.2f}\n"
        f"Link: {product_url}\n"
    )

    ses_client.send_email(
        Source=SENDER_EMAIL,
        Destination={'ToAddresses': [RECIPIENT_EMAIL]},
        Message={
            'Subject': {"Data": subject},
            'Body': {"Text": {'Data': body}},
        },
    )

def send_failure_summary(failures):
    session = boto3.Session(profile_name="ps-price-tracker")
    ses_client = session.client("ses", region_name="us-east-1")

    subject = f"PS Price Tracker: {len(failures)} title(s) failed this run"
    body_lines = [f"- {f['product_id']}: {f['error']}" for f in failures]
    body = "The following titles failed to scrape:\n\n" + "\n".join(body_lines)

    ses_client.send_email(
        Source=SENDER_EMAIL,
        Destination={'ToAddresses': [RECIPIENT_EMAIL]},
        Message={
            'Subject': {"Data": subject},
            'Body': {"Text": {'Data': body}},
        },
    )
