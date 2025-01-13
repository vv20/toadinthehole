import ChangePasswordForm from "./ChangePasswordForm";
import LoginForm from "./LoginForm";
import { useAppSelector } from "../../redux/hooks";

function LoginPage() {
    const requirePasswordChange: boolean = useAppSelector((state) => state.userInfo).requirePasswordChange;
    const logInError: string = useAppSelector((state) => state.userInfo).loginError;
    
    if (requirePasswordChange) {
        return (
            <div>
            <b>{logInError}</b>
            <ChangePasswordForm />
            </div>
        );
    } else {
        return (
            <div>
            <b>{logInError}</b>
            <LoginForm />
            </div>
        );
    }
}

export default LoginPage;
