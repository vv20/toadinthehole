import { Amplify } from "aws-amplify";
import { getCurrentUser } from "aws-amplify/auth";
import { ReactNode, useEffect, useState } from "react";
import Header from "./Header";
import RecipeList from "./RecipeList";

import LoginPage from "./LoginPage";

import amplifyconfiguration from "./amplifyconfiguration.json";
import "./App.css";
import { ThemeType } from "./ThemeType";

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
