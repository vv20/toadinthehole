import { ReactNode, useEffect, useState } from "react";

import "./RecipeList.css";
import RecipePreview from "./RecipePreview";
import { ThemeType } from "./ThemeType";
import { APIMethod, callAPI } from "./APIService";
import { APIRecipePrevew, DocumentType } from "./APIModel";

function RecipeList({
  themeType,
  activeRecipe,
}: {
  themeType: ThemeType;
  activeRecipe: ReactNode;
}) {
  const [recipes, setRecipes] = useState<Array<ReactNode>>([]);

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        const recipeJson: DocumentType = await callAPI({ 'path': '/collection', 'apiMethod': APIMethod.GET });
        const responseJson: APIRecipePrevew[] = Array.of(recipeJson) as APIRecipePrevew[];

        if (responseJson.length === 0) {
          return;
        }

        const recipePreviews: ReactNode[] = [];
        for (var i = 0; i < responseJson.length; i++) {
          recipePreviews.push(
            <RecipePreview themeType={themeType} preview={responseJson[i]} />
          );
        }
        setRecipes(recipePreviews);
      } catch (e) {
        console.log("Error while fetching recipes:", e);
      }
    };
    fetchRecipes();
  }, [themeType]);

  return (
    <div className={"RecipeList RecipeList-" + themeType}>
      <h1 className={"PageTitle PageTitle-" + themeType}>Recipes:</h1>
      {activeRecipe}
      {recipes}
    </div>
  );
}

export default RecipeList;
