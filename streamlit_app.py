import streamlit as st
import subprocess
import threading
import time
import queue

# Function to run shell commands
def run_shell_command(command, output_queue):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        output_queue.put((output.decode(), error.decode()))
    except Exception as e:
        output_queue.put(("", str(e)))

# Function to install tmate and run it
def install_and_run_tmate(output_queue):
    output_queue.put("Updating system and installing tmate...")
    
    update_command = "sudo apt update"
    install_command = "sudo apt install tmate -y"
    
    run_shell_command(update_command, output_queue)
    run_shell_command(install_command, output_queue)

    output_queue.put("Running tmate...")
    tmate_command = "tmate"
    run_shell_command(tmate_command, output_queue)

# Function to manage the running time of the app
def manage_runtime(duration_in_seconds):
    st.write("The application will run for 1 week maximum.")
    time.sleep(duration_in_seconds)
    st.write("Stopping the application as the maximum runtime is reached.")

# Main function
def main():
    st.title("System Update and tmate Installation")

    output_queue = queue.Queue()

    # Creating a separate thread to run the install and run tmate function
    tmate_thread = threading.Thread(target=install_and_run_tmate, args=(output_queue,))
    tmate_thread.start()

    # Displaying outputs in the main thread
    while tmate_thread.is_alive() or not output_queue.empty():
        while not output_queue.empty():
            message = output_queue.get()
            if isinstance(message, tuple):
                output, error = message
                if output:
                    st.write("Output:")
                    st.text(output)
                if error:
                    st.write("Error:")
                    st.text(error)
            else:
                st.write(message)
        time.sleep(1)

    # Run the app for 1 week (7 days * 24 hours * 60 minutes * 60 seconds)
    max_runtime_seconds = 7 * 24 * 60 * 60
    manage_runtime(max_runtime_seconds)

if __name__ == "__main__":
    main()
