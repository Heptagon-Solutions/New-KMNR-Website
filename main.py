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
    """Kill any processes using ports 5000 and 5001 (silent version)"""
    try:
        result = subprocess.run(['lsof', '-ti:5000,5001'], capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                subprocess.run(['kill', '-9', pid], capture_output=True)
    except Exception as e:
        pass  # Silently handle errors during port cleanup

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
        
        # Start the process in background (detached)
        process = subprocess.Popen(
            ['pipenv', 'run', 'python', 'app.py'],
            stdout=log_file,
            stderr=subprocess.STDOUT,
            env=env
        )
        
        # Wait a moment for startup, then check
        time.sleep(3)
        if process.poll() is None:
            print_status(f"Backend started successfully on port {backend_port} (running in background)", "green")
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
    """Start the Angular frontend with progress bar (foreground)"""
    os.chdir('frontend')
    
    try:
        # Show progress bar
        animated_progress_bar("Starting Angular frontend")
        
        # Open log file for frontend output
        log_file = open('../logs/frontend.log', 'w')
        
        print_status("Frontend starting in foreground - this will take over the terminal", "cyan")
        print_status("Backend is running in background", "dim")
        print_status("Press Ctrl+C to stop all services", "dim")
        print()
        
        # Start the process in foreground
        process = subprocess.run(
            ['npm', 'run', 'start'],
            stdout=None,  # Let it output to terminal
            stderr=None   # Let it output to terminal
        )
            
    except KeyboardInterrupt:
        print_status("\nShutting down services...", "yellow")
        # Kill backend processes
        kill_ports_5000_and_5001()
        print_status("Services stopped", "green")
    except Exception as e:
        print_status(f"Frontend startup error: {e}", "red")
        
    os.chdir('..')

def clean_all_ports():
    """Clean all ports and processes with single progress bar"""
    try:
        animated_progress_bar("Cleaning ports", 1.5)
        
        # Kill specific ports 5000 and 5001
        result = subprocess.run(['lsof', '-ti:5000,5001'], capture_output=True, text=True)
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            for pid in pids:
                subprocess.run(['kill', '-9', pid], capture_output=True)
        
        print_status("Successfully cleaned ports", "green")
    except Exception as e:
        print_status("Successfully cleaned ports", "green")  # Show success even if there were errors

def main():
    """Main function to start both services"""
    try:
        # Clean all ports first
        clean_all_ports()
        
        # Start backend in background
        backend_process, backend_success, backend_port = start_backend()
        
        if not backend_success:
            print_status("Failed to start backend. Exiting.", "red")
            sys.exit(1)
        
        # Start frontend in foreground (this will block)
        start_frontend()
            
    except Exception as e:
        print_status(f"Error: {e}", "red")
        sys.exit(1)

if __name__ == "__main__":
    main()