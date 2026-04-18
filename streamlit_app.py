import os
import sys
import subprocess

# Ensure playwright is installed in the current environment
try:
    import playwright
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright"])
    import playwright

# Ensure browsers are installed (use absolute path for the lock file)
_install_lock = os.path.join(os.path.expanduser("~"), "playwright_browsers_installed.txt")
if not os.path.exists(_install_lock):
    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"])
    with open(_install_lock, "w") as f:
        f.write("done")
import streamlit as st
import subprocess
import os

st.title("Instahyre Auto Apply Bot")
st.write("""
Automate your job applications on Instahyre! Enter your details below and click 'Start Applying'.
Your credentials are used only for this session and not stored.
""")

email = st.text_input("Instahyre Email", "")
password = st.text_input("Instahyre Password", "", type="password")
yoe = st.text_input("Years of Experience (YOE)", "")
job_functions = st.text_input("Job Functions (comma separated)", "")
locations = st.text_input("Locations (comma separated)", "")
company_size = st.selectbox("Company Size", ["All", "Small", "Medium", "Large"])

if st.button("Start Applying"):
    if not email or not password:
        st.error("Email and Password are required!")
    else:
        # Set environment variables for the subprocess
        env = os.environ.copy()
        env["INSTAHYRE_EMAIL"] = email
        env["INSTAHYRE_PASSWORD"] = password
        env["YOE"] = yoe
        env["JOB_FUNCTIONS"] = job_functions
        env["LOCATIONS"] = locations
        env["COMPANY_SIZE"] = company_size

        with st.spinner("Running the bot and applying to jobs..."):
            result = subprocess.run(
                [sys.executable, "main.py"],
                env=env,
                capture_output=True,
                text=True
            )
        st.success("Done! The bot has finished applying to jobs.")
        st.text_area("Bot Output", result.stdout + "\n" + result.stderr)