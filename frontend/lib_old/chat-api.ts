export async function sendChatMessage(
  userId: string,
  message: string,
  conversationId?: number,
  token?: string
): Promise<any> {
  
  console.log('════════════════════════════════════');
  console.log('CHAT API CALL STARTED');
  console.log('════════════════════════════════════');
  console.log('Step 1: Input parameters');
  console.log('  userId:', userId);
  console.log('  message:', message);
  console.log('  conversationId:', conversationId);
  console.log('  token provided:', !!token);
  
  let authToken = token;
  if (!authToken && typeof window !== 'undefined') {
    authToken = localStorage.getItem('auth_token');
    console.log('Step 2: Retrieved token from localStorage');
  }
  
  if (!authToken) {
    console.error('Step 2: FAILED - No token available');
    throw new Error('Please log in to use chat');
  }
  console.log('  token (first 15 chars):', authToken.substring(0, 15));

  const url = "http://localhost:8000/api/" + userId + "/chat";
  console.log('Step 3: Built URL:', url);

  const requestBody = { 
    conversation_id: conversationId, 
    message 
  };
  console.log('Step 4: Request body:', JSON.stringify(requestBody));

  console.log('Step 5: Making fetch request...');
  
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + authToken,
      },
      body: JSON.stringify(requestBody),
    });

    console.log('Step 6: Fetch completed');
    console.log('  status:', response.status);
    console.log('  statusText:', response.statusText);
    console.log('  ok:', response.ok);

    if (!response.ok) {
      const errorText = await response.text();
      console.error('Step 7: Response not OK');
      console.error('  error body:', errorText);
      throw new Error(`Server returned ${response.status}: ${errorText}`);
    }

    const data = await response.json();
    console.log('Step 7: Parsed response:', data);
    console.log('════════════════════════════════════');
    console.log('CHAT API CALL SUCCEEDED');
    console.log('════════════════════════════════════');
    return data;

  } catch (error: any) {
    console.error('════════════════════════════════════');
    console.error('CHAT API CALL FAILED');
    console.error('════════════════════════════════════');
    console.error('Error name:', error.name);
    console.error('Error message:', error.message);
    console.error('Error stack:', error.stack);
    console.error('Full error object:', error);
    console.error('════════════════════════════════════');
    throw error;
  }
}