
import os
import sys
import argparse
import requests
import json
from auth import get_token, API_BASE_URL

def create_assistant(project_id, name, instructions, model, tools=None):
    token = get_token()
    
    # Get project specific token
    auth_headers = {"Authorization": f"Bearer {token}"}
    proj_resp = requests.get(f"{API_BASE_URL}/projects/{project_id}", headers=auth_headers)
    proj_resp.raise_for_status()
    data = proj_resp.json()
    project_token = data.get('access_token') or data.get('token') or data.get('jwt_token')
    
    headers = {"Authorization": f"Bearer {project_token}"}
    
    config = {
        "system_prompt": instructions,
        "model": model,
        "type": "agent",
        "configurable": {
             "type": "agent",
             "agent_type": "agent"
        },
        "tools": tools if tools is not None else ["tavily"]
    }
    
    payload = {
        "name": name,
        "config": config,
        "public": True 
    }
    
    response = requests.post(f"{API_BASE_URL}/assistants/", headers=headers, json=payload)
    response.raise_for_status()
    print(json.dumps(response.json(), indent=2))

def list_assistants(project_id):
    token = get_token()
    
    # Get project specific token
    auth_headers = {"Authorization": f"Bearer {token}"}
    proj_resp = requests.get(f"{API_BASE_URL}/projects/{project_id}", headers=auth_headers)
    proj_resp.raise_for_status()
    data = proj_resp.json()
    project_token = data.get('access_token') or data.get('token') or data.get('jwt_token')

    headers = {"Authorization": f"Bearer {project_token}"}
    response = requests.get(f"{API_BASE_URL}/assistants/", headers=headers)
    response.raise_for_status()
    print(json.dumps(response.json(), indent=2))

def main():
    parser = argparse.ArgumentParser(description="Manage EpsimoAI Assistants")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # List
    list_parser = subparsers.add_parser("list", help="List assistants in a project")
    list_parser.add_argument("--project-id", required=True, help="Project ID")

    # Create
    create_parser = subparsers.add_parser("create", help="Create a new assistant")
    create_parser.add_argument("--project-id", required=True, help="Project ID")
    create_parser.add_argument("--name", required=True, help="Assistant name")
    create_parser.add_argument("--instructions", required=True, help="System instructions")
    create_parser.add_argument("--model", default="gpt-4o", help="Model name (default: gpt-4o)")
    create_parser.add_argument("--no-tools", action="store_true", help="Create assistant without any tools")

    args = parser.parse_args()

    if args.command == "list":
        list_assistants(args.project_id)
    elif args.command == "create":
        tools = [] if args.no_tools else None
        create_assistant(args.project_id, args.name, args.instructions, args.model, tools=tools)

if __name__ == "__main__":
    main()
