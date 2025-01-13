import { Amplify } from "aws-amplify";
import { getCurrentUser } from "aws-amplify/auth";
import { ReactNode, useEffect } from "react";

import amplifyconfiguration from "./amplifyconfiguration.json";
import Header from "./components/header/Header";
import RecipeList from "./components/viewer/RecipeList";
import LoginPage from "./components/login/LoginPage";
import { useAppDispatch, useAppSelector } from "./redux/hooks";
import { logIn, logOut } from "./redux/userInfoSlice";
import ThemeType from "./util/ThemeType";

import "./styles/App.css";

Amplify.configure(amplifyconfiguration);

function App() {
    const dispatch = useAppDispatch();
    const themeType: ThemeType = useAppSelector((state) => state.theme).theme;
    const isLoggedIn: boolean = useAppSelector(state => state.userInfo).isLoggedIn;
    
    useEffect(() => {
        const checkLogIn = async () => {
            try {
                await getCurrentUser();
                dispatch(logIn());
            } catch (e) {
                console.log(e);
                dispatch(logOut());
            }
        };
        checkLogIn();
    }, [dispatch]);
    
    var child: ReactNode;
    if (!isLoggedIn) {
        child = <LoginPage/>;
    } else {
        child = (
            <RecipeList/>
        );
    }
    
    return (
        <div className={"App App-" + themeType}>
        <Header/>
        {child}
        </div>
    );
}

export default App;
