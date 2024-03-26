import { Dispatch, useState } from "react";

import ChangePasswordForm from "./ChangePasswordForm";
import LoginForm from "./LoginForm";
import { ThemeType } from "./ThemeType";

function LoginPage({
  themeType,
  setIsLoggedIn,
}: {
  themeType: ThemeType;
  setIsLoggedIn: Dispatch<boolean>;
}) {
  const [requirePasswordChange, setRequirePasswordChange] = useState(false);
  const [logInError, setLogInError] = useState("");
  const [username, setUsername] = useState("");

  if (requirePasswordChange) {
    return (
      <div>
        <b>{logInError}</b>

        <ChangePasswordForm
          themeType={themeType}
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

        <LoginForm
          themeType={themeType}
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
