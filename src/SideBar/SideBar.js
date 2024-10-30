import React from 'react';
import './SideBar.css';
import axios from 'axios';

function Sidebar({user_id, conversations, selectConversation, setConversations}) {
  let rev_conversations = [...conversations].reverse()
  const startNewConversation = async () => {

    try {
      const response = await axios.post('http://localhost:5000/start_conversation', {
        userid: user_id,
      });
  
      const success = response.data.success;
      if(success)
        {const conversations = response.data.conversations;
      const conversation_list = Object.entries(conversations).map(([key, value]) => ({
        title: key,
        messages: value,
      }));
      setConversations(conversation_list)
      selectConversation(conversation_list.length - 1)}
      else {
        alert('Issue with starting conversation. Please try again later')
      }
    } catch (error) {
      if (error.response) {
        alert(error.response.data.error || 'Starting Conversation Failed');
      } else {
        alert('An error occurred. Please try again.');
      }
    } 
    // finally {
    // }
  };

  const capitalizeFirstLetter = (string) => {
    if (!string) return '';
      if(string.length > 30){
        return string.charAt(0).toUpperCase() + string.slice(1,30) + "...";
      } else{
        return string.charAt(0).toUpperCase() + string.slice(1)
      }
  };

  function getConvTitle(conversation){
    if(conversation.messages[conversation.messages.length - 2]){
      return capitalizeFirstLetter(conversation.messages[conversation.messages.length - 2].content)
    } else{
      return "New Conversation"
    }
  }

  return (
    <div className="sidebar gradient-background">
      <h2>Your History</h2>
      <ul>
        {rev_conversations.map((conversation, index) => (
          <li key={index} onClick={() => selectConversation(rev_conversations.length - index - 1)}>
            {getConvTitle(conversation)}
          </li>
        ))}
      </ul>
      <div className="conv-input glow-on-hover">
      <button onClick={startNewConversation}>New Conversation</button>
    </div>
    </div>
  );
}

export default Sidebar;