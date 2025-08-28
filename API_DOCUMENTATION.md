# Elch Agent API Documentation

## Overview

This document provides comprehensive API documentation for the Elch Agent backend, including all endpoints, request/response formats, authentication requirements, and usage examples for frontend integration.

## Base URL
```
http://localhost:8000
```

## Authentication

Most endpoints require authentication. Use the following methods:

### JWT Token Authentication
- Include `Authorization: Bearer <token>` header
- Obtain token via `/token` endpoint

### Session Authentication
- Use session cookies for web-based authentication
- Login via `/token` or OAuth providers

---

## API Endpoints

## 🔐 Authentication & User Management

### POST /signup
Create a new user account.

**Request Body:**
```json
{
  "email": "string",
  "username": "string",
  "password": "string",
  "is_active": true,
  "is_superuser": false
}
```

**Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2023-01-01T00:00:00Z"
}
```

**Error Responses:**
- `400` - Invalid data
- `409` - User already exists

---

### POST /token
Authenticate user and get access token.

**Request Body:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "is_active": true,
    "is_superuser": false
  }
}
```

**Error Responses:**
- `401` - Invalid credentials
- `422` - Validation error

---

### GET /login/{provider}
Initiate OAuth login with specified provider.

**Path Parameters:**
- `provider`: `google` | `github` | `facebook`

**Response (302):**
Redirects to OAuth provider's authorization page.

---

### GET /auth/{provider}
OAuth callback endpoint.

**Path Parameters:**
- `provider`: `google` | `github` | `facebook`

**Query Parameters:**
- `code`: OAuth authorization code
- `state`: OAuth state parameter

**Response (302):**
Redirects to frontend with authentication result.

---

### GET /me
Get current user information.

**Authentication:** Required (JWT or Session)

**Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "is_active": true,
  "is_superuser": false,
  "created_at": "2023-01-01T00:00:00Z"
}
```

---

## ☁️ Cloud Credentials Management

### GET /credentials
Get all cloud credentials for current user.

**Authentication:** Required

**Response (200):**
```json
[
  {
    "id": 1,
    "provider": "aws",
    "access_key": "AKIA...",
    "region": "us-east-1",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
]
```

---

### POST /credentials
Create new cloud credentials.

**Authentication:** Required

**Request Body:**
```json
{
  "provider": "aws",
  "access_key": "AKIA...",
  "secret_key": "secret...",
  "region": "us-east-1"
}
```

**Response (201):**
```json
{
  "id": 1,
  "provider": "aws",
  "access_key": "AKIA...",
  "region": "us-east-1",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

---

## 🤖 AI Agent Core Functionality

### POST /agent/run
Execute an agent task with intelligent question classification.

**Authentication:** Required

**Request Body:**
```json
{
  "user_input": "What is the capital of France?",
  "run_id": "unique-run-id",
  "continue_from_step": 0
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Answered general question using AI knowledge.",
  "history": [
    {
      "step": 1,
      "action": {
        "name": "answer_general_question",
        "params": {
          "question": "What is the capital of France?"
        }
      },
      "result": "Paris is the capital and most populous city of France...",
      "thought": "Answered general question: What is the capital of France?"
    }
  ],
  "final_result": "Paris is the capital and most populous city of France..."
}
```

**Features:**
- **Intelligent Classification**: Automatically detects general questions vs tasks
- **Direct Answers**: General questions answered instantly using Gemini API
- **Tool Execution**: Task requests handled with browser automation
- **Context Awareness**: Uses agent memory for informed responses

---

### POST /prompt
Legacy prompt endpoint (use `/agent/run` for new implementations).

**Authentication:** Required

**Request Body:**
```json
{
  "prompt": "Explain quantum physics"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Answered general question using AI knowledge.",
  "steps": [
    {
      "step": {
        "action": "answer_general_question",
        "params": {
          "question": "Explain quantum physics"
        }
      },
      "result": "Quantum physics is the study of matter and energy...",
      "error": null
    }
  ],
  "evaluation_score": 1.0
}
```

---

### POST /assistant/prompt
Enhanced prompt endpoint with advanced features.

**Authentication:** Required

**Request Body:**
```json
{
  "prompt": "Book a flight to Tokyo"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Plan executed successfully",
  "steps": [
    {
      "step": {
        "action": "open_browser",
        "params": {
          "url": "https://booking.example.com"
        }
      },
      "result": "Browser opened successfully",
      "error": null
    }
  ],
  "evaluation_score": 0.95
}
```

---

## 🌐 Web Scraping & Browsing

### POST /scrape
Scrape web content.

**Authentication:** Required

**Request Body:**
```json
{
  "url": "https://example.com",
  "selectors": {
    "title": "h1",
    "content": ".main-content"
  },
  "wait_time": 5
}
```

**Response (200):**
```json
{
  "url": "https://example.com",
  "title": "Example Domain",
  "content": "This domain is for use in illustrative examples...",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

---

### POST /call_tool
Execute specific automation tools.

**Authentication:** Required

**Request Body:**
```json
{
  "tool_name": "open_browser",
  "params": {
    "url": "https://example.com",
    "max_retries": 3
  }
}
```

**Response (200):**
```json
{
  "result": "Browser opened with ID: browser_123"
}
```

**Available Tools:**
- `open_browser`: Open new browser instance
- `get_page_content`: Extract page content
- `fill_form`: Fill form fields
- `click_button`: Click buttons/links
- `close_browser`: Close browser instance
- `search_web`: Perform web search

---

## 📝 Form Automation

### POST /form/automate_registration
Automate user registration on websites.

**Authentication:** Required

**Request Body:**
```json
{
  "url": "https://example.com/register",
  "form_data": {
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepass123"
  },
  "browser_id": "browser_123"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Registration completed successfully",
  "result": {
    "success": true,
    "redirect_url": "https://example.com/dashboard"
  }
}
```

---

### POST /form/automate_login
Automate login process.

**Authentication:** Required

**Request Body:**
```json
{
  "browser_id": "browser_123",
  "url": "https://example.com/login",
  "username_selector": "#username",
  "username": "user@example.com",
  "password_selector": "#password",
  "password": "mypassword",
  "submit_selector": "button[type='submit']",
  "success_indicator": "Welcome"
}
```

**Response (200):**
```json
{
  "status": "success",
  "result": {
    "login_successful": true,
    "current_url": "https://example.com/dashboard"
  }
}
```

---

### POST /form/apply_job_upwork
Apply for jobs on Upwork.

**Authentication:** Required

**Request Body:**
```json
{
  "job_url": "https://www.upwork.com/job/job-details",
  "proposal_text": "I am excited to work on this project...",
  "rate": 50,
  "browser_id": "browser_123"
}
```

**Response (200):**
```json
{
  "status": "success",
  "message": "Job application submitted successfully",
  "result": {
    "application_id": "app_123",
    "status": "submitted"
  }
}
```

---

### POST /form/apply_job_fiverr
Apply for jobs on Fiverr.

**Authentication:** Required

**Request Body:**
```json
{
  "job_url": "https://www.fiverr.com/gigs/job",
  "proposal_text": "I can deliver high-quality work...",
  "price": 100,
  "browser_id": "browser_123"
}
```

---

### POST /form/apply_job_linkedin
Apply for jobs on LinkedIn.

**Authentication:** Required

**Request Body:**
```json
{
  "job_url": "https://www.linkedin.com/jobs/view/job-id",
  "cover_letter": "I am interested in this position...",
  "browser_id": "browser_123"
}
```

---

### POST /form/batch_apply_jobs
Apply to multiple jobs at once.

**Authentication:** Required

**Request Body:**
```json
{
  "jobs": [
    {
      "platform": "upwork",
      "url": "https://www.upwork.com/job/job1",
      "proposal": "Proposal text..."
    },
    {
      "platform": "fiverr",
      "url": "https://www.fiverr.com/gigs/job1",
      "proposal": "Proposal text..."
    }
  ],
  "browser_id": "browser_123"
}
```

---

## 📊 Task Management

### GET /api/tasks/results
Get task execution results.

**Authentication:** Required

**Query Parameters:**
- `limit`: Number of results (default: 50)
- `offset`: Pagination offset (default: 0)
- `status`: Filter by status (optional)

**Response (200):**
```json
{
  "results": [
    {
      "id": 1,
      "goal": "Book a flight to Paris",
      "description": "Book a flight to Paris",
      "status": "completed",
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z",
      "result": "Flight booked successfully",
      "steps_completed": 5,
      "total_steps": 5,
      "user_id": 1
    }
  ],
  "total": 100,
  "limit": 50,
  "offset": 0
}
```

---

### GET /api/tasks/statistics
Get task execution statistics.

**Authentication:** Required

**Query Parameters:**
- `days`: Number of days to look back (default: 30)

**Response (200):**
```json
{
  "total": 150,
  "completed": 120,
  "failed": 15,
  "running": 10,
  "paused": 5,
  "success_rate": 0.8,
  "average_duration_seconds": 450.5,
  "period_days": 30,
  "start_date": "2023-12-01T00:00:00Z",
  "end_date": "2023-12-31T00:00:00Z"
}
```

---

### GET /api/tasks/{task_id}/download
Download task result in specified format.

**Authentication:** Required

**Path Parameters:**
- `task_id`: Task ID

**Query Parameters:**
- `format`: `json` or `txt` (default: `json`)

**Response (200):**
File download with task details.

---

### DELETE /api/tasks/{task_id}
Delete a task result.

**Authentication:** Required

**Path Parameters:**
- `task_id`: Task ID

**Response (200):**
```json
{
  "message": "Task result deleted successfully"
}
```

---

## 💬 Chat System

### GET /chat/history
Get chat history.

**Authentication:** Required

**Response (200):**
```json
[
  {
    "id": 1,
    "sender": "user",
    "message": "Hello, can you help me?",
    "message_type": "text",
    "timestamp": "2023-01-01T00:00:00Z",
    "agent_run_id": "run_123"
  },
  {
    "id": 2,
    "sender": "agent",
    "message": "Hello! I'd be happy to help you.",
    "message_type": "text",
    "timestamp": "2023-01-01T00:00:05Z",
    "agent_run_id": "run_123"
  }
]
```

---

### POST /chat/message
Send a chat message.

**Authentication:** Required

**Request Body:**
```json
{
  "message": "What is the weather today?",
  "message_type": "text",
  "agent_run_id": "run_123"
}
```

**Response (200):**
```json
{
  "status": "success",
  "response": "I'll help you check the weather..."
}
```

---

### GET /
Home page endpoint.

**Response (200):**
```html
<!DOCTYPE html>
<html>
<head><title>Elch Agent</title></head>
<body><h1>Welcome to Elch Agent</h1></body>
</html>
```

---

## 🏥 Health & Monitoring

### GET /healthz
Health check endpoint.

**Response (200):**
```json
{
  "status": "healthy",
  "timestamp": "2023-01-01T00:00:00Z",
  "version": "1.0.0"
}
```

---

### GET /memory/stats
Get memory usage statistics.

**Authentication:** Required

**Response (200):**
```json
{
  "total_memory_mb": 512,
  "used_memory_mb": 256,
  "available_memory_mb": 256,
  "memory_usage_percent": 50.0,
  "cache_stats": {
    "total_entries": 1000,
    "cache_hits": 850,
    "cache_misses": 150,
    "hit_rate": 0.85
  }
}
```

---

## 🔧 Plan Execution & Feedback

### POST /execute_plan
Execute a predefined plan.

**Authentication:** Required

**Request Body:**
```json
{
  "plan": [
    {
      "action": "open_browser",
      "params": {
        "url": "https://example.com"
      }
    },
    {
      "action": "fill_form",
      "params": {
        "browser_id": "browser_123",
        "selector": "#search",
        "value": "search term"
      }
    }
  ]
}
```

---

### POST /feedback
Provide feedback on plan execution.

**Authentication:** Required

**Request Body:**
```json
{
  "plan_id": 123,
  "rating": 5,
  "comment": "Excellent execution!",
  "improvements": ["Could be faster"]
}
```

---

## Error Response Format

All endpoints return errors in the following format:

```json
{
  "detail": "Error message description",
  "error_code": "ERROR_CODE",
  "timestamp": "2023-01-01T00:00:00Z"
}
```

## Rate Limiting

- **General Questions**: 50 requests per minute per user
- **Task Execution**: 20 requests per minute per user
- **API Calls**: 100 requests per minute per user

## WebSocket Support

Real-time communication is available via WebSocket:

**Endpoint:** `ws://localhost:8000/ws?token=<jwt_token>`

**Messages:**
```json
{
  "topic": "agent_updates",
  "payload": {
    "log": "Agent is thinking...",
    "step": 1,
    "action": "open_browser"
  }
}
```

## Frontend Integration Examples

### JavaScript/TypeScript

```javascript
// Authentication
async function login(username, password) {
  const response = await fetch('/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `username=${username}&password=${password}`
  });
  const data = await response.json();
  localStorage.setItem('token', data.access_token);
  return data;
}

// Agent Interaction
async function askAgent(question) {
  const token = localStorage.getItem('token');
  const response = await fetch('/agent/run', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_input: question,
      run_id: `run_${Date.now()}`
    })
  });
  return await response.json();
}

// Real-time Updates
function connectWebSocket(token) {
  const ws = new WebSocket(`ws://localhost:8000/ws?token=${token}`);

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.topic === 'agent_updates') {
      console.log('Agent update:', data.payload);
    }
  };

  return ws;
}
```

### React Hook Example

```javascript
import { useState, useEffect } from 'react';

