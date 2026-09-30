import os

import boto3

SENDER_EMAIL = os.getenv("ALERT_SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("ALERT_RECIPIENT_EMAIL")
profile_name = os.getenv("AWS_PROFILE")


def send_price_drop_alert(item_name, old_price, new_price, product_url):
    session = boto3.Session(profile_name="ps-price-tracker") if profile_name else boto3.Session()
    ses_client = session.client("ses", region_name="us-east-1")

    subject = f"Price Drop Alert: {item_name}"
    body = (
        f"{item_name} has dropped in price.\n\n"
        f"Old Price: ${old_price / 100:.2f}\n"
        f"New Price: ${new_price / 100:.2f}\n"
        f"Link: {product_url}\n"
    )

    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; color: #222;">
            <h2>Price drop: {item_name}</h2>
            <p>
                <s>${old_price / 100:.2f}</s>
                &rarr;
                <strong style="color: #1a7f37;">${new_price / 100:.2f}</strong>
            </p>
            <p><a href="{product_url}">View on Playstation Store</a></p>
        </body>
    </html>
    """

    ses_client.send_email(
        Source=SENDER_EMAIL,
        Destination={'ToAddresses': [RECIPIENT_EMAIL]},
        Message={
            'Subject': {"Data": subject},
            'Body': {
                "Text": {'Data': body},
                "Html": {'Data': html_body},
            }
        },
    )


def send_failure_summary(failures):
    session = boto3.Session(profile_name="ps-price-tracker") if profile_name else boto3.Session()
    ses_client = session.client("ses", region_name="us-east-1")

    subject = f"PS Price Tracker: {len(failures)} title(s) failed this run"
    body_lines = [f"- {f['product_id']}: {f['error']}" for f in failures]
    body = "The following titles failed to scrape:\n\n" + "\n".join(body_lines)

    html_rows = "".join(
        f"""
        <li style="margin-bottom: 10px;">
            <strong>{f['product_id']}</strong><br>
            <span style="color: #666;">{f['error']}</span>
        </li>
        """
        for f in failures
    )
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #222;">
        <h2>{len(failures)} title(s) failed this run</h2>
        <ul style="padding-left: 20px;">
          {html_rows}
        </ul>
      </body>
    </html>
    """
    ses_client.send_email(
        Source=SENDER_EMAIL,
        Destination={'ToAddresses': [RECIPIENT_EMAIL]},
        Message={
            'Subject': {"Data": subject},
            'Body': {
                "Text": {'Data': body},
                "Html": {'Data': html_body},
            }
        },
    )

