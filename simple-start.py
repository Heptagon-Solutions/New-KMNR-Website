#!/usr/bin/env python3

import subprocess
import time
import os
import sys
import argparse

def print_status(message, style="white"):
    """Simple print function to replace rich console"""
    styles = {
        "green": "\033[92m",
        "red": "\033[91m", 
        "yellow": "\033[93m",
        "cyan": "\033[96m",
        "purple": "\033[95m",
        "dim": "\033[90m",
        "white": "\033[97m"
    }
    reset = "\033[0m"
    print(f"{styles.get(style, '')}{message}{reset}")

def animated_progress_bar(desc="Progress", duration=2):
    """Animated purple progress bar that disappears when complete"""
    import sys
    
    print_status(f"{desc}...", "purple")
    
    bar_length = 40
    purple = "\033[95m"
    reset = "\033[0m"
    
    for i in range(bar_length + 1):
        percent = (i / bar_length) * 100
        filled = '█' * i
        empty = '░' * (bar_length - i)
        
        sys.stdout.write(f'\r{purple}[{filled}{empty}] {percent:.0f}%{reset}')
        sys.stdout.flush()
        
        if i < bar_length:
            import time
            time.sleep(duration / bar_length)
    
    # Clear the progress bar line
    sys.stdout.write('\r' + ' ' * (bar_length + 10) + '\r')
    sys.stdout.flush()
    
    return True

def check_port_available(port):
    """Check if a port is available"""
    try:
        result = subprocess.run(['lsof', '-ti:' + str(port)], 
                              capture_output=True, text=True)
        return len(result.stdout.strip()) == 0
    except:
        return True

def kill_ports_5000_and_5001():
    """Kill any processes using ports 5000 and 5001"""
    try:
        print_status("Killing processes on ports 5000 and 5001...", "yellow")
        result = subprocess.run(['lsof', '-ti:5000,5001'], capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                subprocess.run(['kill', '-9', pid], capture_output=True)
            print_status("Killed processes on ports 5000 and 5001", "green")
        else:
            print_status("Ports 5000 and 5001 are already free", "green")
    except Exception as e:
        print_status(f"Warning: Error killing port processes: {e}", "yellow")

def get_available_backend_port():
    """Get an available port for backend (always kill ports first, then use 5001)"""
    kill_ports_5000_and_5001()
    return 5001

def start_backend():
    """Start the Flask backend with progress bar"""
    backend_port = get_available_backend_port()
    if backend_port is None:
        return None, False
        
    os.chdir('backend')
    
    try:
        # Show progress bar
        print()
        animated_progress_bar("Starting Flask backend")
        
        # Set the port environment variable
        env = os.environ.copy()
        env['FLASK_RUN_PORT'] = str(backend_port)
        
        # Open log file for backend output
        log_file = open('../logs/backend.log', 'w')
        
        # Start the process
        process = subprocess.Popen(
            ['pipenv', 'run', 'python', 'app.py'],
            stdout=log_file,
            stderr=subprocess.STDOUT,
            env=env
        )
        
        # Wait a moment for startup, then check
        time.sleep(3)
        if process.poll() is None:
            print_status(f"Backend started successfully on port {backend_port}", "green")
            print()
            success = True
        else:
            print_status("Backend failed to start", "red")
            print()
            success = False
            
    except Exception as e:
        print_status(f"Backend startup error: {e}", "red")
        success = False
        process = None
        
    os.chdir('..')
    return process, success, backend_port

def start_frontend():
    """Start the Angular frontend with progress bar"""
    os.chdir('frontend')
    
    try:
        # Show progress bar
        animated_progress_bar("Starting Angular frontend")
        
        # Open log file for frontend output
        log_file = open('../logs/frontend.log', 'w')
        
        # Start the process
        process = subprocess.Popen(
            ['npm', 'run', 'start'],
            stdout=log_file,
            stderr=subprocess.STDOUT
        )
        
        # Check immediately if process started
        if process.poll() is None:
            print_status("Frontend started successfully", "green")
            print()
            success = True
        else:
            print_status("Frontend starting (may take longer)", "yellow")
            success = True  # npm start can be slow but still succeed
        
        # Wait for frontend to fully initialize
        time.sleep(5)
            
    except Exception as e:
        print_status(f"Frontend startup error: {e}", "red")
        success = False
        process = None
        
    os.chdir('..')
    return process, success

def kill_existing_processes():
    """Kill existing processes using the kill-processes.sh script"""
    try:
        print_status("Killing existing processes...", "yellow")
        result = subprocess.run(['./kill-processes.sh'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print_status("Existing processes terminated", "green")
        else:
            print_status("Warning: Could not kill existing processes", "yellow")
    except Exception as e:
        print_status(f"Warning: Error killing processes: {e}", "yellow")

def main():
    """Main function to start both services"""
    parser = argparse.ArgumentParser(description="Start KMNR website services")
    parser.add_argument('--do-not-open-browser', action='store_true', 
                       help='Do not automatically open browser after starting services')
    
    args = parser.parse_args()
    
    try:
        # Kill existing processes first
        kill_existing_processes()
        # Start backend
        result = start_backend()
        if len(result) == 3:
            backend_process, backend_success, backend_port = result
        else:
            backend_process, backend_success = result
            backend_port = 5000
        
        # Start frontend
        frontend_process, frontend_success = start_frontend()
        
        # Open browser immediately (unless flag is set)
        if frontend_success and not args.do_not_open_browser:
            subprocess.run(['/usr/bin/open', 'http://localhost:4200'], check=False)
        
        print_status("Frontend: http://localhost:4200", "white")
        print_status(f"Backend: http://127.0.0.1:{backend_port}", "white")
        print()
        print_status("python3 simple-start.py --do-not-open-browser", "dim")
        print_status("\nPress Ctrl+C to stop all services", "dim")
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print_status("\nShutting down...", "yellow")
            if backend_process:
                backend_process.terminate()
            if frontend_process:
                frontend_process.terminate()
            print_status("Services stopped", "green")
            
    except Exception as e:
        print_status(f"Error: {e}", "red")
        sys.exit(1)

if __name__ == "__main__":
    main()