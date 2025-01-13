import { editRecipe } from "../../redux/activeRecipeSlice";
import { useAppDispatch, useAppSelector } from "../../redux/hooks";
import ThemeType from "../../util/ThemeType";

import "../../styles/header/NewRecipeButton.css";

function NewRecipeButton() {
    const dispatch = useAppDispatch();
    const themeType: ThemeType = useAppSelector((state) => state.theme).theme;
    
    function openNewRecipeEditor() {
        dispatch(editRecipe({recipeSlug: ""}));
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
