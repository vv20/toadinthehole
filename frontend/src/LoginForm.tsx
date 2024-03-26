import { resetPassword, signIn } from "aws-amplify/auth";
import { ChangeEvent, Dispatch, FormEvent, useState } from "react";
import "./Button.css";
import "./InputField.css";
import "./InputLabel.css";
import "./LoginForm.css";
import "./LoginFormRow.css";
import "./PageTitle.css";
import { ThemeType } from "./ThemeType";

function LoginForm({
  themeType,
  setIsLoggedIn,
  setLogInError,
  setRequirePasswordChange,
  setUsername,
}: {
  themeType: ThemeType;
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
    <div className={"LoginForm LoginForm-" + themeType}>
      <h1 className={"PageTitle PageTitle-" + themeType}>Log In:</h1>
      <form onSubmit={handleSignIn}>
        <div className={"LoginFormRow LoginFormRow-" + themeType}>
          <label className={"InputLabel InputLabel-" + themeType}>Email:</label>
          <input
            className={"InputField InputField-" + themeType}
            type="text"
            id="username"
            name="username"
            onChange={handleChange}
          />
        </div>

        <div className={"LoginFormRow LoginFormRow-" + themeType}>
          <label className={"InputLabel InputLabel-" + themeType}>
            Password:
          </label>
          <input
            className={"InputField InputField-" + themeType}
            type="password"
            id="password"
            name="password"
            onChange={handleChange}
          />
        </div>

        <div className={"LoginFormRow LoginFormRow-" + themeType}>
          <button className={"Button Button-" + themeType} type="submit">
            Log In
          </button>
        </div>
      </form>
    </div>
  );
}

export default LoginForm;
