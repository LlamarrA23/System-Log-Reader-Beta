#!/usr/bin/env python3
"""
Simple Log Analyzer - Finds failed logins and suspicious activity
"""

import re
from collections import defaultdict

def count_failed_logins(log_file):
    """Count failed login attempts by user"""
    failures = defaultdict(int)
    suspicious = []
    
    try:
        with open(log_file) as f:
            for line in f:
                # Check for failed logins
                if "Failed password" in line:
                    user = re.search(r'for (\w+)', line)
                    if user:
                        username = user.group(1)
                        failures[username] += 1
                        
                        # Flag if more than 3 attempts
                        if failures[username] == 3:
                            suspicious.append(username)
    except FileNotFoundError:
        print(f"Error: Cannot find {log_file}")
        return {}, []
        
    return failures, suspicious

if __name__ == "__main__":
    log_file = "auth.log"  # Change this to your log file
    
    print("Analyzing log file...")
    results, warnings = count_failed_logins(log_file)
    
    print("\nResults:")
    for user, count in results.items():
        print(f"{user}: {count} failed attempts")
    
    if warnings:
        print("\nWarnings:")
        for user in warnings:
            print(f"! {user} has multiple failed logins")