import { useEffect, useState } from "react";
import { get } from "aws-amplify/api";
import { ReactNode } from "react";

import RecipePreview from "./RecipePreview";

import "./RecipeList.css";

function RecipeList() {
  const [recipes, setRecipes] = useState<Array<ReactNode>>([]);

  useEffect(() => {
    const fetchRecipes = async () => {
      try {
        const restOperation = get({
          apiName: "",
          path: "",
        });
        const { body } = await restOperation.response;
        const responseJson: any[] = Array.of(await body.json());

        const recipePreviews: ReactNode[] = [];
        for (var i = 0; i < responseJson.length; i++) {
          recipePreviews.push(<RecipePreview preview={responseJson[i]} />);
        }
        setRecipes(recipePreviews);
      } catch (e) {
        console.log("Error while fetching recipes:", e);
      }
    };
    fetchRecipes();
  }, []);

  return (
    <div className="RecipeList">
      <h1>Recipes:</h1>
      {recipes}
    </div>
  );
}

export default RecipeList;
