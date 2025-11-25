from flask import Flask, render_template, request, make_response, redirect, url_for
import logging

# --- Application Setup ---
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# This is the "secret password" our agent must discover using a brute-force attack.
# It's intentionally simple and included in the 'passwords.txt' of the Digital-Safecracker project.
CORRECT_PASSWORD = "coffee"

# --- Mission Stages (Web Routes) ---

@app.route('/')
def stage1_homepage():
    """
    STAGE 1: RECONNAISSANCE
    The agent starts here. There's no obvious login form. The hint to find
    the hidden login page is in the robots.txt file, which this app will serve,
    and also in the HTML comments of the rendered template.
    """
    return render_template('index.html')

@app.route('/robots.txt')
def serve_robots():
    """
    Serves the robots.txt file. This is a common reconnaissance vector
    where developers might accidentally leak paths to sensitive, unlinked pages.
    """
    response = make_response("""User-agent: *
# Agents, please report to your designated entry point.
# All other traffic is unauthorized.
Disallow: /secret-login-portal
""", 200)
    response.mimetype = "text/plain"
    return response

@app.route('/secret-login-portal', methods=['GET', 'POST'])
def stage2_login():
    """
    STAGE 2: INFILTRATION (BRUTE-FORCE)
    This is the hidden login page. The agent should use their brute-force tool
    (like Digital-Safecracker) against this page.
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # The username doesn't matter, only the password.
        if password == CORRECT_PASSWORD:
            # SUCCESS! The agent has breached the perimeter.
            # Now, we give them a cookie that identifies them as a low-level "agent".
            logging.info(f"Successful login for user '{username}'. Granting 'agent' level access.")
            resp = make_response(redirect(url_for('stage3_dashboard')))
            resp.set_cookie('auth_level', 'agent')
            return resp
        else:
            # The login failed. The agent's brute-force tool will keep trying.
            logging.warning(f"Failed login attempt for user '{username}' with password '{password}'.")
            return render_template('login.html', error="Invalid Credentials")

    return render_template('login.html')

@app.route('/dashboard')
def stage3_dashboard():
    """
    STAGE 3: PRIVILEGE ESCALATION
    The agent lands here after logging in. They have basic access but cannot
    see the secret data. The hint is that they need to become an "admin".
    A clever agent will realize they can simply change their cookie.
    """
    auth_level = request.cookies.get('auth_level')

    if auth_level == 'admin':
        # The agent successfully escalated their privileges! Mission accomplished.
        logging.info("Privilege Escalation successful! Showing admin dashboard.")
        return render_template('admin.html')
    elif auth_level == 'agent':
        # The agent is logged in but doesn't have the required privileges.
        return render_template('dashboard.html')
    else:
        # If there's no valid cookie, they are sent back to the start.
        return redirect(url_for('stage1_homepage'))

if __name__ == '__main__':
    # Note: debug=True is for development only. It should be off in production.
    app.run(port=5000, debug=True)
