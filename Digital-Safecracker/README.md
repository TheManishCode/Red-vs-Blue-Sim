# The Digital Safecracker: An Educational Brute-Force Simulator

This project is a Python-based command-line tool designed to simulate a safecracker trying every possible combination to open a digital vault (a web login form). It's built for educational purposes to demonstrate how a basic brute-force attack works.

***

### **🔴 ETHICAL USE DISCLAIMER 🔴**

**This tool is for educational purposes ONLY.** Using this script on any system, website, or application without explicit, prior authorization from the owner is **illegal and unethical**. The author of this script is not responsible for any misuse or damage caused by this program. **Always respect privacy and the law.**

***

## What is Digital Safecracking?

Just like a safecracker tries every possible combination to open a physical vault, a "digital safecracker" (or a brute-force attack) is a method used to guess credentials like a password. The attacker's script systematically tries a huge list of potential passwords, hoping one of them is the correct "combination" to unlock access. This tool automates that process for learning purposes.

## Features

-   **Two Attack Modes:**
    -   **Dictionary Mode:** A high-speed attack using a pre-defined wordlist (e.g., `passwords.txt`).
    -   **Brute-Force Mode:** A true brute-force attack that generates all possible character combinations up to a given length.
-   **Multi-Threaded:** Uses multiple threads to speed up the attack simulation.
-   **Verbose Logging:** Provides real-time feedback on which combination is being tested.
-   **Educational Comments:** The code is heavily commented to explain every step of the process.

## How to Run the Script

The script can be run in one of two modes: `dictionary` or `bruteforce`.

### Dictionary Mode (Default)

This mode is fast and tests passwords from a file.

```bash
python brute_forcer.py --url <TARGET_URL> --username <USERNAME> --mode dictionary --passwords <PATH_TO_PASSWORD_FILE>
```
*You can omit `--mode dictionary` as it's the default.*

**Example with "Operation: Data Heist":**
```bash
python brute_forcer.py --url http://localhost:5000/secret-login-portal --username admin --passwords passwords.txt
```

### Brute-Force Mode

This mode will try every possible combination.

**🔴 Warning:** The number of combinations grows exponentially. A long `max-length` or a large `charset` can cause the script to run for an extremely long time (hours, days, or longer). Start with a low `max-length` (e.g., 3 or 4) to see how it works.

```bash
python brute_forcer.py --url <TARGET_URL> --username <USERNAME> --mode bruteforce --charset <CHARACTERS> --max-length <LENGTH>
```

**Example (finding a 3-letter lowercase password):**
```bash
python brute_forcer.py --url http://localhost:5000/secret-login-portal --username agent --mode bruteforce --charset "abc" --max-length 3
```
*This will try a, b, c, aa, ab, ac, ba, bb, bc... etc., up to 3 characters.*

### Interpreting the Output

The script will log each attempt, letting you know if the combination worked.

-   `FAILURE` means the combination was incorrect.
-   `SUCCESS` means the combination worked and the vault is open!

If a combination is found, the script will terminate and print the successful one. If it runs through the entire list without success, it will report that the vault could not be opened with the given list.

## How to Prevent Brute-Force Attacks

Understanding how an attack works is the first step to preventing it. Here are common defenses:

1.  **Account Lockout:** Temporarily lock an account after a certain number of failed login attempts.
2.  **Rate Limiting:** Limit the number of login attempts that can be made from a single IP address in a given time frame.
3.  **CAPTCHA:** Implement a "Completely Automated Public Turing test to tell Computers and Humans Apart" to prevent automated submissions.
4.  **Multi-Factor Authentication (MFA):** Require a second form of verification (like a code from a user's phone) in addition to the password. This is one of the most effective defenses.
5.  **Strong Password Policies:** Enforce the use of long and complex passwords.
