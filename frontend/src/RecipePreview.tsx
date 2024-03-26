import { APIRecipePrevew } from "./APIModel";
import "./RecipePreview.css";
import { ThemeType } from "./ThemeType";

function RecipePreview({
  themeType,
  preview,
}: {
  themeType: ThemeType;
  preview: APIRecipePrevew;
}) {
  return (
    <div className={"RecipePrevew RecipePrevew-" + themeType}>
      <h2>{preview.title}</h2>
    </div>
  );
}

export default RecipePreview;
