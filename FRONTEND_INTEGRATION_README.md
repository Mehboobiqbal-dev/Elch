# Frontend Integration Guide - Elch Agent API

## Overview

This guide provides comprehensive resources for integrating the Elch Agent API into your frontend applications. The Elch Agent now supports both **general question answering** and **task automation** with intelligent classification.

## 🚀 Quick Start

### 1. Start the Backend
```bash
cd /path/to/elch-agent
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Basic Integration
```javascript
// Simple API call
const response = await fetch('http://localhost:8000/agent/run', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    user_input: "What is the capital of France?",
    run_id: `run_${Date.now()}`
  })
});
```

## 📁 Integration Resources

### 1. **API Documentation** (`API_DOCUMENTATION.md`)
- Complete endpoint reference
- Request/response formats
- Authentication details
- Error handling guide

### 2. **TypeScript Types** (`api-types.ts`)
- Complete type definitions
- API client class
- React hooks
- Error types

### 3. **JavaScript Examples** (`frontend-integration-examples.js`)
- Authentication service
- Agent service
- Task management
- Chat service
- React hooks
- Complete app example

### 4. **Postman Collection** (`Elch-Agent-API.postman_collection.json`)
- Import into Postman for testing
- Pre-configured requests
- Environment variables
- Automated token management

## 🔑 Key Features for Frontend

### Intelligent Question Classification
```javascript
// The agent automatically detects question type:
"General": "What is quantum physics?"
"Task": "Book a flight to Paris"

// No need to manually specify - the API handles it!
```

### Real-time Updates
```javascript
// WebSocket for live agent updates
const ws = new WebSocket('ws://localhost:8000/ws?token=' + token);
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.topic === 'agent_updates') {
    console.log('Agent thinking:', data.payload.log);
  }
};
```

### Rate Limiting
- **General Questions**: 50 requests/minute
- **Task Execution**: 20 requests/minute
- Built-in error handling for rate limits

## 🛠️ Integration Methods

### Method 1: Direct API Calls
```javascript
// Simple fetch-based integration
class ElchAPI {
  constructor(token) {
    this.token = token;
    this.baseURL = 'http://localhost:8000';
  }

  async askAgent(question) {
    const response = await fetch(`${this.baseURL}/agent/run`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_input: question,
        run_id: `run_${Date.now()}`
      })
    });
    return response.json();
  }
}
```

### Method 2: TypeScript Client
```typescript
import { ElchApiClient, AgentRunResponse } from './api-types';

const client = new ElchApiClient('http://localhost:8000');
await client.login('username', 'password');

const response: AgentRunResponse = await client.runAgent({
  user_input: "What is AI?",
  run_id: "run_123"
});
```

### Method 3: React Hooks
```javascript
import { useAgent, useAuth } from './frontend-integration-examples';