function useAgent() {
  const [isLoading, setIsLoading] = useState(false);
  const [response, setResponse] = useState(null);

  const askQuestion = async (question) => {
    setIsLoading(true);
    try {
      const result = await fetch('/agent/run', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user_input: question,
          run_id: `run_${Date.now()}`
        })
      });
      const data = await result.json();
      setResponse(data);
    } catch (error) {
      console.error('Agent error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return { askQuestion, response, isLoading };
}
```

## Best Practices

### 1. Authentication
- Always include authentication headers for protected endpoints
- Handle token expiration gracefully
- Implement token refresh logic

### 2. Error Handling
- Check response status codes
- Handle network errors
- Provide user-friendly error messages

### 3. Real-time Updates
- Use WebSocket for live agent updates
- Handle connection drops gracefully
- Implement reconnection logic

### 4. Performance
- Cache frequently accessed data
- Implement pagination for large datasets
- Use appropriate loading states

### 5. Security
- Never expose sensitive data in frontend
- Validate all user inputs
- Use HTTPS in production

## Support

For additional help or questions about the API:
- Check the agent logs at `/var/log/elch-agent.log`
- Review the health endpoint for system status
- Contact the development team for specific integration questions

---

**Last Updated:** January 2024
**API Version:** 1.0.0
**Base URL:** `http://localhost:8000`
