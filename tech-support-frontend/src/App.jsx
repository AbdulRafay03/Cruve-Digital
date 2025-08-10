import React, { useState, useRef, useEffect } from 'react';
import { MessageCircle, X, Send } from 'lucide-react';

// ChatMessage Component - Renders individual chat messages
const ChatMessage = ({ message }) => {
  const { sender, text } = message;
  const isUser = sender === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-xs lg:max-w-md px-4 py-2 rounded-2xl ${
          isUser
            ? 'bg-gradient-to-r from-teal-500 to-blue-500 text-white'
            : 'bg-gray-700 text-gray-100'
        }`}
      >
      <p className="text-sm font-medium whitespace-pre-line">{text}</p>
      </div>
    </div>
  );
};

// ChatInput Component - Handles message input and sending
const ChatInput = ({ onSendMessage, isLoading }) => {
  const [message, setMessage] = useState('');
  
  /**
   * Handles form submission
   * Prevents empty messages and calls parent's send function
   */
  const handleSubmit = () => {
    if (message.trim() && !isLoading) {
      onSendMessage(message);
      setMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSubmit();
    }
  };

  return (
    <div className="flex gap-2 p-4 border-t border-gray-600">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder="Type your message..."
        disabled={isLoading}
        className="flex-1 bg-gray-700 text-white px-4 py-2 rounded-full border border-gray-600 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent placeholder-gray-400 disabled:opacity-50"
      />
      <button
        onClick={handleSubmit}
        disabled={!message.trim() || isLoading}
        className="bg-gradient-to-r from-teal-500 to-blue-500 text-white p-2 rounded-full hover:from-teal-600 hover:to-blue-600 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Send size={20} />
      </button>
    </div>
  );
};

// ChatWindow Component - Main chatbot interface
const ChatWindow = ({ isOpen, onClose, isEmbedded = false }) => {
  // State for managing chat messages and loading status
  const [messages, setMessages] = useState([
    { sender: 'assistant', text: 'Hello! I\'m your Technical Support Assistant. How can I help you today?' }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  /**
   * Auto-scrolls to the bottom of chat when new messages are added
   */
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  /**
   * Handles sending messages to the backend API
   * @param {string} userMessage - The message typed by the user
   */
  const handleSendMessage = async (userMessage) => {
    // Add user message to chat immediately
    const userMsg = { sender: 'user', text: userMessage };
    setMessages(prev => [...prev, userMsg]);
    setIsLoading(true);

    try {
      // Send POST request to backend API
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userMessage }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      // Add assistant response to chat
      const assistantMsg = { 
        sender: 'assistant', 
        text: data.response || 'I apologize, but I couldn\'t process your request right now.' 
      };
      setMessages(prev => [...prev, assistantMsg]);
      
    } catch (error) {
      console.error('Error sending message:', error);
      // Add error message to chat
      const errorMsg = { 
        sender: 'assistant', 
        text: 'I\'m having trouble connecting right now. Please try again later.' 
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen && !isEmbedded) return null;

  const containerClasses = isEmbedded 
    ? "w-full h-96 flex flex-col" 
    : "fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50";
    
  const chatClasses = isEmbedded 
    ? "bg-gray-800 w-full h-full flex flex-col" 
    : "bg-gray-800 rounded-2xl w-full max-w-md h-96 flex flex-col shadow-2xl";

  return (
    <div className={containerClasses}>
      <div className={chatClasses}>
        {/* Chat Header - only show for modal version */}
        {!isEmbedded && (
          <div className="flex items-center justify-between p-4 border-b border-gray-600">
            <h3 className="text-white font-semibold">Support Assistant</h3>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-white transition-colors"
            >
              <X size={24} />
            </button>
          </div>
        )}
        
        {/* Messages Container */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message, index) => (
            <ChatMessage key={index} message={message} />
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-700 text-gray-100 px-4 py-2 rounded-2xl">
                <div className="flex space-x-2">
                  <div className="w-2 h-2 bg-teal-500 rounded-full animate-pulse"></div>
                  <div className="w-2 h-2 bg-teal-500 rounded-full animate-pulse" style={{animationDelay: '0.2s'}}></div>
                  <div className="w-2 h-2 bg-teal-500 rounded-full animate-pulse" style={{animationDelay: '0.4s'}}></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        
        {/* Message Input */}
        <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
};

// ChatButton Component - Floating chat button
const ChatButton = ({ onClick }) => {
  return (
    <button
      onClick={onClick}
      className="fixed bottom-6 right-6 bg-gradient-to-r from-teal-500 to-blue-500 text-white p-4 rounded-full shadow-lg hover:shadow-xl hover:scale-110 transition-all duration-300 z-40"
    >
      <MessageCircle size={24} />
    </button>
  );
};

// Page1 Component - Landing/Welcome page
const Page1 = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 flex items-center justify-center relative">
      <div className="text-center px-6">
        <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 tracking-tight">
          Welcome to the
          <span className="block bg-gradient-to-r from-teal-400 to-blue-400 bg-clip-text text-transparent">
            Technical Support
          </span>
          <span className="block">Assistant</span>
        </h1>
        <div className="w-32 h-1 bg-gradient-to-r from-teal-500 to-blue-500 mx-auto mb-8 rounded-full"></div>
        <p className="text-xl text-gray-300 max-w-2xl mx-auto leading-relaxed">
          Get instant help with your technical questions. Our AI assistant is here to provide 
          expert support whenever you need it.
        </p>
      </div>
      
      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <div className="w-6 h-10 border-2 border-gray-400 rounded-full flex justify-center">
          <div className="w-1 h-3 bg-gray-400 rounded-full mt-2 animate-pulse"></div>
        </div>
      </div>
    </div>
  );
};

// Page2 Component - Support interaction page with embedded chat
const Page2 = ({ isChatOpen, setIsChatOpen }) => {
  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center px-6 py-12">
      <div className="max-w-2xl w-full">
        <div className="text-center mb-8">
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Technical Support Assistant
          </h2>
          <p className="text-xl text-gray-400">
            Get instant help with your technical questions
          </p>
        </div>
        
        {/* Embedded Chat Window */}
        <div className="bg-gray-800 rounded-2xl shadow-2xl overflow-hidden">
          <ChatWindow isOpen={true} onClose={() => {}} isEmbedded={true} />
        </div>
      </div>
    </div>
  );
};

// Main App Component
const App = () => {
  // State for managing chatbot visibility
  const [isChatOpen, setIsChatOpen] = useState(false);
  
  // Refs for smooth scrolling between pages
  const page1Ref = useRef(null);
  const page2Ref = useRef(null);

  /**
   * Handles smooth scrolling to specific page sections
   * @param {React.RefObject} targetRef - Reference to the target page element
   */
  const scrollToPage = (targetRef) => {
    targetRef.current?.scrollIntoView({ 
      behavior: 'smooth',
      block: 'start'
    });
  };

  /**
   * Handles scroll events to enable page navigation
   */
  useEffect(() => {
    const handleScroll = () => {
      const scrollY = window.scrollY;
      const windowHeight = window.innerHeight;
      
      // Auto-scroll to page 2 when user scrolls past halfway point of page 1
      if (scrollY > windowHeight * 0.5) {
        scrollToPage(page2Ref);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="font-['Inter'] antialiased">
      {/* Page 1 - Landing */}
      <div ref={page1Ref}>
        <Page1 />
      </div>
      
      {/* Page 2 - Support Interaction with Embedded Chat */}
      <div ref={page2Ref}>
        <Page2 isChatOpen={isChatOpen} setIsChatOpen={setIsChatOpen} />
      </div>
    </div>
  );
};

export default App;