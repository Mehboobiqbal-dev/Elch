// Elch Agent API TypeScript Definitions
// Use these types in your frontend application for type safety

// ========================================
// BASE TYPES
// ========================================

export interface BaseResponse {
  status: 'success' | 'error';
  message: string;
  timestamp?: string;
}

export interface ErrorResponse extends BaseResponse {
  status: 'error';
  detail: string;
  error_code?: string;
}

export interface PaginatedResponse<T> extends BaseResponse {
  results: T[];
  total: number;
  limit: number;
  offset: number;
}

// ========================================
// AUTHENTICATION TYPES
// ========================================

export interface User {
  id: number;
  email: string;
  username: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface SignupRequest {
  email: string;
  username: string;
  password: string;
  is_active?: boolean;
  is_superuser?: boolean;
}

export interface LoginResponse extends BaseResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface GoogleLoginRequest {
  token: string;
}

// ========================================
// CLOUD CREDENTIALS TYPES
// ========================================

export interface CloudCredential {
  id: number;
  provider: 'aws' | 'azure' | 'gcp';
  access_key?: string;
  region?: string;
  created_at: string;
  updated_at: string;
}

export interface CloudCredentialCreate {
  provider: 'aws' | 'azure' | 'gcp';
  access_key: string;
  secret_key: string;
  region: string;
}

export interface CloudCredentialsResponse extends PaginatedResponse<CloudCredential> {}

// ========================================
// AGENT AND PROMPT TYPES
// ========================================

export interface AgentStateRequest {
  user_input: string;
  run_id?: string;
  continue_from_step?: number;
}

export interface AgentStep {
  step: number;
  action: {
    name: string;
    params: Record<string, any>;
  };
  result: any;
  thought: string;
}

export interface AgentRunResponse extends BaseResponse {
  status: 'success' | 'error' | 'running';
  history: AgentStep[];
  final_result?: any;
  current_step?: number;
  total_steps?: number;
}

export interface PromptRequest {
  prompt: string;
}

export interface PromptStep {
  step: {
    action: string;
    params: Record<string, any>;
  };
  result: any;
  error: string | null;
}

export interface PromptResponse extends BaseResponse {
  steps: PromptStep[];
  evaluation_score: number;
}

// ========================================
// TASK MANAGEMENT TYPES
// ========================================

export interface TaskResult {
  id: number;
  goal: string;
  description: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'paused';
  created_at: string;
  updated_at: string;
  result?: any;
  steps_completed: number;
  total_steps: number;
  user_id: number;
}

export interface TaskStatistics {
  total: number;
  completed: number;
  failed: number;
  running: number;
  paused: number;
  success_rate: number;
  average_duration_seconds: number;
  period_days: number;
  start_date: string;
  end_date: string;
}

export interface TaskResultsResponse extends PaginatedResponse<TaskResult> {}

// ========================================
// CHAT TYPES
// ========================================

export interface ChatMessage {
  id: number;
  sender: 'user' | 'agent';
  message: string;
  message_type: 'text' | 'image' | 'file';
  timestamp: string;
  agent_run_id?: string;
}

export interface ChatHistoryResponse extends Array<ChatMessage> {}

export interface SendMessageRequest {
  message: string;
  message_type?: 'text' | 'image' | 'file';
  agent_run_id?: string;
}

export interface SendMessageResponse extends BaseResponse {
  response: string;
}

// ========================================
// WEB SCRAPING TYPES
// ========================================

export interface ScrapingRequest {
  url: string;
  selectors?: Record<string, string>;
  wait_time?: number;
  max_retries?: number;
}

export interface ScrapingResponse extends BaseResponse {
  url: string;
  title?: string;
  content?: string;
  timestamp: string;
  extracted_data?: Record<string, any>;
}

// ========================================
// FORM AUTOMATION TYPES
// ========================================

export interface LoginAutomationRequest {
  browser_id: string;
  url: string;
  username_selector: string;
  username: string;
  password_selector: string;
  password: string;
  submit_selector: string;
  success_indicator?: string;
}

export interface RegistrationRequest {
  url: string;
  form_data: Record<string, any>;
  browser_id: string;
  success_selector?: string;
}

export interface JobApplicationRequest {
  job_url: string;
  proposal_text: string;
  rate?: number;
  browser_id: string;
}

export interface BatchJobApplication {
  jobs: Array<{
    platform: 'upwork' | 'fiverr' | 'linkedin';
    url: string;
    proposal: string;
    rate?: number;
    price?: number;
  }>;
  browser_id: string;
}

export interface AutomationResponse extends BaseResponse {
  result: {
    success: boolean;
    message?: string;
    current_url?: string;
    application_id?: string;
    status?: string;
    redirect_url?: string;
  };
}

// ========================================
// TOOL EXECUTION TYPES
// ========================================

export interface ToolCallRequest {
  tool_name: string;
  params: Record<string, any>;
}

export interface ToolCallResponse extends BaseResponse {
  result: any;
}

// ========================================
// PLAN EXECUTION TYPES
// ========================================

export interface PlanStep {
  action: string;
  params: Record<string, any>;
  description?: string;
}

export interface PlanExecutionRequest {
  plan: PlanStep[];
  name?: string;
  description?: string;
}

export interface PlanExecutionResponse extends BaseResponse {
  plan_id: number;
  status: 'pending' | 'running' | 'completed' | 'failed';
  current_step: number;
  total_steps: number;
  results: any[];
}

// ========================================
// FEEDBACK TYPES
// ========================================

export interface FeedbackRequest {
  plan_id: number;
  rating: number; // 1-5
  comment?: string;
  improvements?: string[];
}

export interface FeedbackResponse extends BaseResponse {
  feedback_id: number;
}

// ========================================
// HEALTH AND MONITORING TYPES
// ========================================

export interface HealthResponse extends BaseResponse {
  version: string;
  uptime_seconds: number;
  services: Record<string, 'healthy' | 'degraded' | 'unhealthy'>;
}

export interface MemoryStatsResponse extends BaseResponse {
  total_memory_mb: number;
  used_memory_mb: number;
  available_memory_mb: number;
  memory_usage_percent: number;
  cache_stats: {
    total_entries: number;
    cache_hits: number;
    cache_misses: number;
    hit_rate: number;
  };
}

// ========================================
// WEBSOCKET MESSAGE TYPES
// ========================================

export interface WebSocketMessage {
  topic: string;
  payload: any;
}

export interface AgentUpdateMessage extends WebSocketMessage {
  topic: 'agent_updates';
  payload: {
    log?: string;
    step?: number;
    action?: string;
    thought?: string;
    result?: any;
    error?: string;
  };
}

export interface ChatMessageWS extends WebSocketMessage {
  topic: 'chat';
  payload: {
    sender: 'user' | 'agent';
    message: string;
    message_type: 'text' | 'image' | 'file';
    agent_run_id?: string;
  };
}

// ========================================
// API CLIENT CLASS
// ========================================

export class ElchApiClient {
  private baseURL: string;
  private token: string | null = null;

