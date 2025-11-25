# Red-vs-Blue-Sim: An Ethical Hacking Playground

Welcome to the Red vs. Blue Simulation Suite. This project is an interactive, educational environment designed to teach fundamental cybersecurity concepts by putting you in the role of both the attacker (Red Team) and the defender (Blue Team).

## Overview

This suite contains two main projects:

1.  **`Digital-Safecracker` (Red Team Tool):**
    A Python-based command-line tool for executing password attacks. It started as a simple dictionary attacker and was upgraded to include a true brute-force mode. This is your primary offensive weapon.

2.  **`Operation-Data-Heist` (Blue Team Target):**
    A vulnerable web application built with Python and Flask. This project is a multi-stage mission where you, the "agent," must use your skills to find and exploit a series of vulnerabilities to reach the final objective. It is the target for your Red Team tool.

## How to Use This Suite

This is a guided experience. It's recommended to start with the `Operation-Data-Heist` mission.

1.  **Set up the Target:** Navigate into `Operation-Data-Heist`, set up the Python virtual environment, and run the web server as instructed in its `README.md`.
2.  **Begin the Mission:** Access the web application in your browser and follow the mission prompts.
3.  **Use Your Tools:** When you reach a stage that requires a password attack, navigate to the `Digital-Safecracker` directory in a separate terminal and use the tool to attack the `Operation-Data-Heist` target.

By playing both sides of the simulation, you will gain a practical understanding of reconnaissance, brute-force attacks, privilege escalation, and how to defend against them.

## Educational Goals

-   Understand the difference between dictionary and brute-force attacks.
-   Learn how to use command-line tools to interact with web applications.
-   Identify and exploit common web vulnerabilities (reconnaissance via `robots.txt`, weak passwords, insecure cookies).
-   Appreciate the attacker's mindset (Red Team) and the defender's challenges (Blue Team).

Have fun, and hack ethically!
