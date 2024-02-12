import APIModel from "./APIModel";

import "./RecipePreview.css";

function RecipePreview({ preview }: { preview: APIModel.APIRecipePrevew }) {
  return (
    <div className="RecipePrevew">
      <h2>{preview.title}</h2>
    </div>
  );
}

export default RecipePreview;
