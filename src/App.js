import React, { useState, useEffect } from 'react';
import Sidebar from './SideBar/SideBar'
import ChatHistory from './ChatHistory/ChatHistory';
import ChatInput from './ChatInput/ChatInput';
import SignInForm from './SignIn/SignIn';
import axios from 'axios';
import './css/App.css';

function App() {
  const [conversations, setConversations] = useState();
  const [user_id, setUserId] = useState();
  const [selectedConversation, setSelectedConversation] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [signedIn, setSignedIn] =useState(false)

  function onSignInFunc(user_id, conversations){
    setUserId(user_id)
    setSignedIn(true)
    setConversations(conversations)
  }

  const scrollToBottom = () => {
    const timer = setTimeout(() => {
      const scrollContainer = document.querySelector('.chat-history');
      if (scrollContainer) {
        scrollContainer.scrollTo({
          top: scrollContainer.scrollHeight,
          behavior: 'smooth',  // enables smooth scrolling
        });
      }
    }, 100); // 2000 milliseconds delay

    return () => clearTimeout(timer);
  };

  // Optionally useEffect to run some initial scroll or other setup actions
  useEffect(() => {
    scrollToBottom();
  }, [selectedConversation]);

  const addMessage = async (message) => {
    conversations[selectedConversation].messages.push({
      sender_type: 'User',
      content: message,
    });
    scrollToBottom();
    const newConversations = [...conversations];
    let conversation_id = newConversations[selectedConversation].title
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:5000/add_message', {
        message: message,
        conversationid: conversation_id,
      });
  
      // Handle success (store token, navigate, etc.)
      const success = response.data.success;
     if (success)
      {const conversation = response.data.conversation;
      newConversations[selectedConversation] =  {
        title: newConversations[selectedConversation].title,
        messages: conversation
      }}else {
        alert('Issue with sending message. Please try again later')
      }
    } catch (error) {
      if (error.response) {
        alert(error.response.data.error || 'Sending message Failed');
      } else {
        alert('An error occurred. Please try again.');
      }
    } finally {
      scrollToBottom();
      setIsLoading(false);
      setConversations(newConversations);
    }
  };

  if (!signedIn) {
    return <SignInForm onSignIn={onSignInFunc} />;
  }
  return (
    <div className="App"> 
      {user_id && (
        <Sidebar
          user_id={user_id} 
          conversations={conversations}
          selectConversation={setSelectedConversation}
          setConversations={setConversations}
        />
      )}
      <div className="chat-container">
        {conversations.length > 0 && conversations[selectedConversation] ? (
          <ChatHistory messages={conversations[selectedConversation].messages} loading={isLoading} />
        ) : (
          <p className='no-conv'>No conversations available.</p>
        )}
        <ChatInput addMessage={addMessage} />
      </div>
    </div>
  );
}

export default App;