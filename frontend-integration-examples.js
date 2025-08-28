/**
 * Elch Agent Frontend Integration Examples
 * Complete JavaScript/React examples for integrating with the Elch Agent API
 */

// ========================================
// BASIC SETUP AND CONFIGURATION
// ========================================

// API Configuration
const API_CONFIG = {
  baseURL: 'http://localhost:8000',
  endpoints: {
    auth: {
      login: '/token',
      signup: '/signup',
      me: '/me'
    },
    agent: {
      run: '/agent/run',
      prompt: '/prompt'
    },
    tasks: {
      results: '/api/tasks/results',
      statistics: '/api/tasks/statistics'
    },
    chat: {
      history: '/chat/history',
      message: '/chat/message'
    }
  }
};

// ========================================
// AUTHENTICATION SERVICE
// ========================================

class AuthService {
  constructor() {
    this.token = localStorage.getItem('auth_token');
  }

  async login(username, password) {
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await fetch(`${API_CONFIG.baseURL}/token`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('Login failed');
      }

      const data = await response.json();
      this.token = data.access_token;
      localStorage.setItem('auth_token', this.token);
      localStorage.setItem('user', JSON.stringify(data.user));

      return data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  async signup(userData) {
    try {
      const response = await fetch(`${API_CONFIG.baseURL}/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(userData)
      });

      if (!response.ok) {
        throw new Error('Signup failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Signup error:', error);
      throw error;
    }
  }

  async getCurrentUser() {
    if (!this.token) return null;

    try {
      const response = await fetch(`${API_CONFIG.baseURL}/me`, {
        headers: {
          'Authorization': `Bearer ${this.token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to get user');
      }

      return await response.json();
    } catch (error) {
      console.error('Get user error:', error);
      this.logout();
      throw error;
    }
  }

  logout() {
    this.token = null;
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
  }

  getAuthHeaders() {
    return this.token ? { 'Authorization': `Bearer ${this.token}` } : {};
  }
}

// ========================================
// AGENT SERVICE
// ========================================

class AgentService {
  constructor(authService) {
    this.auth = authService;
  }

  async runAgent(userInput, runId = null) {
    if (!runId) {
      runId = `run_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    try {
      const response = await fetch(`${API_CONFIG.baseURL}/agent/run`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...this.auth.getAuthHeaders()
        },
        body: JSON.stringify({
          user_input: userInput,
          run_id: runId
        })
      });

      if (!response.ok) {
        throw new Error('Agent request failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Agent run error:', error);
      throw error;
    }
  }

  async sendPrompt(prompt) {
    try {
      const response = await fetch(`${API_CONFIG.baseURL}/prompt`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...this.auth.getAuthHeaders()
        },
        body: JSON.stringify({
          prompt: prompt
        })
      });

      if (!response.ok) {
        throw new Error('Prompt request failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Prompt error:', error);
      throw error;
    }
  }
}

// ========================================
// TASK MANAGEMENT SERVICE
// ========================================

class TaskService {
  constructor(authService) {
    this.auth = authService;
  }

  async getTaskResults(limit = 50, offset = 0, status = null) {
    try {
      const params = new URLSearchParams({
        limit: limit.toString(),
        offset: offset.toString()
      });

      if (status) {
        params.append('status', status);
      }

      const response = await fetch(
        `${API_CONFIG.baseURL}/api/tasks/results?${params}`,
        {
          headers: this.auth.getAuthHeaders()
        }
      );

      if (!response.ok) {
        throw new Error('Failed to get task results');
      }

      return await response.json();
    } catch (error) {
      console.error('Get task results error:', error);
      throw error;
    }
  }

  async getTaskStatistics(days = 30) {
    try {
      const response = await fetch(
        `${API_CONFIG.baseURL}/api/tasks/statistics?days=${days}`,
        {
          headers: this.auth.getAuthHeaders()
        }
      );

      if (!response.ok) {
        throw new Error('Failed to get task statistics');
      }

      return await response.json();
    } catch (error) {
      console.error('Get task statistics error:', error);
      throw error;
    }
  }

  async downloadTaskResult(taskId, format = 'json') {
    try {
      const response = await fetch(
        `${API_CONFIG.baseURL}/api/tasks/${taskId}/download?format=${format}`,
        {
          headers: this.auth.getAuthHeaders()
        }
      );

      if (!response.ok) {
        throw new Error('Failed to download task result');
      }

      // Handle file download
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `task-${taskId}-result.${format}`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Download task result error:', error);
      throw error;
    }
  }
}

// ========================================
// CHAT SERVICE
// ========================================

class ChatService {
  constructor(authService) {
    this.auth = authService;
    this.websocket = null;
  }

  async getChatHistory() {
    try {
      const response = await fetch(`${API_CONFIG.baseURL}/chat/history`, {
        headers: this.auth.getAuthHeaders()
      });

      if (!response.ok) {
        throw new Error('Failed to get chat history');
      }

      return await response.json();
    } catch (error) {
      console.error('Get chat history error:', error);
      throw error;
    }
  }

  async sendMessage(message, messageType = 'text', agentRunId = null) {
    try {
      const response = await fetch(`${API_CONFIG.baseURL}/chat/message`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...this.auth.getAuthHeaders()
        },
        body: JSON.stringify({
          message: message,
          message_type: messageType,
          agent_run_id: agentRunId
        })
      });

      if (!response.ok) {
        throw new Error('Failed to send message');
      }

      return await response.json();
    } catch (error) {
      console.error('Send message error:', error);
      throw error;
    }
  }

  connectWebSocket(onMessage) {
    if (this.websocket) {
      this.websocket.close();
    }

    const token = this.auth.token;
    if (!token) {
      throw new Error('No authentication token available');
    }

    this.websocket = new WebSocket(`${API_CONFIG.baseURL.replace('http', 'ws')}/ws?token=${token}`);

    this.websocket.onopen = () => {
      console.log('WebSocket connected');
    };

    this.websocket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage(data);
      } catch (error) {
        console.error('WebSocket message parse error:', error);
      }
    };

    this.websocket.onclose = () => {
      console.log('WebSocket disconnected');
    };

    this.websocket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    return this.websocket;
  }

  disconnectWebSocket() {
    if (this.websocket) {
      this.websocket.close();
      this.websocket = null;
    }
  }
}

// ========================================
// REACT HOOKS FOR EASY INTEGRATION
// ========================================

// React Hook for Authentication
function useAuth() {
  const [user, setUser] = React.useState(null);
  const [loading, setLoading] = React.useState(true);
  const [authService] = React.useState(() => new AuthService());

  React.useEffect(() => {
    const checkAuth = async () => {
      try {
        const currentUser = await authService.getCurrentUser();
        setUser(currentUser);
      } catch (error) {
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (username, password) => {
    setLoading(true);
    try {
      const result = await authService.login(username, password);
      setUser(result.user);
      return result;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  return {
    user,
    loading,
    login,
    logout,
    authService
  };
}

// React Hook for Agent Interaction
function useAgent(authService) {
  const [loading, setLoading] = React.useState(false);
  const [response, setResponse] = React.useState(null);
  const [agentService] = React.useState(() => new AgentService(authService));

  const askAgent = async (question) => {
    setLoading(true);
    setResponse(null);

    try {
      const result = await agentService.runAgent(question);
      setResponse(result);
      return result;
    } catch (error) {
      console.error('Agent error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const sendPrompt = async (prompt) => {
    setLoading(true);
    setResponse(null);

    try {
      const result = await agentService.sendPrompt(prompt);
      setResponse(result);
      return result;
    } catch (error) {
      console.error('Prompt error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  return {
    askAgent,
    sendPrompt,
    response,
    loading
  };
}

// React Hook for Task Management
function useTasks(authService) {
  const [tasks, setTasks] = React.useState([]);
  const [statistics, setStatistics] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [taskService] = React.useState(() => new TaskService(authService));

  const loadTasks = async (limit = 50, offset = 0, status = null) => {
    setLoading(true);
    try {
      const result = await taskService.getTaskResults(limit, offset, status);
      setTasks(result.results);
      return result;
    } catch (error) {
      console.error('Load tasks error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const loadStatistics = async (days = 30) => {
    try {
      const result = await taskService.getTaskStatistics(days);
      setStatistics(result);
      return result;
    } catch (error) {
      console.error('Load statistics error:', error);
      throw error;
    }
  };

  const downloadTask = async (taskId, format = 'json') => {
    try {
      await taskService.downloadTaskResult(taskId, format);
    } catch (error) {
      console.error('Download task error:', error);
      throw error;
    }
  };

  return {
    tasks,
    statistics,
    loading,
    loadTasks,
    loadStatistics,
    downloadTask
  };
}

// React Hook for Chat
function useChat(authService) {
  const [messages, setMessages] = React.useState([]);
  const [loading, setLoading] = React.useState(false);
  const [chatService] = React.useState(() => new ChatService(authService));
  const [wsConnection, setWsConnection] = React.useState(null);

  const loadHistory = async () => {
    try {
      const history = await chatService.getChatHistory();
      setMessages(history);
      return history;
    } catch (error) {
      console.error('Load chat history error:', error);
      throw error;
    }
  };

  const sendMessage = async (message, messageType = 'text', agentRunId = null) => {
    setLoading(true);
    try {
      const result = await chatService.sendMessage(message, messageType, agentRunId);

      // Add user message to local state
      const userMessage = {
        id: Date.now(),
        sender: 'user',
        message: message,
        message_type: messageType,
        timestamp: new Date().toISOString(),
        agent_run_id: agentRunId
      };
      setMessages(prev => [...prev, userMessage]);

      return result;
    } catch (error) {
      console.error('Send message error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const connectWebSocket = (onMessage) => {
    const ws = chatService.connectWebSocket(onMessage);
    setWsConnection(ws);
    return ws;
  };

  const disconnectWebSocket = () => {
    chatService.disconnectWebSocket();
    setWsConnection(null);
  };

  React.useEffect(() => {
    return () => {
      if (wsConnection) {
        disconnectWebSocket();
      }
    };
  }, [wsConnection]);

  return {
    messages,
    loading,
    loadHistory,
    sendMessage,
    connectWebSocket,
    disconnectWebSocket
  };
}

// ========================================
// USAGE EXAMPLES
// ========================================

// Complete React Component Example
function ElchAgentApp() {
  const { user, loading: authLoading, login, logout } = useAuth();
  const { askAgent, response: agentResponse, loading: agentLoading } = useAgent();
  const { tasks, loadTasks, loading: tasksLoading } = useTasks();
  const { messages, sendMessage, connectWebSocket } = useChat();

  const [input, setInput] = React.useState('');

  React.useEffect(() => {
    if (user) {
      // Load initial data
      loadTasks();
    }
  }, [user]);

  React.useEffect(() => {
    if (user) {
      // Connect to WebSocket for real-time updates
      connectWebSocket((data) => {
        if (data.topic === 'agent_updates') {
          console.log('Agent update:', data.payload);
        }
      });
    }
  }, [user]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    try {
      await askAgent(input);
      setInput('');
    } catch (error) {
      console.error('Failed to ask agent:', error);
    }
  };

  if (authLoading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return (
      <div className="login-form">
        <h2>Login to Elch Agent</h2>
        <form onSubmit={async (e) => {
          e.preventDefault();
          const formData = new FormData(e.target);
          try {
            await login(formData.get('username'), formData.get('password'));
          } catch (error) {
            alert('Login failed');
          }
        }}>
          <input name="username" placeholder="Username" required />
          <input name="password" type="password" placeholder="Password" required />
          <button type="submit">Login</button>
        </form>
      </div>
    );
  }

  return (
    <div className="elch-app">
      <header>
        <h1>Welcome to Elch Agent, {user.username}!</h1>
        <button onClick={logout}>Logout</button>
      </header>

      <div className="main-content">
        <div className="agent-chat">
          <h2>Ask the Agent</h2>
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask me anything... (general questions or tasks)"
              disabled={agentLoading}
            />
            <button type="submit" disabled={agentLoading}>
              {agentLoading ? 'Thinking...' : 'Ask'}
            </button>
          </form>

          {agentResponse && (
            <div className="response">
              <h3>Agent Response:</h3>
              <div className="response-content">
                <p><strong>Status:</strong> {agentResponse.status}</p>
                <p><strong>Message:</strong> {agentResponse.message}</p>
                {agentResponse.final_result && (
                  <p><strong>Result:</strong> {agentResponse.final_result}</p>
                )}
              </div>
            </div>
          )}
        </div>

        <div className="tasks-section">
          <h2>Recent Tasks</h2>
          {tasksLoading ? (
            <p>Loading tasks...</p>
          ) : (
            <div className="tasks-list">
              {tasks.slice(0, 5).map(task => (
                <div key={task.id} className="task-item">
                  <h4>{task.goal}</h4>
                  <p>Status: {task.status}</p>
                  <p>Steps: {task.steps_completed}/{task.total_steps}</p>
                  <small>{new Date(task.created_at).toLocaleString()}</small>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Export all services and hooks
export {
  AuthService,
  AgentService,
  TaskService,
  ChatService,
  useAuth,
  useAgent,
  useTasks,
  useChat,
  ElchAgentApp
};
