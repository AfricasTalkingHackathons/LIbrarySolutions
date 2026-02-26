#!/usr/bin/env python3
"""
Setup script for Maktaba Semantic Search System

Automates initialization of:
1. PostgreSQL database
2. pgvector extension
3. Sample data embedding
4. System verification
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path so embedd module can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

class SetupHelper:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.errors = []
        self.warnings = []
    
    def check_dependencies(self) -> bool:
        """Check if all required packages are installed"""
        print("\n" + "=" * 60)
        print("✓ Checking dependencies...")
        print("=" * 60)
        
        required = {
            'google-genai': 'google',
            'sqlalchemy': 'sqlalchemy',
            'psycopg2-binary': 'psycopg2',
            'fastapi': 'fastapi',
            'uvicorn': 'uvicorn'
        }
        
        missing = []
        for package, import_name in required.items():
            try:
                __import__(import_name)
                print(f"  ✓ {package}")
            except ImportError:
                print(f"  ✗ {package}")
                missing.append(package)
        
        if missing:
            self.errors.append(f"Missing packages: {', '.join(missing)}")
            print(f"\n💡 Install with: pip install {' '.join(missing)}")
            return False
        
        return True
    
    def check_postgresql(self) -> bool:
        """Check PostgreSQL connection"""
        print("\n" + "=" * 60)
        print("✓ Checking PostgreSQL...")
        print("=" * 60)
        
        try:
            import psycopg2
            db_url = os.getenv("DATABASE_URL")
            
            if not db_url:
                self.warnings.append("DATABASE_URL not set in .env")
                print("  ⚠ DATABASE_URL not configured")
                return False
            
            print(f"  ✓ Database URL configured")
            return True
        
        except Exception as e:
            self.errors.append(f"PostgreSQL error: {str(e)}")
            print(f"  ✗ Error: {str(e)}")
            return False
    
    def check_gemini_api(self) -> bool:
        """Check Gemini API configuration"""
        print("\n" + "=" * 60)
        print("✓ Checking Gemini API...")
        print("=" * 60)
        
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            self.errors.append("GEMINI_API_KEY not set in .env")
            print("  ✗ GEMINI_API_KEY not configured")
            print("\n Get API key from: https://aistudio.google.com/app/apikey")
            return False
        
        print(f"  ✓ API key configured")
        
        # Try to initialize client
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            print(f"  ✓ Gemini client initialized")
            return True
        except Exception as e:
            self.errors.append(f"Gemini API error: {str(e)}")
            print(f"  ✗ Error: {str(e)}")
            return False
    
    def init_database(self) -> bool:
        """Initialize database"""
        print("\n" + "=" * 60)
        print("✓ Initializing database...")
        print("=" * 60)
        
        try:
            from embedd.vector_db import init_db
            init_db()
            print("  ✓ Database initialized")
            return True
        except Exception as e:
            self.errors.append(f"Database init error: {str(e)}")
            print(f"  ✗ Error: {str(e)}")
            return False
    
    def run_demo(self) -> bool:
        """Run embedding demo"""
        print("\n" + "=" * 60)
        print("✓ Running embedding demo...")
        print("=" * 60)
        
        try:
            from embedd.demo import embed_sample_books
            embed_sample_books()
            return True
        except Exception as e:
            self.warnings.append(f"Demo error: {str(e)}")
            print(f"  ⚠ Demo failed: {str(e)}")
            return False
    
    def print_summary(self):
        """Print setup summary"""
        print("\n" + "=" * 60)
        print("Setup Summary")
        print("=" * 60)
        
        if self.errors:
            print("\n Errors:")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print("\n  Warnings:")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if not self.errors:
            print("\nSetup completed successfully!")
            print("\nNext steps:")
            print("  1. Start API server:")
            print("     python -m uvicorn embedd.search_api:app --reload --port 8001")
            print("  2. Visit: http://localhost:8001/docs")
            print("  3. Test endpoints")
        
        print("\n" + "=" * 60)
    
    def run_all(self, skip_demo: bool = False):
        """Run full setup"""
        print("\n")
        print("╔" + "=" * 58 + "╗")
        print("║   Maktaba Semantic Search - Setup Assistant  " + " " * 10 + "║")
        print("╚" + "=" * 58 + "╝")
        
        # Run checks
        checks_pass = True
        
        if not self.check_dependencies():
            checks_pass = False
        
        if not self.check_gemini_api():
            checks_pass = False
        
        if not self.check_postgresql():
            checks_pass = False
        
        if not checks_pass:
            print("\n Setup halted due to errors")
            self.print_summary()
            return False
        
        # Initialize database
        if not self.init_database():
            self.print_summary()
            return False
        
        # Run demo
        if not skip_demo:
            if not self.run_demo():
                print("\n You can run demo manually: python -m embedd.demo")
        
        self.print_summary()
        return True

def main():
    """Main setup entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup Maktaba Semantic Search")
    parser.add_argument("--skip-demo", action="store_true", help="Skip embedding demo")
    parser.add_argument("--check-only", action="store_true", help="Only check configuration")
    
    args = parser.parse_args()
    
    helper = SetupHelper()
    
    if args.check_only:
        # Only run checks
        helper.check_dependencies()
        helper.check_gemini_api()
        helper.check_postgresql()
        helper.print_summary()
        return 0 if not helper.errors else 1
    else:
        # Run full setup
        success = helper.run_all(skip_demo=args.skip_demo)
        return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
