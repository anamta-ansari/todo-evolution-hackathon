# check_env.py
import os
from pathlib import Path

def check_env_file(file_path, required_vars):
    """Check if .env file exists and has required variables"""
    print(f"\nChecking: {file_path}")

    if not os.path.exists(file_path):
        print(f"  ERROR: File not found!")
        return False

    print(f"  OK: File exists")

    # Read .env file
    with open(file_path, 'r') as f:
        content = f.read()

    missing = []
    for var in required_vars:
        if var not in content or f"{var}=" not in content:
            missing.append(var)
        else:
            # Check if value is set (not empty)
            for line in content.split('\n'):
                if line.startswith(f"{var}="):
                    value = line.split('=', 1)[1].strip()
                    if value and value != "your-key-here":
                        print(f"  OK: {var} is set")
                    else:
                        print(f"  WARNING: {var} is empty or placeholder")
                        missing.append(var)

    if missing:
        print(f"  ERROR: Missing or empty: {', '.join(missing)}")
        return False

    return True

def main():
    print("=" * 60)
    print("Environment Variables Check")
    print("=" * 60)

    # Backend .env
    backend_required = ["DATABASE_URL", "BETTER_AUTH_SECRET", "OPENAI_API_KEY"]
    backend_ok = check_env_file("backend/.env", backend_required)

    # Frontend .env.local
    frontend_required = ["NEXT_PUBLIC_API_URL", "BETTER_AUTH_SECRET"]
    frontend_ok = check_env_file("frontend/.env.local", frontend_required)

    print("\n" + "=" * 60)
    if backend_ok and frontend_ok:
        print("SUCCESS: All environment variables are configured!")
        print("=" * 60)
        print("\nYou can now run: python start_all.py")
    else:
        print("FAILURE: Some environment variables are missing or empty")
        print("=" * 60)
        print("\nPlease configure the missing variables and try again.")

        if not backend_ok:
            print("\nBackend .env template:")
            print("DATABASE_URL=postgresql://user:pass@host:5432/dbname")
            print("BETTER_AUTH_SECRET=your-secret-key-here")
            print("OPENAI_API_KEY=sk-your-openai-key-here")

        if not frontend_ok:
            print("\nFrontend .env.local template:")
            print("NEXT_PUBLIC_API_URL=http://localhost:8000")
            print("BETTER_AUTH_SECRET=your-secret-key-here")
            print("NEXT_PUBLIC_OPENAI_DOMAIN_KEY=optional-for-localhost")

if __name__ == "__main__":
    main()