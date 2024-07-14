import { Dispatch, ReactNode, useEffect, useState } from "react";

import "./RecipeList.css";
import RecipePreview from "./RecipePreview";
import { ThemeType } from "./ThemeType";
import { APIMethod, callAPI } from "./APIService";
import { APIRecipePrevew, DocumentType } from "./APIModel";

function RecipeList({
  themeType,
  activeRecipe,
  setActiveRecipe,
  setExistingTags,
}: {
  themeType: ThemeType;
  activeRecipe: ReactNode;
  setActiveRecipe: Dispatch<ReactNode>;
  setExistingTags: Dispatch<string[]>;
}) {
  const [recipes, setRecipes] = useState<Array<ReactNode>>([]);

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        const recipeJson: DocumentType = await callAPI({
          'path': '/collection',
          'apiMethod': APIMethod.GET,
          parseResponseJson: true,
        }) as {[key: string]: DocumentType};
        const recipePreviews: APIRecipePrevew[] = recipeJson.recipes as APIRecipePrevew[];
        const recipePreviewNodes: ReactNode[] = [];

        for (var i = 0; i < recipePreviews.length; i++) {
          recipePreviewNodes.push(
            <RecipePreview themeType={themeType} preview={recipePreviews[i]} setActiveRecipe={setActiveRecipe}/>
          );
        }
        setRecipes(recipePreviewNodes);
        setExistingTags(recipeJson.tags as string[]);
      } catch (e) {
        console.log("Error while fetching recipes:", e);
      }
    };
    fetchRecipes();
  }, [themeType, setActiveRecipe, setExistingTags]);

  return (
    <div className={"RecipeList RecipeList-" + themeType}>
      <h1 className={"PageTitle PageTitle-" + themeType}>Recipes:</h1>
        {activeRecipe}
      {recipes}
    </div>
  );
}

export default RecipeList;
