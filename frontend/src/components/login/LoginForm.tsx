import { resetPassword, signIn } from "aws-amplify/auth";
import { ChangeEvent, FormEvent, useState } from "react";

import { useAppDispatch, useAppSelector } from "../../redux/hooks";
import { logIn, setLogInError, setRequirePasswordChange, setUsername } from "../../redux/userInfoSlice";
import ThemeType from "../../util/ThemeType";

import "../../styles/container/LoginFormRow.css";
import "../../styles/general/Button.css";
import "../../styles/general/InputField.css";
import "../../styles/general/InputLabel.css";
import "../../styles/general/PageTitle.css";
import "../../styles/login/LoginForm.css";

function LoginForm() {
    const dispatch = useAppDispatch();
    const themeType: ThemeType = useAppSelector((state) => state.theme).theme;
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
                    dispatch(logIn());
                    break;
                }
                case "CONFIRM_SIGN_IN_WITH_NEW_PASSWORD_REQUIRED": {
                    dispatch(setLogInError({ loginError: "Set a new password:" }));
                    dispatch(setRequirePasswordChange({ requirePasswordChange: true }));
                    dispatch(setUsername({ username: formData.username }));
                    resetPassword({ username: formData.username });
                    break;
                }
                default: {
                    dispatch(setLogInError({ loginError: "Incorrect username or password" }));
                }
            }
        } catch (error) {
            dispatch(setLogInError({ loginError: "Error while signing in" }));
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
