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
   git clone https://github.com/ErickMontesDK/IST105-Assignment9.git
   cd IST105-Assignment9
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply migrations:**
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

## Usage
- Authenticate with your Cisco DNA Center credentials.
- View your token, list devices, and see interface details.
- Use the "Exit" button to log out and clear credentials.

## Notes
- For MongoDB logging, ensure your MongoDB instance is running and configured if you want to store logs.

## MongoDB Setup & Configuration

### 1. Install MongoDB (Ubuntu 20.04/22.04)
```bash
# Import MongoDB Public GPG Key
curl -fsSL https://pgp.mongodb.com/server-6.0.asc | \
  sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg \
  --dearmor

# Create a List File for MongoDB
echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu $(lsb_release -cs)/mongodb-org/6.0 multiverse" | \
  sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list > /dev/null

# Update Package Index
sudo apt update

# Install MongoDB
sudo apt install -y mongodb-org

# Start and Enable MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Verify MongoDB is Running
sudo systemctl status mongod
```
You should see `Active: active (running)`.

### 2. Allow Remote Connections (Optional/Only if you need remote access)
Edit `/etc/mongod.conf`:
```yaml
net:
  port: 27017
  bindIp: 0.0.0.0
```
Then restart MongoDB:
```bash
sudo systemctl restart mongod
```

### 3. Create a Database User
```bash
mongosh
```
In the MongoDB shell:
```js
use <DB_NAME>

db.createUser({
  user: "<DB_USER>",
  pwd: "<DB_PASSWORD>",
  roles: [{ role: "readWrite", db: "<DB_NAME>" }]
})
```
You can view users with:
```js
show users
```

### 4. Django Integration
Install the required packages:
```bash
pip install djongo pymongo
```
In your `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': '<DB_NAME>',
        'CLIENT': {
            'host': 'mongodb://<DB_USER>:<DB_PASSWORD>@<MONGO_SERVER_IP>:27017/<DB_NAME>?authSource=<DB_NAME>',
        }
    }
}
```
Replace `<DB_USER>`, `<DB_PASSWORD>`, `<DB_NAME>`, and `<MONGO_SERVER_IP>` with your actual MongoDB credentials and server IP.

---

**Author:** Erick Montes Bedolla