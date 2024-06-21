import streamlit as st
import subprocess
import threading
import time

# Function to run shell commands
def run_shell_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output, error

# Function to install tmate and run it
def install_and_run_tmate():
    st.write("Updating system and installing tmate...")
    update_command = "sudo apt update && sudo apt install tmate -y"
    output, error = run_shell_command(update_command)
    st.write("System Update and tmate Installation Output:")
    st.text(output.decode())
    st.write("System Update and tmate Installation Error (if any):")
    st.text(error.decode())

    st.write("Running tmate...")
    tmate_command = "tmate"
    output, error = run_shell_command(tmate_command)
    st.write("tmate Output:")
    st.text(output.decode())
    st.write("tmate Error (if any):")
    st.text(error.decode())

# Function to manage the running time of the app
def manage_runtime(duration_in_seconds):
    st.write("The application will run for 1 week maximum.")
    time.sleep(duration_in_seconds)
    st.write("Stopping the application as the maximum runtime is reached.")

# Main function
def main():
    st.title("System Update and tmate Installation")

    # Creating a separate thread to run the install and run tmate function
    tmate_thread = threading.Thread(target=install_and_run_tmate)
    tmate_thread.start()

    # Run the app for 1 week (7 days * 24 hours * 60 minutes * 60 seconds)
    max_runtime_seconds = 7 * 24 * 60 * 60
    manage_runtime(max_runtime_seconds)

    # Stop the tmate thread after the runtime is over
    if tmate_thread.is_alive():
        st.write("Stopping tmate process...")
        tmate_thread.join(timeout=1)
        st.write("tmate process stopped.")

if __name__ == "__main__":
    main()
