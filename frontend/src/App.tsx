import { Amplify } from "aws-amplify";
import { getCurrentUser } from "aws-amplify/auth";
import { ReactNode, useEffect, useState } from "react";
import Header from "./components/header/Header";
import RecipeList from "./components/viewer/RecipeList";

import LoginPage from "./components/login/LoginPage";

import amplifyconfiguration from "./amplifyconfiguration.json";
import "./styles/App.css";
import { ThemeType } from "./util/ThemeType";

Amplify.configure(amplifyconfiguration);

function App() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [themeType, setThemeType] = useState<ThemeType>(ThemeType.Pastel);
    const [activeRecipe, setActiveRecipe] = useState<ReactNode>();
    const [existingTags, setExistingTags] = useState<string[]>([]);
    
    useEffect(() => {
        const checkLogIn = async () => {
            try {
                await getCurrentUser();
                setIsLoggedIn(true);
            } catch (e) {
                console.log(e);
                setIsLoggedIn(false);
            }
        };
        checkLogIn();
    }, []);
    
    var child: ReactNode;
    if (!isLoggedIn) {
        child = <LoginPage setIsLoggedIn={setIsLoggedIn} themeType={themeType} />;
    } else {
        child = (
            <RecipeList
            themeType={themeType}
            activeRecipe={activeRecipe}
            existingTags={existingTags}
            setActiveRecipe={setActiveRecipe}
            setExistingTags={setExistingTags}
            />
        );
    }
    
    return (
        <div className={"App App-" + themeType}>
        <Header
        themeType={themeType}
        isLoggedIn={isLoggedIn}
        existingTags={existingTags}
        setThemeType={setThemeType}
        setActiveRecipe={setActiveRecipe}
        />
        {child}
        </div>
    );
}

export default App;
