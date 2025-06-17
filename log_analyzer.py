import re

# Specify the path to the log file (update if needed)
log_file_path = "auth.log"  # Use a sample log for testing

def parse_log(file_path):
    """
    Reads the specified log file and returns its lines.
    """
    with open(file_path, "r") as file:
        lines = file.readlines()
    return lines

def find_failed_logins(log_lines):
    """
    Looks for failed SSH login attempts in log lines.
    """
    failed_logins = []
    pattern = re.compile(r"Failed password for (invalid user )?(\w+) from ([\d\.]+)")
    for line in log_lines:
        match = pattern.search(line)
        if match:
            user = match.group(2)
            ip = match.group(3)
            failed_logins.append((user, ip))
    return failed_logins

def summarize_attempts(failed_logins):
    """
    Summarizes failed login attempts by IP.
    """
    summary = {}
    for user, ip in failed_logins:
        summary[ip] = summary.get(ip, 0) + 1
    return summary

if __name__ == "__main__":
    print("Reading log file...")
    lines = parse_log(log_file_path)
    failed_logins = find_failed_logins(lines)
    print(f"Total failed login attempts: {len(failed_logins)}\n")

    summary = summarize_attempts(failed_logins)
    print("Failed login attempts by IP:")
    for ip, count in summary.items():
        print(f"{ip}: {count} attempts")
