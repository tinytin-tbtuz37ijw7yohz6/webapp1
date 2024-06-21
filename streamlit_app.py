import streamlit as st
import subprocess
import threading
import time

# Function to run shell commands
def run_shell_command(command):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        return output.decode(), error.decode()
    except Exception as e:
        return "", str(e)

# Function to install tmate and run it
def install_and_run_tmate():
    st.write("Updating system and installing tmate...")
    update_command = "sudo apt update"
    install_command = "sudo apt install tmate -y"
    
    update_output, update_error = run_shell_command(update_command)
    st.write("System Update Output:")
    st.text(update_output)
    if update_error:
        st.write("System Update Error:")
        st.text(update_error)
    
    install_output, install_error = run_shell_command(install_command)
    st.write("tmate Installation Output:")
    st.text(install_output)
    if install_error:
        st.write("tmate Installation Error:")
        st.text(install_error)

    st.write("Running tmate...")
    tmate_command = "tmate"
    tmate_output, tmate_error = run_shell_command(tmate_command)
    st.write("tmate Output:")
    st.text(tmate_output)
    if tmate_error:
        st.write("tmate Error:")
        st.text(tmate_error)

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
