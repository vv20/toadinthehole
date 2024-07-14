import { Dispatch, ReactNode } from "react";
import { APIRecipePrevew } from "./APIModel";
import "./RecipePreview.css";
import { ThemeType } from "./ThemeType";
import Recipe from "./Recipe";

function RecipePreview({
  themeType,
  preview,
  setActiveRecipe
}: {
  themeType: ThemeType;
  preview: APIRecipePrevew;
  setActiveRecipe: Dispatch<ReactNode>;
}) {
  function openRecipe() {
    setActiveRecipe(
      <Recipe
        themeType={themeType}
        preview={preview}
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
