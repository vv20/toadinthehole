import { Dispatch, ReactNode } from "react";

import Recipe from "./Recipe";
import { APIRecipePrevew } from "../../api/APIModel";
import { ThemeType } from "../../util/ThemeType";

import "../../styles/viewer/RecipePreview.css";

function RecipePreview({
    themeType,
    preview,
    existingTags,
    setActiveRecipe
}: {
    themeType: ThemeType;
    preview: APIRecipePrevew;
    existingTags: string[];
    setActiveRecipe: Dispatch<ReactNode>;
}) {
    function openRecipe() {
        setActiveRecipe(
            <Recipe
            themeType={themeType}
            preview={preview}
            existingTags={existingTags}
            setActiveRecipe={setActiveRecipe}
            />
        );
    }
    return (
        <div className={"RecipePreview RecipePreview-" + themeType} onClick={openRecipe}>
        <h2>{preview.name}</h2>
        <p>{preview.description}</p>
        </div>
    );
}

export default RecipePreview;
