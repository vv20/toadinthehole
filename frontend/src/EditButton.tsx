import { Dispatch, ReactNode } from "react";
import "./Button.css";
import "./EditButton.css";
import { ThemeType } from "./ThemeType";
import { APIRecipePrevew } from "./APIModel";
import RecipeEditor from "./RecipeEditor";

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
        console.log("boop");
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