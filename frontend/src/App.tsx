import { Amplify } from "aws-amplify";
import { getCurrentUser } from "aws-amplify/auth";
import { useEffect, useState } from "react";

import "./App.css";

import LoginPage from "./LoginPage";
import Main from "./Main";

import amplifyconfiguration from "./amplifyconfiguration.json";

Amplify.configure(amplifyconfiguration);

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const checkLogIn = async () => {
      try {
        const { username } = await getCurrentUser();
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
        <h1>Log In:</h1>
        <LoginPage setIsLoggedIn={setIsLoggedIn} />
      </div>
    );
  } else {
    return (
      <div className="App">
        <Main />
      </div>
    );
  }
}

export default App;
