# Instahyre Auto Apply Bot

Automate your job applications on Instahyre with this powerful Python bot! This tool logs in, filters jobs, and applies automatically, saving you hours of manual effort.

## Features
- Automated login (supports Google and email/password)
- Job search filtering (YOE, job function, location, company size)
- Automatic application to jobs with robust handling of dynamic web elements
- Modular code for easy customization

## Setup Instructions

### 1. Clone the Repository
```
git clone https://github.com/vs704vs/instahyre-bot.git
cd instahyre-bot
```

### 2. Install Python Dependencies
Make sure you have Python 3.8+ installed.
```
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root with the following content:
```
# Required credentials
INSTA_EMAIL=your_email@example.com
INSTA_PASSWORD=your_password

# Optional filters
# YOE: Years of experience (number)
# JOB_FUNCTION: Comma-separated job functions (e.g., Software Engineer,Backend Developer)
# LOCATION: Comma-separated locations (e.g., Bangalore,Remote)
# COMPANY_SIZE: One of Small, Medium, Large, or All
```

Example:
```
INSTA_EMAIL=your_email@example.com
INSTA_PASSWORD=your_password
YOE=2
JOB_FUNCTION=Frontend Developer,Full Stack Developer
LOCATION=Delhi,Mumbai
COMPANY_SIZE=Medium
```
* COMPANY_SIZE can be: Small, Medium, Large, or All
* YOE is a number (years of experience)
* JOB_FUNCTION and LOCATION can be comma-separated for multiple values

### 4. Run the Bot
```
python main.py
```

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## SEO Keywords
Instahyre automation, Instahyre bot, auto apply Instahyre, job application automation, Python Instahyre script, Playwright Instahyre bot, job search automation, Instahyre auto apply bot, automate Instahyre applications, open source Instahyre bot

---

Boost your job search productivity with the Instahyre Auto Apply Bot!