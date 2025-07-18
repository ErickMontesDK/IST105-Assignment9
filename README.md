# Cisco DNA Center Django Web Interface

## Description
This project is a Django web application that allows you to:
- Authenticate with Cisco DNA Center and display the authentication token
- List network devices
- Show interface details by device IP
- Log actions in a database (MongoDB integration ready)

## Requirements
- Python 3.8+
- pip
- Cisco DNA Center sandbox or your own instance

## Installation
1. **Clone the repository:**
   ```bash
   git clone <REPO_URL>
   cd <project_folder>
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure DNA Center connection:**
   - Edit `dna_center_cisco/dnac_config.py` with your DNA Center host, port, username, and password (or use the login form).

4. **Apply migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. **Run the server:**
   ```bash
   python manage.py runserver
   ```
6. **Access the app:**
   - Open your browser and go to [http://localhost:8000/](http://localhost:8000/)

## Main Dependencies
- Django
- requests
- pymongo
- dnac_config (custom, included)

## Usage
- Authenticate with your Cisco DNA Center credentials.
- View your token, list devices, and see interface details.
- Use the "Exit" button to log out and clear credentials.

## Notes
- For MongoDB logging, ensure your MongoDB instance is running and configured if you want to store logs.
- The project is ready for further extension (e.g., more endpoints, advanced logging, etc).

---

**Author:** Erick 