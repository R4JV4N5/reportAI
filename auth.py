from sqlalchemy.orm import Session
from uuid import uuid4
from modelclass import UserDB
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

sessions = {}

def authenticate_user(db: Session, identifier: str, password: str):
    user = db.query(UserDB).filter(
        (UserDB.Username == identifier) | (UserDB.Email == identifier)
    ).first()
    if user and pwd_context.verify(password, user.Password):
        return user
    return None

def create_session(user):
    session_id = str(uuid4())
    sessions[session_id] = user
    return session_id





react_codes = """"

-------------------------->signup code

import React, { useState } from 'react';
import axios from 'axios';

const Signup = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleSignup = async (e) => {
    e.preventDefault();

    const userData = { username, email, password };

    try {
      const response = await axios.post('http://127.0.0.1:8000/signup', userData);
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response ? error.response.data.detail : 'Something went wrong!');
    }
  };

  return (
    <div>
      <h2>Signup</h2>
      <form onSubmit={handleSignup}>
        <input 
          type="text" 
          placeholder="Username" 
          value={username} 
          onChange={(e) => setUsername(e.target.value)} 
        />
        <input 
          type="email" 
          placeholder="Email" 
          value={email} 
          onChange={(e) => setEmail(e.target.value)} 
        />
        <input 
          type="password" 
          placeholder="Password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
        />
        <button type="submit">Signup</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default Signup;



---------------------->Login code

import React, { useState } from 'react';
import axios from 'axios';

const Login = ({ setLoggedIn }) => {
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://127.0.0.1:8000/login', {
        identifier,
        password,
      }, { withCredentials: true });

      setMessage(response.data.message);
      setLoggedIn(true); // Update the parent component to track the logged-in state
    } catch (error) {
      setMessage(error.response ? error.response.data.detail : 'Something went wrong!');
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <input 
          type="text" 
          placeholder="Username or Email" 
          value={identifier} 
          onChange={(e) => setIdentifier(e.target.value)} 
        />
        <input 
          type="password" 
          placeholder="Password" 
          value={password} 
          onChange={(e) => setPassword(e.target.value)} 
        />
        <button type="submit">Login</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default Login;


-------------------->logout code

import React from 'react';
import axios from 'axios';

const Logout = ({ setLoggedIn }) => {
  const handleLogout = async () => {
    try {
      await axios.post('http://127.0.0.1:8000/logout', {}, { withCredentials: true });
      setLoggedIn(false); // Update parent component to mark the user as logged out
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  return (
    <div>
      <h2>Logout</h2>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default Logout;


--------------------------->Main code

import React, { useState } from 'react';
import Signup from './Signup';
import Login from './Login';
import Logout from './Logout';

const App = () => {
  const [loggedIn, setLoggedIn] = useState(false);

  return (
    <div>
      <h1>React Authentication with FastAPI</h1>
      {loggedIn ? (
        <Logout setLoggedIn={setLoggedIn} />
      ) : (
        <>
          <Signup />
          <Login setLoggedIn={setLoggedIn} />
        </>
      )}
    </div>
  );
};

export default App;



"""