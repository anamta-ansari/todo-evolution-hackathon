"use client";

import { useState, useRef, useEffect } from "react";
import { X, MessageCircle, Send, Minimize2, Maximize2 } from "lucide-react";
import { useAuth } from "@/contexts/AuthContext";
import { sendChatMessage } from "@/lib/chat-api";
import { emitTaskUpdated } from "@/lib/events";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export default function FloatingChat() {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { user, token, isLoading: authIsLoading } = useAuth();
  const [showLoginPrompt, setShowLoginPrompt] = useState(false);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Check authentication when component mounts or opens
  useEffect(() => {
    if (isOpen && !user && !authIsLoading) {
      setShowLoginPrompt(true);
    } else {
      setShowLoginPrompt(false);
    }
  }, [isOpen, user, authIsLoading]);

  // Add welcome message when chat opens for first time
  useEffect(() => {
    if (isOpen && messages.length === 0 && user) {
      const welcomeMessage: Message = {
        id: "welcome",
        role: "assistant",
        content: "Hi! I'm your AI assistant. I can help you manage your tasks. Try saying 'Add a task to buy groceries' or 'Show me my tasks'.",
        timestamp: new Date(),
      };
      setMessages([welcomeMessage]);
    }
  }, [isOpen, messages.length, user]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    // Get token
    const authToken = token || localStorage.getItem('auth_token');
    
    if (!authToken) {
      console.error('[CHAT] No auth token');
      const errorMsg: Message = {
        id: Date.now().toString(),
        role: "assistant",
        content: "Please log in to use chat",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMsg]);
      return;
    }

    // Extract user ID from token (ALWAYS decode, don't rely on user object)
    let userId: string;
    try {
      const base64Url = authToken.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const payload = JSON.parse(window.atob(base64));
      userId = payload.user_id || payload.sub || payload.id;
      console.log('[CHAT] Extracted userId:', userId);
    } catch (e) {
      console.error('[CHAT] Failed to decode token:', e);
      const errorMsg: Message = {
        id: Date.now().toString(),
        role: "assistant",
        content: "Authentication error. Please log in again.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMsg]);
      return;
    }

    if (!userId) {
      console.error('[CHAT] No userId in token');
      return;
    }

    // Create user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      console.log('[CHAT] Sending message...');
      
      const response = await sendChatMessage(
        userId,
        userMessage.content,
        conversationId || undefined,
        authToken
      );

      console.log('[CHAT] Got response:', response);

      if (response.conversation_id && !conversationId) {
        setConversationId(response.conversation_id);
      }

      // Check if response contains tool calls that affect tasks
      if (response.tool_calls && response.tool_calls.length > 0) {
        const hasTaskOperation = response.tool_calls.some(
          (call: any) => ['add_task', 'complete_task', 'delete_task', 'update_task'].includes(call.tool)
        );
        
        if (hasTaskOperation) {
          console.log('[CHAT] Task operation detected, emitting update event');
          emitTaskUpdated(); // Notify dashboard to refresh
        }
      }

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.response || "Message received",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);

    } catch (error: any) {
      console.error('[CHAT] Error:', error);
      
      let errorText = "Sorry, I encountered an error. ";
      
      if (error.message?.includes('Failed to fetch') || error.message?.includes('NetworkError')) {
        errorText = "Failed to connect to server. Make sure the backend is running on http://localhost:8000";
      } else {
        errorText += error.message || "Please try again.";
      }

      const errorMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: errorText,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 bg-pink-600 hover:bg-pink-700 text-white rounded-full p-4 shadow-lg transition-all duration-300 hover:scale-110 z-50"
        aria-label="Open chat"
      >
        <MessageCircle className="w-6 h-6" />
      </button>
    );
  }

  return (
    <div
      className={`fixed bottom-6 right-6 bg-white dark:bg-gray-800 rounded-lg shadow-2xl z-50 transition-all duration-300 ${
        isMinimized ? "h-14" : "h-[600px]"
      } w-96 flex flex-col border border-gray-200 dark:border-gray-700`}
    >
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700 bg-gradient-to-r from-pink-600 to-pink-700 text-white rounded-t-lg">
        <div className="flex items-center gap-2">
          <MessageCircle className="w-5 h-5" />
          <h3 className="font-semibold">AI Assistant</h3>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setIsMinimized(!isMinimized)}
            className="hover:bg-pink-800 p-1 rounded transition-colors"
            aria-label={isMinimized ? "Maximize" : "Minimize"}
          >
            {isMinimized ? (
              <Maximize2 className="w-4 h-4" />
            ) : (
              <Minimize2 className="w-4 h-4" />
            )}
          </button>
          <button
            onClick={() => setIsOpen(false)}
            className="hover:bg-pink-800 p-1 rounded transition-colors"
            aria-label="Close chat"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Chat Content - Only show when not minimized */}
      {!isMinimized && (
        <>
          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50 dark:bg-gray-900">
            {showLoginPrompt ? (
              <div className="flex flex-col items-center justify-center h-full p-4">
                <MessageCircle className="w-12 h-12 mx-auto mb-4 text-gray-400" />
                <h3 className="text-lg font-semibold mb-2">Login Required</h3>
                <p className="text-gray-600 dark:text-gray-400 text-center mb-4">
                  Please log in to use the AI assistant.
                </p>
                <button
                  onClick={() => {
                    // Redirect to login page
                    window.location.href = '/signin';
                  }}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
                >
                  Go to Login
                </button>
              </div>
            ) : messages.length === 0 ? (
              <div className="text-center text-gray-500 dark:text-gray-400 mt-8">
                <MessageCircle className="w-12 h-12 mx-auto mb-3 opacity-50" />
                <p className="text-sm">Start a conversation with your AI assistant</p>
                <p className="text-xs mt-2">Try: "Add a task to buy groceries"</p>
              </div>
            ) : (
              messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${
                    message.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg p-3 ${
                      message.role === "user"
                        ? "bg-pink-600 text-white"
                        : "bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 border border-gray-200 dark:border-gray-700"
                    }`}
                  >
                    <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                    <p
                      className={`text-xs mt-1 ${
                        message.role === "user"
                          ? "text-pink-100"
                          : "text-gray-500 dark:text-gray-400"
                      }`}
                    >
                      {message.timestamp.toLocaleTimeString([], {
                        hour: "2-digit",
                        minute: "2-digit",
                      })}
                    </p>
                  </div>
                </div>
              ))
            )}
            {isLoading && (
              <div className="flex justify-start">
                <div className="bg-white dark:bg-gray-800 rounded-lg p-3 border border-gray-200 dark:border-gray-700">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100" />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200" />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-4 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
            {showLoginPrompt ? (
              <div className="text-center text-gray-500 dark:text-gray-400 py-2">
                Log in to enable chat functionality
              </div>
            ) : (
              <div className="flex gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Type your message..."
                  disabled={isLoading}
                  className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 dark:bg-gray-700 dark:text-white disabled:opacity-50"
                />
                <button
                  onClick={handleSend}
                  disabled={!input.trim() || isLoading}
                  className="bg-pink-600 hover:bg-pink-700 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg transition-colors flex items-center gap-2"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}