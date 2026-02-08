// utils/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Get the JWT token from localStorage
 */
function getToken(): string | null {
  return localStorage.getItem('auth_token');
}

/**
 * Generic API request function
 */
export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {},
  userId?: number
): Promise<T> {
  // Get the JWT token from localStorage
  const token = getToken();

  // Construct the URL based on whether userId is provided
  let url;
  if (userId !== undefined) {
    // For user-specific endpoints like /api/v1/users/{userId}/tasks
    url = `${API_BASE_URL}/api/v1/users/${userId}${endpoint}`;
  } else {
    // For general endpoints
    url = `${API_BASE_URL}${endpoint}`;
  }

  const config: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    },
    ...options,
  };

  let response;
  try {
    response = await fetch(url, config);
  } catch (networkError) {
    // Handle network errors (e.g., server not reachable, CORS issues)
    console.error(`Network error when calling ${url}:`, networkError);
    throw new Error(`Network error: Unable to reach the server. Please make sure the backend is running on ${API_BASE_URL}.`);
  }

  // Handle different response types appropriately
  if (!response.ok) {
    // Try to get error message from response body
    let errorMessage = `HTTP error! Status: ${response.status}`;
    try {
      const errorBody = await response.text();
      if (errorBody) {
        errorMessage += ` - ${errorBody}`;
      }
    } catch (e) {
      // If we can't parse the error body, just use the status code
    }

    throw new Error(errorMessage);
  }

  // Handle responses that might not have JSON bodies (like DELETE)
  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/json')) {
    return response.json();
  } else {
    // For responses without JSON body (like DELETE), return void or a simple success indicator
    return {} as T;
  }
}

/**
 * Get all tasks for a user
 */
export async function getUserTasks(userId: number, queryParams?: string): Promise<any[]> {
  const queryString = queryParams ? `?${queryParams}` : '';
  return apiRequest(`/tasks${queryString}`, {}, userId);
}

/**
 * Create a new task for a user
 */
export async function createUserTask(
  userId: number,
  taskData: {
    title: string;
    description: string;
    priority: 'low' | 'medium' | 'high';
    category: string;
    due_date: string | null
  }
): Promise<any> {
  return apiRequest(
    `/tasks`,
    {
      method: 'POST',
      body: JSON.stringify(taskData),
    },
    userId
  );
}

/**
 * Update a task for a user
 */
export async function updateUserTask(
  userId: number,
  taskId: number,
  taskData: {
    title?: string;
    description?: string;
    completed?: boolean;
    priority?: 'low' | 'medium' | 'high';
    category?: string;
    due_date?: string | null;
  }
): Promise<any> {
  return apiRequest(
    `/tasks/${taskId}`,
    {
      method: 'PUT',
      body: JSON.stringify(taskData),
    },
    userId
  );
}

/**
 * Delete a task for a user
 */
export async function deleteUserTask(userId: number, taskId: number): Promise<void> {
  await apiRequest(
    `/tasks/${taskId}`,
    {
      method: 'DELETE',
    },
    userId
  );
}

/**
 * Toggle task completion status
 */
export async function toggleTaskCompletion(userId: number, taskId: number): Promise<any> {
  return apiRequest(
    `/tasks/${taskId}/complete`,
    {
      method: 'PATCH',
    },
    userId
  );
}