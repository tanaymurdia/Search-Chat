import React from 'react';
import './ChatHistory.css';

function ChatHistory({ messages, loading }) {
  function parseTextWithButtons(inputText) {
    const anchorRegex = /<a\s+href=['"]([^'"]+)['"]>(.*?)<\/a>/gi;
    const chunks = [];
    let lastIndex = 0;
    let match;
    console.log("Check")
  
    while ((match = anchorRegex.exec(inputText)) !== null) {
      console.log("Check 2")
      console.log(chunks)
      const fullTag = match[0];        // Complete match, like <a href='link'>text</a>
      const href = match[1];           // URL extracted from href
      const content = match[2];        // Placeholder text between <a> and </a>
      const startIndex = match.index;
  
      // Push regular text before the match
      if (startIndex > lastIndex) {
        chunks.push(<div>{inputText.substring(lastIndex, startIndex)}</div>);
      }
  
      // Create a button element
      chunks.push(
        <button className="glow-on-hover link-button" key={startIndex} onClick={() => window.open(href, '_blank')}>
          {content}
        </button>
      );
  
      lastIndex = anchorRegex.lastIndex;
    }
  
    // Push any remaining text after the last match
    if (lastIndex < inputText.length) {

      chunks.push(<div>{inputText.substring(lastIndex)}</div>);
    }
  
    return chunks;
  }
  
  const DynamicButtonsComponent = ({ text }) => {
    return (
      <div>
        <p>{parseTextWithButtons(text)}</p>
      </div>
    );
  };

  
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