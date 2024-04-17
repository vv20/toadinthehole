import { get } from "aws-amplify/api";
import { fetchAuthSession } from "aws-amplify/auth";
import { ReactNode, useEffect, useState } from "react";

import "./RecipeList.css";
import RecipePreview from "./RecipePreview";
import { ThemeType } from "./ThemeType";

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
        const { idToken } = (await fetchAuthSession()).tokens ?? {};
        const options = {
          headers: {
            Authorization: `${idToken?.toString()}`,
          },
        };
        const restOperation = get({
          apiName: "ToadInTheHoleAPI",
          path: "/collection",
          options: options,
        });
        const { body } = await restOperation.response;
        const responseJson: any[] = Array.of(await body.json());

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
