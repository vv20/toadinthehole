import { Amplify } from "aws-amplify";
import { getCurrentUser } from "aws-amplify/auth";
import { useEffect, useState } from "react";

import "./App.css";
import logo from "./logo.svg";

import LoginPage from "./LoginPage";

Amplify.configure({
  Auth: {
    Cognito: {
      userPoolId: "eu-west-2_14DbX1xkG",
      userPoolClientId: "1sn1af1lbustougtitif6ib08f",
      signUpVerificationMethod: "link",
    },
  },
});

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
        <img src={logo} className="App-logo" alt="logo" />
      </div>
    );
  }
}

export default App;
