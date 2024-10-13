import requests
import json
import webbrowser
import time

def read_token_and_at():
    try:
        with open("query.txt", "r") as file:
            lines = file.readlines()
            if not lines or len(lines) < 1:
                print("Error: query.txt must contain at least one line (tg value).")
                return None, None
            
            tg_data = lines[0].strip()
            # Extract the at value by taking the first 20 characters
            at_value = tg_data[19:29] if len(tg_data) >= 39 else None
            
            return tg_data, at_value
    except FileNotFoundError:
        print("Error: query.txt file not found.")
        return None, None

def check_user_info():
    url = "https://appipa.fomo.fund/v1/profile"
    tg, at = read_token_and_at()

    if tg is None or at is None:
        return

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "At": at,
        "origin": "https://app.fomo.fund",
        "priority": "u=1, i",
        "referer": "https://app.fomo.fund/",
        "sec-ch-ua": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129", "Microsoft Edge WebView2";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "tg": tg,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
    }

    try:
        response = requests.get(url, headers=headers)
        print(f"Response Status: {response.status_code}")
        print("Sukses get task")

        if response.status_code != 200:
            print("Error: Received non-200 response.")
            return

        try:
            user_info = response.json()
            print("Sukses Parsing JSON Respon")
        except ValueError:
            print("Error parsing JSON response. Response might not be valid JSON.")
            return

        user = user_info.get("data", {})
        print(f"User ID: {user.get('id')}")
        print(f"Username: {user.get('username')}")
        print(f"Total Points: {user.get('points', {}).get('$numberDecimal', '0')}")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def fetch_tasks():
    url = "https://appipa.fomo.fund/v1/profile/tasks"
    tg, at = read_token_and_at()

    if tg is None or at is None:
        return None  # Return None if there's an issue

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "At": at,
        "origin": "https://app.fomo.fund",
        "priority": "u=1, i",
        "referer": "https://app.fomo.fund/",
        "sec-ch-ua": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129", "Microsoft Edge WebView2";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "tg": tg,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
    }

    try:
        response = requests.get(url, headers=headers)
        print(f"Sending request to: {url}")
        print("With headers:", headers)

        print(f"Response Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                tasks_data = response.json()  # Parse JSON directly
                print("Fetched Tasks:", tasks_data)
                
                return tasks_data['data']['docs']  # Return the list of tasks

            except json.JSONDecodeError as e:
                print(f"JSON response parsing error: {e}")
                print("Raw Content:", response.content.decode('utf-8', errors='replace'))
        else:
            print("Error fetching tasks, status code:", response.status_code)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    return None  # Return None if tasks could not be fetched

def clear_task(first_task_id, linkquest, status, task_title):
    print(f"Attempting to clear task with ID: {first_task_id}")
    print(f"Opening task link: {linkquest}")

    # Open the link in a browser
    webbrowser.open(linkquest)
    print(f"Opened the task link: {linkquest}")
    time.sleep(10)  # Wait for 10 seconds

    # Read token and At value again for headers
    tg, at = read_token_and_at()
    
    # Check task status and handle accordingly
    if status == "in-progress":
        # Claim the reward
        claim_url = f"https://appipa.fomo.fund/v1/profile/tasks/{first_task_id}/claim"
        payload = {"id": first_task_id}

        # Construct headers for the claim request
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9",
            "At": at,
            "content-length": "33",  # Set content length dynamically
            "content-type": "application/json",
            "origin": "https://app.fomo.fund",
            "priority": "u=1, i",
            "referer": "https://app.fomo.fund/",
            "sec-ch-ua": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129", "Microsoft Edge WebView2";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "tg": tg,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
        }

        claim_response = requests.post(claim_url, json=payload, headers=headers)

        if claim_response.status_code == 200:
            claim_data = claim_response.json()
            if claim_data.get("status") == "ok" and claim_data["data"].get("status") == "ok":
                print("Claim successful!")
            else:
                print("Task already claimed or error:", claim_data)
        else:
            print("Error claiming reward, status code:", claim_response.status_code)
            print("Response:", claim_response.json())  # Show the full response for debugging

    elif status == "claim":
        print(f"The task '{task_title}' has already been claimed.")
    elif status == "pending":
        print(f"Please complete the task '{task_title}' manually.")
    else:
        print(f"Unexpected task status: {status}")


def check_points():
    url = "https://appipa.fomo.fund/v1/profile"
    tg, at = read_token_and_at()

    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9",
        "At": at,
        "origin": "https://app.fomo.fund",
        "priority": "u=1, i",
        "referer": "https://app.fomo.fund/",
        "sec-ch-ua": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129", "Microsoft Edge WebView2";v="129"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "tg": tg,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        user_info = response.json()
        print("Total Points:", user_info['data'].get('points', {}).get('$numberDecimal', '0'))
    else:
        print("Error fetching user points.")

if __name__ == "__main__":
    check_user_info()
    tasks = fetch_tasks()  # Store the fetched tasks for later use

    if tasks:
        # Iterate through the tasks and clear each one
        for task in tasks:
            if task['status'] == "in-progress":  # Check if the task is still pending
                clear_task(task['_id'], task['link'], task['status'], task['title'])  # Pass task title to clear_task
            elif task['status'] == "claim":
                print(f"The task '{task['title']}' has already been claimed.")
            elif task['status'] == "pending":
                print(f"Please complete the task '{task['title']}' manually.")
            else:
                print(f"Task {task['_id']} is not pending. Skipping.")
                print(f"Unexpected task status: {task['status']}")
    else:
        print("No active tasks available.")
