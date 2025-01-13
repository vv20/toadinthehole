import { APIRecipePreview } from "../../api/APIModel";
import { viewRecipe } from "../../redux/activeRecipeSlice";
import { useAppDispatch, useAppSelector } from "../../redux/hooks";
import ThemeType from "../../util/ThemeType";

import "../../styles/viewer/RecipePreview.css";

function RecipePreview({ preview }: { preview: APIRecipePreview }) {
    const dispatch = useAppDispatch();
    const themeType: ThemeType = useAppSelector((state) => state.theme).theme;

    function openRecipe() {
        dispatch(viewRecipe({ recipeSlug: preview.slug }));
    }

    return (
        <div className={"RecipePreview RecipePreview-" + themeType} onClick={openRecipe}>
        <h2>{preview.name}</h2>
        <p>{preview.description}</p>
        </div>
    );
}

export default RecipePreview;