  constructor(baseURL: string = 'http://localhost:8000') {
    this.baseURL = baseURL;
    this.token = localStorage.getItem('auth_token');
  }

  private getAuthHeaders(): Record<string, string> {
    return this.token ? { 'Authorization': `Bearer ${this.token}` } : {};
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...this.getAuthHeaders(),
        ...options.headers
      }
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Request failed');
    }

    return response.json();
  }

  // Authentication methods
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    const formData = new FormData();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const response = await fetch(`${this.baseURL}/token`, {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      throw new Error('Login failed');
    }

    const data = await response.json();
    this.token = data.access_token;
    localStorage.setItem('auth_token', this.token);
    return data;
  }

  async signup(userData: SignupRequest): Promise<User> {
    return this.request<User>('/signup', {
      method: 'POST',
      body: JSON.stringify(userData)
    });
  }

  async getCurrentUser(): Promise<User> {
    return this.request<User>('/me');
  }

  logout(): void {
    this.token = null;
    localStorage.removeItem('auth_token');
  }

  // Agent methods
  async runAgent(request: AgentStateRequest): Promise<AgentRunResponse> {
    return this.request<AgentRunResponse>('/agent/run', {
      method: 'POST',
      body: JSON.stringify(request)
    });
  }

  async sendPrompt(request: PromptRequest): Promise<PromptResponse> {
    return this.request<PromptResponse>('/prompt', {
      method: 'POST',
      body: JSON.stringify(request)
    });
  }

  // Task methods
  async getTaskResults(
    limit: number = 50,
    offset: number = 0,
    status?: string
  ): Promise<TaskResultsResponse> {
    const params = new URLSearchParams({
      limit: limit.toString(),
      offset: offset.toString()
    });

    if (status) {
      params.append('status', status);
    }

    return this.request<TaskResultsResponse>(`/api/tasks/results?${params}`);
  }

  async getTaskStatistics(days: number = 30): Promise<TaskStatistics> {
    return this.request<TaskStatistics>(`/api/tasks/statistics?days=${days}`);
  }

  async downloadTaskResult(taskId: number, format: 'json' | 'txt' = 'json'): Promise<Blob> {
    const response = await fetch(
      `${this.baseURL}/api/tasks/${taskId}/download?format=${format}`,
      {
        headers: this.getAuthHeaders()
      }
    );

    if (!response.ok) {
      throw new Error('Download failed');
    }

    return response.blob();
  }

  // Chat methods
  async getChatHistory(): Promise<ChatHistoryResponse> {
    return this.request<ChatHistoryResponse>('/chat/history');
  }

  async sendMessage(request: SendMessageRequest): Promise<SendMessageResponse> {
    return this.request<SendMessageResponse>('/chat/message', {
      method: 'POST',
      body: JSON.stringify(request)
    });
  }

  // Web scraping
  async scrapeWebsite(request: ScrapingRequest): Promise<ScrapingResponse> {
    return this.request<ScrapingResponse>('/scrape', {
      method: 'POST',
      body: JSON.stringify(request)
    });
  }

  // Form automation
  async automateLogin(request: LoginAutomationRequest): Promise<AutomationResponse> {
    return this.request<AutomationResponse>('/form/automate_login', {
      method: 'POST',
      body: JSON.stringify(request)
    });
  }

  async automateRegistration(request: RegistrationRequest): Promise<AutomationResponse> {
    return this.request<AutomationResponse>('/form/automate_registration', {
      method: 'POST',
      body: JSON.stringify(request)
    });
  }

  async applyForJob(request: JobApplicationRequest): Promise<AutomationResponse> {
    return this.request<AutomationResponse>('/form/apply_job_upwork', {
      method: 'POST',
      body: JSON.stringify(request)
    });
  }

  async executeTool(request: ToolCallRequest): Promise<ToolCallResponse> {
    return this.request<ToolCallResponse>('/call_tool', {
      method: 'POST',
      body: JSON.stringify(request)
    });
  }

  // Health check
  async healthCheck(): Promise<HealthResponse> {
    return this.request<HealthResponse>('/healthz');
  }

  async getMemoryStats(): Promise<MemoryStatsResponse> {
    return this.request<MemoryStatsResponse>('/memory/stats');
  }

  // WebSocket connection
  connectWebSocket(): WebSocket {
    if (!this.token) {
      throw new Error('No authentication token available');
    }

    const wsUrl = this.baseURL.replace('http', 'ws') + `/ws?token=${this.token}`;
    return new WebSocket(wsUrl);
  }
}

