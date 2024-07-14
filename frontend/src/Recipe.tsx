import { APIRecipePrevew } from "./APIModel";
import { ThemeType } from "./ThemeType";
import "./Recipe.css";
import "./RecipeFormRow.css";
import "./RecipeTitle.css";
import ClearActiveRecipeButton from "./ClearActiveRecipeButton";
import { Dispatch, ReactNode } from "react";

function Recipe({
  themeType,
  preview,
  setActiveRecipe,
}: {
  themeType: ThemeType;
  preview: APIRecipePrevew;
  setActiveRecipe: Dispatch<ReactNode>;
}) {
  return (
      <div className={"Recipe Recipe-" + themeType}>
        <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
          <h1 className={"RecipeTitle RecipeTitle-" + themeType}>
            {preview.name}
          </h1>
          <ClearActiveRecipeButton themeType={themeType} setActiveRecipe={setActiveRecipe} />
        </div>
        <div style={{display: 'flex'}}>
          <div className={"RecipeEditorLeft RecipeEditorLeft-" + themeType}>
            <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
              <img src={"/image/" + preview.imageId} />
            </div>
          </div>
        </div>
      </div>
  );
}

export default Recipe;