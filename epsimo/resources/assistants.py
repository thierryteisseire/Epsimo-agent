class Assistants:
    def __init__(self, client):
        self.client = client

    def list(self, project_id):
        """List assistants in a project."""
        headers = self.client.get_project_headers(project_id)
        return self.client.request("GET", "/assistants/", headers=headers)

    def create(self, project_id, name, model="gpt-4o", instructions="", tools=None, public=False):
        """Create a new assistant."""
        headers = self.client.get_project_headers(project_id)
        
        # Construct configurable config
        configurable = {
            "type": "agent",
            "type==agent/agent_type": "GPT-4O", # legacy/specific key
            "type==agent/model": model,
            "type==agent/system_message": instructions,
        }
        
        if tools:
            # Normalize tools format if needed, or assume list of dicts
            # The API expects specific structure
             configurable["type==agent/tools"] = tools

        payload = {
            "name": name,
            "config": {"configurable": configurable},
            "public": public
        }
        return self.client.request("POST", "/assistants/", json=payload, headers=headers)

    def get(self, project_id, assistant_id):
        """Get assistant details."""
        headers = self.client.get_project_headers(project_id)
        return self.client.request("GET", f"/assistants/{assistant_id}", headers=headers)

    def update(self, project_id, assistant_id, payload):
        """Update assistant settings."""
        headers = self.client.get_project_headers(project_id)
        return self.client.request("PUT", f"/assistants/{assistant_id}", json=payload, headers=headers)

    def delete(self, project_id, assistant_id):
        """Delete an assistant."""
        headers = self.client.get_project_headers(project_id)
        return self.client.request("DELETE", f"/assistants/{assistant_id}", headers=headers)
