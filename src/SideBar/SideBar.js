import React from 'react';
import './SideBar.css';
import axios from 'axios';

function Sidebar({user_id, conversations, selectConversation, setConversations}) {
  let rev_conversations = [...conversations].reverse()
  // const startNewConversation = () => {
    console.log("normal: ", conversations)
  console.log("reversed: ", rev_conversations)
  // };
  const startNewConversation = async () => {

    try {
      const response = await axios.post('http://localhost:5000/start_conversation', {
        userid: user_id,
      });
  
      // Handle success (store token, navigate, etc.)
      const success = response.data.success;
      const conversations = response.data.conversations;
      const conversation_list = Object.entries(conversations).map(([key, value]) => ({
        title: key,
        messages: value,
      }));
      console.log(conversation_list)
      setConversations(conversation_list)
      // rev_conversations = [...conversations].reverse()
      selectConversation(rev_conversations.length - 1)
    } catch (error) {
      // Handle error (e.g., network issue)
    } finally {
    }
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