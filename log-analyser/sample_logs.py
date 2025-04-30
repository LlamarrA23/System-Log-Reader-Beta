#!/usr/bin/env python3
"""
Generates 50 realistic auth log entries for testing
"""

import random
from datetime import datetime, timedelta
import os

# Configuration
LOG_FILE = "auth.log"
NUM_ENTRIES = 50
START_DATE = datetime.now() - timedelta(days=1)  # Logs from past 24 hours

# Sample data
USERS = ["admin", "root", "bob", "alice", "guest", "www-data", "ubuntu"]
IPS = ["192.168.1.{}".format(i) for i in range(1, 20)]
MESSAGES = {
    "success": "Accepted password for {} from {} port {} ssh2",
    "fail": "Failed password for {} from {} port {} ssh2",
    "invalid": "Invalid user {} from {} port {} ssh2",
    "timeout": "Connection closed by {} port {} [preauth]"
}

def random_timestamp(base_date):
    """Generate random timestamp within range"""
    return base_date + timedelta(seconds=random.randint(0, 86400))

def generate_log_entry(timestamp):
    """Generate one random log entry"""
    user = random.choice(USERS + ["hacker"])  # Occasionally add invalid user
    ip = random.choice(IPS)
    port = random.randint(10000, 60000)
    
    # 70% chance of failed login, 20% success, 10% invalid/other
    roll = random.random()
    if roll < 0.7:
        msg = MESSAGES["fail"].format(user, ip, port)
    elif roll < 0.9:
        msg = MESSAGES["success"].format(user, ip, port)
    else:
        msg = MESSAGES["invalid"].format(user if user == "hacker" else random.choice(["test", "unknown"]), ip, port)
    
    return f"{timestamp.strftime('%b %d %H:%M:%S')} sshd[{random.randint(1000,9999)}]: {msg}\n"

def main():
    """Generate log file"""
    log_path = os.path.join(os.path.dirname(__file__), LOG_FILE)
    
    print(f"Generating {NUM_ENTRIES} log entries in {LOG_FILE}...")
    
    with open(log_path, "w") as f:
        for _ in range(NUM_ENTRIES):
            timestamp = random_timestamp(START_DATE)
            f.write(generate_log_entry(timestamp))
    
    print(f"Done! Created {LOG_FILE} with {NUM_ENTRIES} entries")

if __name__ == "__main__":
    main()