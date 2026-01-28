"use client";

export async function sendChatMessage(
  userId: string,
  message: string,
  conversationId?: number
) {
  // Get JWT token from auth context or storage
  // This assumes you have a way to get the JWT token from Better Auth
  const token = localStorage.getItem("better-auth.session_token"); // Adjust based on your auth implementation
  
  const response = await fetch(`/api/${userId}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}`
    },
    body: JSON.stringify({
      conversation_id: conversationId,
      message
    })
  });
  
  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.detail || "Chat request failed");
  }
  
  return response.json();
}