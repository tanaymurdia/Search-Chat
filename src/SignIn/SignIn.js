import React, { useState } from 'react';
import axios from 'axios';
import './SignIn.css'

const SignInForm = ({onSignIn}) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleSignIn = async (e) => {
    e.preventDefault(); // Prevent form submission

    try {
      // Send a POST request to the /signin endpoint
      const response = await axios.post('http://localhost:5000/signin', {
        username: username,
        password: password,
      });

      // Handle success (store token, navigate, etc.)
      if(response.data.success)
        { const conversations = response.data.conversations;
      const user_id = response.data.user_id;
      const conversation_list = Object.entries(conversations).map(([key, value]) => ({
        title: key,
        messages: value,
      }));
    //   localStorage.setItem('authToken', token); // Example of storing the token
      onSignIn(user_id, conversation_list)
      setMessage('Sign-in successful!');}
      else {
        setMessage('Cannot Sign-In as Server seems to have an issue')
      }
    } catch (error) {
      if (error.response) {
        setMessage(error.response.data.error || 'Sign-in failed');
      } else {
        setMessage('An error occurred. Please try again.');
      }
    }
  };

  return (
    <div className="sign-in-container gradient-background">
      <form className="sign-in-form" onSubmit={handleSignIn}>
        <h2>Sign In</h2>
        <div className="form-group">
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        {message && <p>{message}</p>}
        </div>
        <button type="submit" className="sign-in-button">Sign In</button>
      </form>
    </div>
  );
};

export default SignInForm;