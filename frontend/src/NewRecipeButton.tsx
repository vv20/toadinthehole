import { Dispatch, ReactNode } from "react";
import "./NewRecipeButton.css";
import RecipeEditor from "./RecipeEditor";
import { ThemeType } from "./ThemeType";

function NewRecipeButton({
  themeType,
  setActiveRecipe,
}: {
  themeType: ThemeType;
  setActiveRecipe: Dispatch<ReactNode>;
}) {
  function openNewRecipeEditor() {
    setActiveRecipe(<RecipeEditor themeType={themeType} recipe={{}} />);
  }

  return (
    <button
      className={"NewRecipeButton NewRecipeButton-" + themeType}
      onClick={openNewRecipeEditor}
    >
      Add New Recipe
    </button>
  );
}

export default NewRecipeButton;
