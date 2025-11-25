# Operation: Data Heist

Welcome, agent. This project is your mission, should you choose to accept it. You are about to infiltrate the secure servers of the notorious "SecureCorp." Your objective is to bypass their security and retrieve the secret data hidden within.

This is a theme-based web application designed to teach several key cybersecurity concepts in a fun, story-driven way.

## The Mission Stages

Your mission is broken down into four stages:

### Stage 1: Reconnaissance
-   **Objective:** Find the hidden login portal.
-   **Scenario:** You will start at the public-facing corporate homepage. There is no obvious way in. You must use your reconnaissance skills to discover the secret entry point.
-   **Hint:** In the real world, system administrators sometimes accidentally leak paths in files not meant for public consumption. Check everything.

### Stage 2: Infiltration (Brute-Force)
-   **Objective:** Break through the login page.
-   **Scenario:** Once you've found the portal, you'll be met with a login screen. We have intelligence that suggests the password is weak.
-   **Tool:** This is the perfect opportunity to use the **`Digital-Safecracker`** tool to automate a brute-force attack.

### Stage 3: Privilege Escalation
-   **Objective:** Gain admin-level access.
-   **Scenario:** A successful login will grant you access to a dashboard, but you'll be classified as a low-level user. The secret data is only available to "Admins." You need to find a way to elevate your own privileges.
-   **Hint:** How does the server know who you are? Sometimes, the mechanism used to track your identity (like a browser cookie) is not as secure as it should be.

### Stage 4: The Payoff
-   **Objective:** Retrieve the secret data.
-   **Scenario:** If you successfully escalate your privileges, the server will recognize you as an Admin and grant you access to the prize. Mission accomplished!

## How to Run the Project

1.  **Navigate to the project directory:**
    ```bash
    cd Operation-Data-Heist
    ```

2.  **Install the necessary Python packages:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Start the SecureCorp server:**
    ```bash
    python app.py
    ```

4.  **Begin your mission:**
    Open your web browser and navigate to `http://localhost:5000`. Your mission starts now.

Good luck, agent.
