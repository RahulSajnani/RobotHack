import subprocess
import time

# --- BEGIN CONFIGURATION ---

HF_USERNAME = "rohanc007" 
FOLLOWER_ARM_PORT = "so101_follower" #todo
CAMERA_DEVICE_URL = "http://" #todo

POLICY_PATHS = {
    "pick_lid": "path/to/your/open_lid_policy",
    "remove_debris": "path/to/your/remove_debris_policy",
    "drop_lid": "path/to/your/replace_lid_policy",
}

PROMPTS = {
    "pick_lid": "Pick the lid with the red cross and place it on the side.",
    "remove_debris": "remove the debris",
    "drop_lid": "Pick the lid with the red cross from the side and place it on top of the hole.",
}

# How long (in seconds) to run each policy before assuming it's done.
TASK_DURATIONS = {
    "pick_lid": 60,      
    "remove_debris": 60, 
    "drop_lid": 60,   
}

# This could be a local device like "/dev/video0" or your phone's URL.
CAMERA_DEVICE = "http://10.0.0.114:4747/video" 

# --- END OF CONFIGURATION ---


def run_robot_task(task_name: str):
    """
    Constructs and runs the lerobot RECORD command for a specific evaluation task.
    """
    if task_name not in POLICY_PATHS:
        print(f"Error: Task '{task_name}' not found in configuration.")
        return

    policy_path = POLICY_PATHS[task_name]
    prompt = PROMPTS[task_name]
    duration = TASK_DURATIONS[task_name]
    
    # Define a repo_id for the evaluation dataset we are recording
    eval_repo_id = f"{HF_USERNAME}/eval-{task_name}-{int(time.time())}"

    print("\n" + "="*50)
    print(f"Executing Task: {task_name.replace('_', ' ').title()}")
    print(f"  - Using Policy: {policy_path}")
    print(f"  - With Task Prompt: '{prompt}'")
    print(f"  - Saving evaluation to: {eval_repo_id}")
    print(f"  - Running for: {duration} seconds")
    print("="*50 + "\n")

    # This is the command that will be run in the terminal.
    # We use `lerobot.record` for evaluation, passing the policy path to it.
    command = [
        "python",
        "-m",
        "lerobot.record",
        f"--robot.type=so101_follower",
        f"--robot.port={FOLLOWER_ARM_PORT}",
        f'--robot.cameras={{main:{{type:opencv,index_or_path:"{CAMERA_DEVICE_URL}"}}}}',
        f"--display_data=false",
        f"--dataset.repo_id={eval_repo_id}",
        f'--dataset.single_task="{prompt}"',
        f"--policy.path={policy_path}",
    ]

    try:
        print("Starting robot evaluation... Press Ctrl+C in this terminal to stop early.")
        # We use subprocess.run here which is a bit cleaner for this use case
        subprocess.run(command, timeout=duration, check=True)
        print(f"\nTask timer finished ({duration}s). Assuming completion.")

    except subprocess.TimeoutExpired:
        print(f"\nTask timer finished ({duration}s). Assuming completion.")
        # In a real scenario, the process is already killed by timeout.
        print("Task completed.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred in the lerobot script: {e}")

    except KeyboardInterrupt:
        print("\nUser requested stop. Terminating policy.")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



def main_menu():
    """
    Displays the main menu and handles user input.
    """
    while True:
        print("\n--- CivicBot Control Menu ---")
        print("1. Pick Lid")
        print("2. Remove Debris")
        print("3. Drop Lid")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            run_robot_task("open_lid")
        elif choice == '2':
            run_robot_task("remove_debris")
        elif choice == '3':
            run_robot_task("replace_lid")
        elif choice == '4':
            print("Exiting manhole controller. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
