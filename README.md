# Epsimo Agent Framework

> **Beta Release** — Build sophisticated AI-powered applications with agents, persistent threads, and Virtual Database state management.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](https://github.com/thierryteisseire/epsimo-agent)
[![Skills](https://img.shields.io/badge/skills.sh-epsimo--agent-purple.svg)](https://skills.sh)
[![npm](https://img.shields.io/badge/npm-epsimo--agent-red.svg)](https://www.npmjs.com/package/epsimo-agent)

The Epsimo Agent Framework provides a unified **CLI**, **Python SDK**, and **React UI Kit** for building AI applications with:
- 🤖 Multi-agent orchestration
- 💾 Virtual Database (thread-based persistent state)
- 💬 Streaming conversations with tool support
- 🎨 Pre-built React components
- 🔌 Extensible tool library

**Base URL:** `https://api.epsimoagents.com`  
**Frontend:** `https://app.epsimoagents.com`

---

## 📦 Installation

### For AI Coding Agents (Recommended)

Install as a skill for Claude Code, Cursor, Cline, Windsurf, and 30+ other AI coding agents:

```bash
npx skills add thierryteisseire/epsimo-agent
```

This installs the skill across all your AI agents in one command! The skill helps agents:
- Set up Epsimo projects quickly
- Manage agents and threads
- Query the Virtual Database
- Deploy configurations
- Handle authentication flows

### npm Package (Global Installation)

```bash
npm install -g epsimo-agent
```

### Python SDK & CLI

```bash
# Install from PyPI (coming soon)
pip install epsimo-agent

# Or install from source
git clone https://github.com/thierryteisseire/epsimo-agent.git
cd epsimo-agent
pip install -r requirements.txt

# Make CLI executable
chmod +x epsimo/cli.py
export PATH="$PATH:$(pwd)/epsimo"
```

---

## 🚀 Quick Start

### 1. Authentication

```bash
# Login to Epsimo
epsimo auth login

# Check who you're logged in as
epsimo whoami

# Check thread/credit balance
epsimo credits balance
```

### 2. Create Your First Project

```bash
# Create a new Next.js project with Epsimo
epsimo create "My AI App"

# Or initialize in existing directory
cd my-existing-project
epsimo init
```

### 3. Deploy Configuration

```bash
# Sync your epsimo.yaml to the platform
epsimo deploy
```

---

## 🛠️ CLI Reference

### Authentication Commands
```bash
epsimo auth login              # Interactive login
epsimo whoami                  # Display current user info
```

### Project Management
```bash
epsimo projects                # List all projects
epsimo create <name>           # Scaffold a new Next.js app
epsimo init                    # Initialize existing directory
epsimo deploy                  # Deploy epsimo.yaml configuration
```

### Virtual Database
```bash
epsimo db query --project-id <P_ID> --thread-id <T_ID>
epsimo db set --project-id <P_ID> --thread-id <T_ID> --key <K> --value <V>
epsimo db get --project-id <P_ID> --thread-id <T_ID> --key <K>
```

### Credits & Billing
```bash
epsimo credits balance                  # Check thread balance
epsimo credits buy --quantity <N>       # Generate Stripe checkout URL
```

### Resource Listing
```bash
epsimo assistants --project-id <P_ID>  # List assistants
epsimo threads --project-id <P_ID>     # List threads
```

---

## 📚 Python SDK

### Installation

```python
from epsimo import EpsimoClient

# Initialize with API key (JWT token)
client = EpsimoClient(api_key="your-token-here")

# Or use environment variable
# export EPSIMO_API_KEY=your-token-here
client = EpsimoClient()
```

### Virtual Database Access

```python
# Get all structured data from a thread
db_state = client.db.get_all(project_id, thread_id)

# Get specific key
user_prefs = client.db.get(project_id, thread_id, "user_preferences")
print(f"Theme: {user_prefs.get('theme')}")

# Set value (for seeding/testing)
client.db.set(project_id, thread_id, "status", "active")
```

### Streaming Conversations

```python
# Stream assistant responses
for chunk in client.threads.run_stream(
    project_id, 
    thread_id, 
    assistant_id, 
    "Hello, how can you help me?"
):
    print(chunk, end="", flush=True)
```

### Managing Resources

```python
# Projects
projects = client.projects.list()
project = client.projects.create(name="My Project", description="...")
project_details = client.projects.get(project_id)

# Assistants
assistants = client.assistants.list(project_id)
assistant = client.assistants.create(project_id, config={...})

# Threads
threads = client.threads.list(project_id)
thread = client.threads.create(project_id, assistant_id=assistant_id)

# Files
files = client.files.list(project_id)
file = client.files.upload(project_id, file_path="document.pdf")

# Credits
balance = client.credits.get_balance()
checkout_url = client.credits.create_checkout_session(quantity=1000, amount=100.0)
```

---

## 🎨 React UI Kit

### ThreadChat Component

```tsx
import { ThreadChat } from "@/components/epsimo";

export default function App() {
  return (
    <ThreadChat 
      assistantId="your-assistant-id"
      projectId="your-project-id"
      placeholder="Ask me anything..."
    />
  );
}
```

### useChat Hook (Headless)

```tsx
import { useChat } from "@/hooks/epsimo";

export default function CustomChat() {
  const { messages, sendMessage, isLoading } = useChat({
    projectId: "...",
    threadId: "...",
    assistantId: "..."
  });

  return (
    <div>
      {messages.map(msg => (
        <div key={msg.id}>{msg.content}</div>
      ))}
      <button onClick={() => sendMessage("Hello")} disabled={isLoading}>
        Send
      </button>
    </div>
  );
}
```

---

## 🧪 Tool Library

The framework includes reusable tool schemas in `epsimo/tools/library.yaml`:

### Available Tools

| Tool | Type | Description |
|------|------|-------------|
| **database_sync** | function | Persist structured JSON to thread state (Virtual DB) |
| **web_search_tavily** | search_tavily | Advanced web search with source attribution |
| **web_search_ddg** | ddg_search | Fast DuckDuckGo search for simple queries |
| **retrieval_optimized** | retrieval | High-accuracy document search in uploaded files |
| **task_management** | function | Track and update user tasks |

### Using Tools in Assistants

```yaml
# epsimo.yaml
assistants:
  - name: "Research Assistant"
    model: "gpt-4o"
    instructions: "You help with research tasks"
    tools:
      - type: search_tavily
        max_results: 5
      - type: function
        name: update_database
        description: "Save research findings"
        parameters:
          type: object
          properties:
            key: { type: string }
            value: { type: object }
```

---

## 💾 Virtual Database Pattern

Threads serve as persistent, structured storage — eliminating the need for a separate database.

### How It Works

1. **Agent writes to DB** using the `update_database` tool
2. **Data persists** in thread state
3. **Query from SDK or CLI**:

```python
# Python SDK
preferences = client.db.get(project_id, thread_id, "user_preferences")

# CLI
epsimo db query --project-id P123 --thread-id T456
```

### Benefits

- ✅ Zero database configuration
- ✅ Data naturally partitioned by conversation
- ✅ Agent always "knows" what's in its DB
- ✅ Queryable from both agent and application code

See [docs/virtual_db_guide.md](docs/virtual_db_guide.md) for detailed guide.

---

## 🔐 Authentication & Security

### Environment Variables

```bash
# .env file (never commit!)
EPSIMO_API_KEY=your-jwt-token-here
EPSIMO_EMAIL=your@email.com
EPSIMO_PASSWORD=your-password  # Only for automated scripts
```

### Token Management

```python
from epsimo.auth import get_token, perform_login

# Login programmatically
token = perform_login("your@email.com", "password")

# Get cached token (auto-refreshes if expired)
token = get_token()
```

**Token Storage:** Tokens are stored in `~/code/epsimo-frontend/.epsimo_token` (configurable via `TOKEN_FILE` in auth.py)

**Security Best Practices:**
- Never commit `.epsimo_token` or `.env` files
- Use environment variables in production
- Rotate tokens regularly
- Use project-specific tokens for multi-tenant apps

---

## 📖 API Reference

See [references/api_reference.md](references/api_reference.md) for comprehensive endpoint documentation including:
- Authentication flows
- Request/response schemas
- HTTP status codes
- Error handling patterns
- Rate limits

---

## 🧪 Verification & Testing

```bash
# Verify skill is correctly configured
python3 verify_skill.py

# Run E2E test suite
python3 scripts/test_all_skills.py

# Test streaming functionality
python3 scripts/test_streaming.py

# Test Virtual DB
python3 scripts/test_vdb.py
```

---

## 📁 Project Structure

```
epsimo-agent/
├── epsimo/
│   ├── cli.py              # Unified CLI
│   ├── client.py           # Main SDK client
│   ├── auth.py             # Authentication logic
│   ├── resources/          # Resource-specific clients
│   │   ├── projects.py
│   │   ├── assistants.py
│   │   ├── threads.py
│   │   ├── files.py
│   │   ├── credits.py
│   │   └── db.py
│   ├── tools/
│   │   └── library.yaml    # Reusable tool schemas
│   └── templates/          # Project scaffolding templates
├── scripts/                # Helper scripts and examples
├── docs/                   # Additional documentation
├── references/             # API reference docs
├── SKILL.md                # Main skill documentation
└── README.md               # This file
```

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or pull request on [GitHub](https://github.com/thierryteisseire/epsimo-agent).

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🔗 Links

### Installation & Discovery
- **skills.sh:** Search for "epsimo-agent" at https://skills.sh
- **npm Package:** https://www.npmjs.com/package/epsimo-agent
- **Install Command:** `npx skills add thierryteisseire/epsimo-agent`

### Documentation
- **Skill Guide:** [SKILL.md](SKILL.md)
- **API Reference:** [references/api_reference.md](references/api_reference.md)
- **Virtual DB Guide:** [docs/virtual_db_guide.md](docs/virtual_db_guide.md)

### Platform
- **GitHub Repository:** https://github.com/thierryteisseire/epsimo-agent
- **Epsimo Web App:** https://app.epsimoagents.com
- **API Endpoint:** https://api.epsimoagents.com

---

**Questions?** Open an issue on [GitHub](https://github.com/thierryteisseire/epsimo-agent/issues) or check the [API Reference](references/api_reference.md).
