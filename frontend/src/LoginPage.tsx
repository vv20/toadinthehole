import { Dispatch, useState } from "react";

import "./LoginPage.css";

import ChangePasswordForm from "./ChangePasswordForm";
import LoginForm from "./LoginForm";

function LoginPage({ setIsLoggedIn }: { setIsLoggedIn: Dispatch<boolean> }) {
  const [requirePasswordChange, setRequirePasswordChange] = useState(false);
  const [logInError, setLogInError] = useState("");
  const [username, setUsername] = useState("");

  if (requirePasswordChange) {
    return (
      <div>
        <b>{logInError}</b>
        <br />

        <ChangePasswordForm
          username={username}
          setLogInError={setLogInError}
          setRequirePasswordChange={setRequirePasswordChange}
        />
      </div>
    );
  } else {
    return (
      <div>
        <b>{logInError}</b>
        <br />

        <LoginForm
          setIsLoggedIn={setIsLoggedIn}
          setLogInError={setLogInError}
          setRequirePasswordChange={setRequirePasswordChange}
          setUsername={setUsername}
        />
      </div>
    );
  }
}

export default LoginPage;
