import os
import sys
import argparse
import time
from urllib.parse import urlparse

from dotenv import load_dotenv
from loguru import logger
from twilio.rest import Client


logger.remove(0)
logger.add(sys.stderr, level="DEBUG", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", colorize=True)

load_dotenv(override=True)

def format_webhook_url(base_url):
    """Format the URL for Twilio webhook."""
    parsed_url = urlparse(base_url)
    
    if not parsed_url.scheme:
        base_url = f"http://{base_url}"
    
    if not base_url.endswith('/twiml'):
        base_url = f"{base_url.rstrip('/')}/twiml"
    
    return base_url


def make_call(to_number, from_number, webhook_url, account_sid, auth_token):
    """Initiate an outbound call using Twilio API."""
    logger.info(f"Initiating call to {to_number} from {from_number}")
    
    try:
        client = Client(account_sid, auth_token)
        call = client.calls.create(
            to=to_number,
            from_=from_number,
            url=webhook_url,
        )
        logger.info(f"Call initiated with SID: {call.sid}")
        return call.sid
    except Exception as e:
        logger.error(f"Failed to initiate call: {e}")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initiate outbound calls using Twilio")
    parser.add_argument("to_number", help="Phone number to call (e.g. +1234567890)")
    parser.add_argument("-f", "--from-number", help="Your Twilio phone number", 
                        default=os.getenv("TWILIO_PHONE_NUMBER"))
    parser.add_argument("-u", "--url", help="Base URL for your server",
                        default="http://localhost:8765")
    args = parser.parse_args()
    
    # Get credentials from environment variables
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = args.from_number
    
    # Validate required parameters
    if not account_sid or not auth_token:
        logger.error("TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN must be set in your .env file")
    elif not from_number:
        logger.error("TWILIO_PHONE_NUMBER must be set in your .env file or provided with --from-number")
    else:
        # Format the webhook URL
        webhook_url = format_webhook_url(args.url)
        
        # Make the call
        call_sid = make_call(
            to_number=args.to_number,
            from_number=from_number,
            webhook_url=webhook_url,
            account_sid=account_sid,
            auth_token=auth_token
        )
        
        if call_sid:
            logger.info(f"Call in progress. Call SID: {call_sid}")
            logger.info("Press Ctrl+C to exit (call will continue)")
            
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("Exiting...")
        else:
            logger.error("Failed to initiate call")