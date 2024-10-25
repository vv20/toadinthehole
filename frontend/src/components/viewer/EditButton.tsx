import { Dispatch, ReactNode } from "react";

import RecipeEditor from "../editor/RecipeEditor";
import { APIRecipePrevew } from "../../api/APIModel";
import { ThemeType } from "../../util/ThemeType";

import "../../styles/general/Button.css";
import "../../styles/viewer/EditButton.css";

function EditButton({
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
    function editCurrentRecipe() {
        setActiveRecipe(
            <RecipeEditor
            themeType={themeType}
            recipe={preview}
            existingTags={existingTags}
            setActiveRecipe={setActiveRecipe}
            />
        );
    }
    return (
        <button
        className={"Button Button-" + themeType + " EditButton EditButton-" + themeType}
        onClick={editCurrentRecipe}>
        Edit
        </button>
    )
}

export default EditButton;