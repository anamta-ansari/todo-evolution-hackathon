# start_all.py (in project root)
import subprocess
import sys
import os
import time
import signal

def start_backend():
    """Start the FastAPI backend server"""
    print("🔧 Starting Backend Server...")
    
    # Change to backend directory
    backend_dir = os.path.join(os.getcwd(), "backend")
    
    if sys.platform == 'win32':
        # Windows
        return subprocess.Popen(
            [sys.executable, "start_server.py"],
            cwd=backend_dir,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    else:
        # Unix-like systems
        return subprocess.Popen(
            [sys.executable, "start_server.py"],
            cwd=backend_dir
        )

def start_frontend():
    """Start the Next.js frontend server"""
    print("⚡ Starting Frontend Server...")
    
    # Change to frontend directory
    frontend_dir = os.path.join(os.getcwd(), "frontend")
    
    if sys.platform == 'win32':
        # Windows
        return subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            creationflags=subprocess.CREATE_NEW_CONSOLE,
            shell=True
        )
    else:
        # Unix-like systems
        return subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir
        )

def main():
    print("=" * 60)
    print("🚀 Phase III - AI Todo Chatbot - Development Servers")
    print("=" * 60)
    print()
    
    # Check if .env files exist
    backend_env = os.path.join("backend", ".env")
    frontend_env = os.path.join("frontend", ".env.local")
    
    if not os.path.exists(backend_env):
        print(f"⚠️  Warning: {backend_env} not found")
    
    if not os.path.exists(frontend_env):
        print(f"⚠️  Warning: {frontend_env} not found")
    
    print()
    
    try:
        # Start backend
        backend_process = start_backend()
        print("✅ Backend starting... (wait 5 seconds)")
        time.sleep(5)
        
        # Start frontend
        frontend_process = start_frontend()
        print("✅ Frontend starting... (wait 5 seconds)")
        time.sleep(5)
        
        print()
        print("=" * 60)
        print("🎉 Both servers are running!")
        print("=" * 60)
        print()
        print("📍 Backend API:  http://localhost:8000")
        print("📚 API Docs:     http://localhost:8000/docs")
        print("💚 Health Check: http://localhost:8000/health")
        print()
        print("🌐 Frontend UI:  http://localhost:3000")
        print("💬 Chat Page:    http://localhost:3000/chat")
        print()
        print("Press CTRL+C to stop both servers")
        print("=" * 60)
        
        # Wait for processes
        backend_process.wait()
        frontend_process.wait()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down servers...")
        
        # Terminate processes
        if 'backend_process' in locals():
            backend_process.terminate()
        if 'frontend_process' in locals():
            frontend_process.terminate()
        
        print("✅ Servers stopped")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()