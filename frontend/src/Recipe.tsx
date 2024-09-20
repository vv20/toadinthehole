import { APIRecipePrevew } from "./APIModel";
import { ThemeType } from "./ThemeType";
import "./ActiveTag.css";
import "./Recipe.css";
import "./RecipeFormRow.css";
import "./RecipeTitle.css";
import ClearActiveRecipeButton from "./ClearActiveRecipeButton";
import { Dispatch, ReactNode } from "react";
import EditButton from "./EditButton";

function Recipe({
  themeType,
  preview,
  existingTags,
  setActiveRecipe,
}: {
  themeType: ThemeType;
  preview: APIRecipePrevew;
  existingTags: string[];
  setActiveRecipe: Dispatch<ReactNode>;
}) {
  const tagElements: Array<ReactNode> = [];
  if (preview.tags !== undefined) {
    for (var i = 0; i < preview.tags.length; i++) {
      tagElements.push(
        <div className={"ActiveTag ActiveTag-" + themeType}>
            #{preview.tags[i]}
        </div>
      );
    }
  }
  return (
      <div className={"Recipe Recipe-" + themeType}>
        <EditButton
          themeType={themeType}
          preview={preview}
          existingTags={existingTags}
          setActiveRecipe={setActiveRecipe}
        />
        <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
          <h1 className={"RecipeTitle RecipeTitle-" + themeType}>
            {preview.name}
          </h1>
          <ClearActiveRecipeButton themeType={themeType} setActiveRecipe={setActiveRecipe} />
        </div>
        <div style={{display: 'flex'}}>
          <div className={"RecipeEditorLeft RecipeEditorLeft-" + themeType}>
            <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
              <img src={"/image/" + preview.image_id} alt="no pic :("/>
            </div>
            <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
              <p>{preview.description}</p>
            </div>
          </div>
          <div className={"RecipeEditorRight RecipeEditorRight-"+ themeType}>
            <div className={"RecipeFormRow RecipeFormRow-" + themeType}>
              {tagElements}
            </div>
          </div>
        </div>
      </div>
  );
}

export default Recipe;