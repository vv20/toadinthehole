import { confirmResetPassword } from "aws-amplify/auth";
import { ChangeEvent, Dispatch, FormEvent, useState } from "react";

import "./ChangePasswordForm.css";

function ChangePasswordForm({
  username,
  setLogInError,
  setRequirePasswordChange,
}: {
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
      <label>Password:</label>
      <input
        type="text"
        id="password"
        name="password"
        onChange={handleChange}
      />
      <br />

      <label>Confirmation code:</label>
      <input type="text" id="code" name="code" onChange={handleChange} />
      <br />

      <button type="submit">Log In</button>
    </form>
  );
}

export default ChangePasswordForm;
