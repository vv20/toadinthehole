import { confirmResetPassword } from "aws-amplify/auth";
import { ChangeEvent, Dispatch, FormEvent, useState } from "react";
import "./Button.css";
import "./InputField.css";
import "./InputLabel.css";
import { ThemeType } from "./ThemeType";

function ChangePasswordForm({
  themeType,
  username,
  setLogInError,
  setRequirePasswordChange,
}: {
  themeType: ThemeType;
  username: string;
  setLogInError: Dispatch<string>;
  setRequirePasswordChange: Dispatch<boolean>;
}) {
  const [formData, setFormData] = useState({
    password: "",
    code: "",
  });

  function handleChange(event: ChangeEvent<HTMLInputElement>) {
    const { name, value } = event.target;
    setFormData((prevFormData) => ({ ...prevFormData, [name]: value }));
  }

  async function handlePasswordChange(event: FormEvent) {
    try {
      event.preventDefault();
      await confirmResetPassword({
        username: username,
        newPassword: formData.password,
        confirmationCode: formData.code,
      });
    } catch (error) {
      console.log(error);
      setLogInError("Error while setting a new password");
      setRequirePasswordChange(false);
    }
  }

  return (
    <form onSubmit={handlePasswordChange}>
      <label className={"InputLabel InputLabel-" + themeType}>Password:</label>
      <input
        className={"InputField InputField-" + themeType}
        type="text"
        id="password"
        name="password"
        onChange={handleChange}
      />
      <br />

      <label className={"InputLabel InputLabel-" + themeType}>
        Confirmation code:
      </label>
      <input
        className={"InputField InputField-" + themeType}
        type="text"
        id="code"
        name="code"
        onChange={handleChange}
      />
      <br />

      <button className={"Button Button-" + themeType} type="submit">
        Log In
      </button>
    </form>
  );
}

export default ChangePasswordForm;
