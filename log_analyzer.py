import re

# Specify the path to the log file you want to analyze
# For real systems, this could be '/var/log/auth.log'. Here, use a sample file for testing.
log_file_path = "auth.log"

def parse_log(file_path):
    """
    Reads the specified log file and returns its lines as a list.
    """
    with open(file_path, "r") as file:
        lines = file.readlines()  # Read all lines from the log file
    return lines

def find_failed_logins(log_lines):
    """
    Searches through the log lines to find failed SSH login attempts.
    Returns a list of tuples containing (username, IP address) for each failed attempt.
    """
    failed_logins = []
    # This regex matches lines indicating a failed SSH login attempt
    pattern = re.compile(r"Failed password for (invalid user )?(\w+) from ([\d\.]+)")
    for line in log_lines:
        match = pattern.search(line)
        if match:
            user = match.group(2)  # Extract the username from the match
            ip = match.group(3)    # Extract the IP address from the match
            failed_logins.append((user, ip))  # Add the result to the list
    return failed_logins

def summarize_attempts(failed_logins):
    """
    Summarizes the failed login attempts by IP address.
    Returns a dictionary with IP addresses as keys and the number of attempts as values.
    """
    summary = {}
    for user, ip in failed_logins:
        # If the IP is already in the summary, increment its count, else set to 1
        summary[ip] = summary.get(ip, 0) + 1
    return summary

if __name__ == "__main__":
    # Step 1: Read the log file
    print("Reading log file...")
    lines = parse_log(log_file_path)
    # Step 2: Find and collect failed login attempts
    failed_logins = find_failed_logins(lines)
    print(f"Total failed login attempts: {len(failed_logins)}\n")

    # Step 3: Summarize the number of failed attempts per IP address
    summary = summarize_attempts(failed_logins)
    print("Failed login attempts by IP:")
    for ip, count in summary.items():
        print(f"{ip}: {count} attempts")
