import { confirmResetPassword } from "aws-amplify/auth";
import { ChangeEvent, FormEvent, useState } from "react";

import { useAppDispatch, useAppSelector } from "../../redux/hooks";
import { setLogInError, setRequirePasswordChange } from "../../redux/userInfoSlice";
import ThemeType from "../../util/ThemeType";

import "../../styles/general/Button.css";
import "../../styles/general/InputField.css";
import "../../styles/general/InputLabel.css";

function ChangePasswordForm() {
    const dispatch = useAppDispatch();
    const themeType: ThemeType = useAppSelector((state) => state.theme).theme;
    const username: string = useAppSelector((state) => state.userInfo).username;
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
            dispatch(setLogInError({ loginError: "Error while setting a new password" }));
            dispatch(setRequirePasswordChange({ requirePasswordChange: false }));
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