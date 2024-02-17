import { resetPassword, signIn } from "aws-amplify/auth";
import { ChangeEvent, Dispatch, FormEvent, useState } from "react";

import "./LoginForm.css";

function LoginForm({
  setIsLoggedIn,
  setLogInError,
  setRequirePasswordChange,
  setUsername,
}: {
  setIsLoggedIn: Dispatch<boolean>;
  setLogInError: Dispatch<string>;
  setRequirePasswordChange: Dispatch<boolean>;
  setUsername: Dispatch<string>;
}) {
  const [formData, setFormData] = useState({ username: "", password: "" });

  function handleChange(event: ChangeEvent<HTMLInputElement>) {
    const { name, value } = event.target;
    setFormData((prevFormData) => ({ ...prevFormData, [name]: value }));
  }

  async function handleSignIn(event: FormEvent) {
    try {
      event.preventDefault();

      const { nextStep } = await signIn({
        username: formData.username,
        password: formData.password,
      });

      switch (nextStep.signInStep) {
        case "DONE": {
          setIsLoggedIn(true);
          break;
        }
        case "CONFIRM_SIGN_IN_WITH_NEW_PASSWORD_REQUIRED": {
          setLogInError("Set a new password:");
          setRequirePasswordChange(true);
          setUsername(formData.username);
          resetPassword({ username: formData.username });
          break;
        }
        default: {
          setLogInError("Incorrect username or password");
        }
      }
    } catch (error) {
      setLogInError("Error while signing in");
    }
  }

  return (
    <form onSubmit={handleSignIn}>
      <label>Email:</label>
      <input
        type="text"
        id="username"
        name="username"
        onChange={handleChange}
      />
      <br />

      <label>Password:</label>
      <input
        type="text"
        id="password"
        name="password"
        onChange={handleChange}
      />
      <br />

      <button type="submit">Log In</button>
    </form>
  );
}

export default LoginForm;
