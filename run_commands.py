import subprocess

def run_command(command):
    """Run a command using subprocess."""
    try:
        subprocess.run(command, check=True)
        print(f"Successfully executed: {' '.join(command)}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing: {' '.join(command)}")

def main():
    commands = [
        ["python", "scrape/scrape.py"],
        ["python", "data_processing/process_data.py"],
        ["streamlit", "run", "app/dashboard.py"]
    ]

    for command in commands:
        run_command(command)

if __name__ == "__main__":
    main()