// ========================================
// REACT HOOKS (TypeScript)
// ========================================

export interface UseAuthReturn {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<LoginResponse>;
  logout: () => void;
  signup: (userData: SignupRequest) => Promise<User>;
}

export interface UseAgentReturn {
  response: AgentRunResponse | null;
  loading: boolean;
  askAgent: (question: string, runId?: string) => Promise<AgentRunResponse>;
  sendPrompt: (prompt: string) => Promise<PromptResponse>;
}

export interface UseTasksReturn {
  tasks: TaskResult[];
  statistics: TaskStatistics | null;
  loading: boolean;
  loadTasks: (limit?: number, offset?: number, status?: string) => Promise<TaskResultsResponse>;
  loadStatistics: (days?: number) => Promise<TaskStatistics>;
  downloadTask: (taskId: number, format?: 'json' | 'txt') => Promise<void>;
}

export interface UseChatReturn {
  messages: ChatMessage[];
  loading: boolean;
  loadHistory: () => Promise<ChatHistoryResponse>;
  sendMessage: (message: string, type?: string, runId?: string) => Promise<SendMessageResponse>;
  connectWebSocket: (onMessage: (data: WebSocketMessage) => void) => WebSocket;
  disconnectWebSocket: () => void;
}

// ========================================
// ERROR TYPES
// ========================================

export class ApiError extends Error {
  public statusCode: number;
  public details: any;

  constructor(message: string, statusCode: number = 500, details?: any) {
    super(message);
    this.statusCode = statusCode;
    this.details = details;
    this.name = 'ApiError';
  }
}

export class AuthenticationError extends ApiError {
  constructor(message: string = 'Authentication failed') {
    super(message, 401);
    this.name = 'AuthenticationError';
  }
}

export class ValidationError extends ApiError {
  constructor(message: string, details?: any) {
    super(message, 422, details);
    this.name = 'ValidationError';
  }
}

export class RateLimitError extends ApiError {
  constructor(message: string = 'Rate limit exceeded') {
    super(message, 429);
    this.name = 'RateLimitError';
  }
}

// ========================================
// UTILITY TYPES
// ========================================

export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

export interface ApiConfig {
  baseURL: string;
  timeout: number;
  retries: number;
}

export interface RequestOptions {
  method?: HttpMethod;
  headers?: Record<string, string>;
  body?: any;
  timeout?: number;
}

// Export default client instance
export const apiClient = new ElchApiClient();
