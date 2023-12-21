import { getCurrentUser } from "aws-amplify/auth";
import { useEffect, useState } from "react";

import "./App.css";
import logo from "./logo.svg";

import LoginForm from "./LoginForm";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const checkLogIn = async () => {
      try {
        const { username, userId, signInDetails } = await getCurrentUser();
        console.log(username);
        setIsLoggedIn(true);
      } catch (e) {
        console.log(e);
        setIsLoggedIn(false);
      }
    };
    checkLogIn();
  }, []);

  if (!isLoggedIn) {
    return (
      <div className="App">
        <LoginForm />
      </div>
    );
  } else {
    return (
      <div className="App">
        <img src={logo} className="App-logo" alt="logo" />
      </div>
    );
  }
}

export default App;