function MyComponent() {
  const { user } = useAuth();
  const { askAgent, response, loading } = useAgent();

  const handleAsk = async () => {
    await askAgent("Explain machine learning");
  };

  return (
    <div>
      <button onClick={handleAsk} disabled={loading}>
        {loading ? 'Thinking...' : 'Ask Agent'}
      </button>
      {response && <div>{response.final_result}</div>}
    </div>
  );
}
```

## 📊 Response Handling

### General Questions
```javascript
{
  "status": "success",
  "message": "Answered general question using AI knowledge.",
  "history": [...],
  "final_result": "Paris is the capital and most populous city of France."
}
```

### Task Execution
```javascript
{
  "status": "success",
  "message": "Plan executed successfully",
  "history": [...],
  "final_result": "Flight booked successfully"
}
```

### Error Handling
```javascript
{
  "detail": "Authentication required",
  "error_code": "AUTH_REQUIRED",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

## 🔐 Authentication Flow

### 1. Login
```javascript
const loginResponse = await fetch('/token', {
  method: 'POST',
  body: new FormData([
    ['username', 'user'],
    ['password', 'pass']
  ])
});
const { access_token } = await loginResponse.json();
localStorage.setItem('token', access_token);
```

### 2. Use Token
```javascript
const response = await fetch('/agent/run', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
  // ... rest of request
});
```

### 3. Handle Expiration
```javascript
if (response.status === 401) {
  // Token expired, redirect to login
  localStorage.removeItem('token');
  window.location.href = '/login';
}
```

## 🎨 UI/UX Considerations

### Loading States
```javascript
const [loading, setLoading] = useState(false);

const askQuestion = async (question) => {
  setLoading(true);
  try {
    const result = await api.askAgent(question);
    // Handle result
  } finally {
    setLoading(false);
  }
};
```

### Progress Updates
```javascript
// Show agent thinking progress
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.topic === 'agent_updates') {
    setProgress(data.payload.log);
  }
};
```

### Error Display
```javascript
const [error, setError] = useState(null);

try {
  await api.askAgent(question);
} catch (err) {
  setError(err.message);
}

// Display error in UI
{error && <div className="error">{error}</div>}
```

## 📱 Example Frontend App

### React Component
```javascript
import React, { useState } from 'react';
import { useAgent, useAuth } from './services/elch-api';

function ChatInterface() {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const { askAgent, loading } = useAgent();
  const { user } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    const userMessage = { role: 'user', content: message };
    setChatHistory(prev => [...prev, userMessage]);
    setMessage('');

    try {
      const response = await askAgent(message);
      const agentMessage = {
        role: 'agent',
        content: response.final_result || response.message
      };
      setChatHistory(prev => [...prev, agentMessage]);
    } catch (error) {
      const errorMessage = {
        role: 'agent',
        content: `Error: ${error.message}`,
        isError: true
      };
      setChatHistory(prev => [...prev, errorMessage]);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-history">
        {chatHistory.map((msg, index) => (
          <div key={index} className={`message ${msg.role} ${msg.isError ? 'error' : ''}`}>
            <strong>{msg.role === 'user' ? user?.username : 'Elch'}:</strong> {msg.content}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="chat-input">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask me anything... (questions or tasks)"
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Thinking...' : 'Send'}
        </button>
      </form>
    </div>
  );
}

export default ChatInterface;
```

### Vue.js Composition API
```javascript
import { ref, reactive } from 'vue';
import { useAgent, useAuth } from './composables/elch-api';

export default {
  setup() {
    const message = ref('');
    const chatHistory = ref([]);
    const { askAgent, loading } = useAgent();
    const { user } = useAuth();

    const handleSubmit = async () => {
      if (!message.value.trim()) return;

      chatHistory.value.push({
        role: 'user',
        content: message.value
      });

      const currentMessage = message.value;
      message.value = '';

      try {
        const response = await askAgent(currentMessage);
        chatHistory.value.push({
          role: 'agent',
          content: response.final_result || response.message
        });
      } catch (error) {
        chatHistory.value.push({
          role: 'agent',
          content: `Error: ${error.message}`,
          isError: true
        });
      }
    };

    return {
      message,
      chatHistory,
      loading,
      user,
      handleSubmit
    };
  }
};
```

## 🔧 Environment Setup

### Development
```bash
# .env file
VITE_ELCH_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

### Production
```bash
# .env file
VITE_ELCH_API_URL=https://your-api-domain.com
VITE_WS_URL=wss://your-api-domain.com
```

## 🧪 Testing Your Integration

### 1. Import Postman Collection
- Open Postman
- Import `Elch-Agent-API.postman_collection.json`
- Set `base_url` variable to your API URL
- Test authentication and endpoints

### 2. Run Integration Tests
```javascript
// Test basic functionality
const api = new ElchApiClient();
await api.login('testuser', 'testpass');
const response = await api.runAgent({
  user_input: 'What is 2+2?',
  run_id: 'test_run'
});
console.log('Test passed:', response.status === 'success');
```

### 3. Test WebSocket
```javascript
const ws = new WebSocket('ws://localhost:8000/ws?token=' + token);
ws.onopen = () => console.log('WebSocket connected');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

## 🚀 Deployment Checklist

- [ ] API endpoint URLs configured
- [ ] Authentication flow implemented
- [ ] Error handling in place
- [ ] Loading states handled
- [ ] WebSocket integration (optional)
- [ ] Rate limiting handled
- [ ] Mobile responsiveness
- [ ] Accessibility considerations
- [ ] Security headers configured

## 📞 Support

### Common Issues

1. **CORS Errors**
   - Ensure backend allows your frontend domain
   - Check CORS configuration in main.py

2. **WebSocket Connection Issues**
   - Verify WebSocket URL and token
   - Check browser console for connection errors

3. **Authentication Problems**
   - Verify token storage and retrieval
   - Check token expiration handling

4. **Rate Limiting**
   - Implement exponential backoff
   - Show user-friendly rate limit messages

### Getting Help

1. **Check the Logs**: Backend logs are in `/var/log/elch-agent.log`
2. **Health Check**: Visit `/healthz` to verify API status
3. **Documentation**: Refer to `API_DOCUMENTATION.md` for detailed specs

---

**Happy coding! 🎉**

The Elch Agent API is designed to be developer-friendly and powerful. Use these resources to build amazing AI-powered applications.
