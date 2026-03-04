import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Loader } from 'lucide-react';
import { chatWithBot } from '../services/api';

const Chatbot = () => {
  const [messages, setMessages] = useState([
    {
      role: 'bot',
      content: 'Hi! 👋 I\'m your AI skincare assistant. Ask me anything about skincare, products, routines, or concerns!',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [skinType, setSkinType] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = {
      role: 'user',
      content: input,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await chatWithBot(input, skinType || null);
      
      const botMessage = {
        role: 'bot',
        content: response.message,
        source: response.source,
        confidence: response.confidence,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        role: 'bot',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const quickQuestions = [
    'How to treat acne?',
    'Best sunscreen for oily skin',
    'How to reduce dark circles?',
    'What causes wrinkles?',
    'Natural remedies for pigmentation'
  ];

  const handleQuickQuestion = (question) => {
    setInput(question);
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <Bot size={32} />
        <div>
          <h2>AI Skincare Assistant</h2>
          <p>Get instant answers to your skincare questions</p>
        </div>
      </div>

      {/* Skin Type Selector */}
      <div className="skin-type-selector">
        <label>Your skin type (optional):</label>
        <select 
          value={skinType}
          onChange={(e) => setSkinType(e.target.value)}
          className="skin-type-select"
        >
          <option value="">Not specified</option>
          <option value="Dry">Dry</option>
          <option value="Normal">Normal</option>
          <option value="Oily">Oily</option>
        </select>
      </div>

      {/* Quick Questions */}
      {messages.length === 1 && (
        <div className="quick-questions">
          <h4>Quick questions:</h4>
          <div className="quick-questions-grid">
            {quickQuestions.map((question, index) => (
              <button
                key={index}
                className="quick-question-btn"
                onClick={() => handleQuickQuestion(question)}
              >
                {question}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Messages */}
      <div className="chat-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <div className="message-avatar">
              {message.role === 'bot' ? <Bot size={24} /> : <User size={24} />}
            </div>
            <div className="message-content">
              <div className="message-bubble">
                {message.content.split('\n').map((line, i) => (
                  <p key={i}>{line}</p>
                ))}
              </div>
              {message.source && (
                <span className="message-meta">
                  {message.source === 'stored' ? '✨ Expert knowledge' : '🤖 AI generated'}
                </span>
              )}
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="message bot">
            <div className="message-avatar">
              <Bot size={24} />
            </div>
            <div className="message-content">
              <div className="message-bubble typing">
                <Loader className="spinner" size={20} />
                Thinking...
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="chat-input-container">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me anything about skincare..."
          className="chat-input"
          rows={1}
        />
        <button 
          onClick={handleSend}
          disabled={!input.trim() || loading}
          className="send-btn"
        >
          <Send size={20} />
        </button>
      </div>
    </div>
  );
};

export default Chatbot;