import { Dispatch, ReactNode } from "react";

import RecipeEditor from "../editor/RecipeEditor";
import { ThemeType } from "../../util/ThemeType";

import "../../styles/header/NewRecipeButton.css";

function NewRecipeButton({
    themeType,
    existingTags,
    setActiveRecipe,
}: {
    themeType: ThemeType;
    existingTags: string[];
    setActiveRecipe: Dispatch<ReactNode>;
}) {
    function openNewRecipeEditor() {
        setActiveRecipe(
            <RecipeEditor
            themeType={themeType}
            recipe={{}}
            setActiveRecipe={setActiveRecipe}
            existingTags={existingTags}
            />
        );
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
