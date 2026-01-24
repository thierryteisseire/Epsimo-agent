
import os
import sys
import argparse
import requests
import json
import time
from scripts.auth import get_token, API_BASE_URL

# Make sure we can import from scripts
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_verification():
    print("🚀 Starting EpsimoAI Skill Verification")
    
    # Auth
    print("\n🔑 Verifying Authentication...")
    try:
        from scripts.auth import get_token
        # This will prompt if needed or use existing token
        token = get_token()
        print("✅ Authentication successful.")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        print("Try running `python3 .agent/skills/epsimo-agent/scripts/auth.py login` first.")
        return

    # 3. Create Project
    print("\nPs Creating Test Project...")
    project_id = None
    try:
        headers = {"Authorization": f"Bearer {token}"}
        payload = {"name": "Skill Verification Project", "description": "Temporary project for verification"}
        resp = requests.post(f"{API_BASE_URL}/projects/", headers=headers, json=payload)
        resp.raise_for_status()
        project = resp.json()
        project_id = project['project_id']
        print(f"✅ Created project: {project['name']} ({project_id})")
    except Exception as e:
        print(f"❌ Project creation failed: {e}")
        return

    try:
        # Get Project Token
        print("\n🎫 Getting Project Token...")
        resp = requests.get(f"{API_BASE_URL}/projects/{project_id}", headers=headers)
        resp.raise_for_status()
        data = resp.json()
        project_token = data.get('access_token') or data.get('token') or data.get('jwt_token')
        proj_headers = {"Authorization": f"Bearer {project_token}"}
        print("✅ Obtained project token.")

        # 4. Create Assistant
        print("\n🤖 Creating Test Assistant...")
        asst_payload = {
            "name": "Test Agent", 
            "config": {
                "instructions": "You are a test agent.",
                "model": "gpt-4o"
            },
            "public": False
        }
        resp = requests.post(f"{API_BASE_URL}/assistants/", headers=proj_headers, json=asst_payload)
        resp.raise_for_status()
        assistant = resp.json()
        print(f"✅ Created assistant: {assistant['name']} ({assistant['assistant_id']})")

        # 5. Create Thread
        print("\n🧵 Creating Test Thread...")
        thread_payload = {"name": "Test Thread"}
        resp = requests.post(f"{API_BASE_URL}/threads/", headers=proj_headers, json=thread_payload)
        resp.raise_for_status()
        thread = resp.json()
        print(f"✅ Created thread: {thread['name']} ({thread['thread_id']})")
        
        # 6. List Items (Verification)
        print("\n📋 Verifying Lists...")
        # Check Project List
        resp = requests.get(f"{API_BASE_URL}/projects/", headers=headers)
        projects = resp.json()
        if any(p['project_id'] == project_id for p in projects):
             print("✅ Project found in list.")
        else:
             print("❌ Project NOT found in list.")
             
    except Exception as e:
        print(f"❌ Verification steps failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 7. Cleanup
        if project_id:
            print("\n🧹 Cleaning up...")
            try:
                # Need to use main token for this, but switch context usually
                # Delete project
                # Using main token 
                del_url = f"{API_BASE_URL}/projects/{project_id}?confirm=true"
                resp = requests.delete(del_url, headers=headers)
                if resp.status_code in [200, 204]:
                    print("✅ Project deleted.")
                else:
                    print(f"⚠️ Failed to delete project: {resp.status_code} {resp.text}")
            except Exception as e:
                print(f"⚠️ Cleanup failed: {e}")

    print("\n✨ Verification Complete.")

if __name__ == "__main__":
    run_verification()
