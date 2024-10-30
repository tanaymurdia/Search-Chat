import React from 'react';
import './ChatHistory.css';

function ChatHistory({ messages, loading }) {
  function parseTextWithButtons(inputText) {
    const anchorRegex = /<a\s+href=['"]([^'"]+)['"]>(.*?)<\/a>/gi;
    const chunks = [];
    let lastIndex = 0;
    let match;
  
    while ((match = anchorRegex.exec(inputText)) !== null) {
      // const fullTag = match[0];       
      const href = match[1];           
      const content = match[2];        
      const startIndex = match.index;
  
      if (startIndex > lastIndex) {
        chunks.push(<div>{inputText.substring(lastIndex, startIndex)}</div>);
      }
  
      chunks.push(
        <button className="glow-on-hover link-button" key={startIndex} onClick={() => window.open(href, '_blank')}>
          {content}
        </button>
      );
  
      lastIndex = anchorRegex.lastIndex;
    }
  
    if (lastIndex < inputText.length) {

      chunks.push(<div>{inputText.substring(lastIndex)}</div>);
    }
  
    return chunks;
  }

  
  return (
    <div className="chat-history">
      {messages.map((msg, index) => (
        <div key={index} className={`message ${msg.sender_type}`}>
          <span>{parseTextWithButtons(msg.content)}</span>
        </div>
      ))}
      {loading && <div key="loading" className={`message AI`}>
          <div className="loader"></div>
        </div>}
    </div>
  );
}

export default ChatHistory;