---
name: epsimo-agent
description: Interact with the EpsimoAI platform to manage agents, projects, and threads, and design frontends.
---

# Epsimo Agent Framework (Beta)

> [!NOTE]
> This is a **Beta** version of the Epsimo Agent Framework. Features and APIs may be subject to change.

The Epsimo Agent Framework allows you to build sophisticated AI-powered applications with agents, persistent threads, and a "Virtual Database" state layer. It provides a unified **CLI**, a **Python SDK**, and a **React UI Kit**.

**Base URL:** `https://api.epsimoagents.com`
**Frontend URL:** `https://app.epsimoagents.com`

## 🚀 Quick Start: Create an MVP

The fastest way to build an Epsimo app is using the project generator:

```bash
# 1. Authenticate
epsimo auth login

# 2. Create a new Next.js project
epsimo create "My AI App"

# 3. Initialize and Deploy
cd my-ai-app
epsimo init
epsimo deploy
```

## 🛠️ Unified CLI (`epsimo`)

The `epsimo` CLI is the main tool for managing your agents and data.

### Authentication
```bash
epsimo auth login
epsimo whoami
```

### Project Scaffolding
- `epsimo create <name>`: Scaffolds a full Next.js application with Epsimo integrated.
- `epsimo init`: Links a local directory to an Epsimo project.
- `epsimo deploy`: Syncs your `epsimo.yaml` configuration to the platform.

### Virtual Database
Threads can serve as a persistent structured storage layer.
- `epsimo db query --project-id <P_ID> --thread-id <T_ID>`: View structured thread state.
- `epsimo db set --project-id <P_ID> --thread-id <T_ID> --key <K> --value <V>`: Seed state.

### Credits
- `epsimo credits balance`: Check current token balance.
- `epsimo credits buy --quantity <N>`: Generate a Stripe checkout URL.

## 📦 Python SDK (`epsimo`)

The framework includes a powerful Python SDK for automation or backend services.

```python
from epsimo import EpsimoClient

c = EpsimoClient(api_key="your-token")

# Virtual DB Access
user_pref = c.db.get(project_id, thread_id, "user_preferences")

# Conversation Streaming
for chunk in c.threads.run_stream(project_id, thread_id, assistant_id, "Hello!"):
    print(chunk)
```

## 🎨 React UI Kit

The UI Kit provides high-level components for immediate integration.

- **`ThreadChat`**: A modern, dark-themed chat interface with streaming and tool support.
- **`useChat`**: A headless hook for managing conversation state.

**Importing:**
```tsx
import { ThreadChat } from "@/components/epsimo";

export default function App() {
  return <ThreadChat assistantId="your-assistant-id" />;
}
```

## 📚 Tool Library

Found in `epsimo/tools/library.yaml`, this collection provides reusable JSON schemas for:
- **`database_sync`**: Allow agents to write to the Virtual DB.
- **`web_search_tavily`**: Advanced search with sources.
- **`retrieval_optimized`**: High-accuracy document search.

## 🧪 Verification
Ensure your environment is correctly configured:
```bash
python3 -m epsimo.verify_skill
```

