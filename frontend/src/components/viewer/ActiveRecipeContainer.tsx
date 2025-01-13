import { APIRecipePreview } from "../../api/APIModel";
import { useAppSelector } from "../../redux/hooks";
import ActiveRecipeType from "../../util/ActiveRecipeType";
import RecipeEditor from "../editor/RecipeEditor";
import Recipe from "./Recipe";

function ActiveRecipeContainer() {
    const activeRecipeType: ActiveRecipeType = useAppSelector((state) => state.activeRecipe).activeRecipeType;
    const activeRecipeSlug: string | undefined = useAppSelector((state) => state.activeRecipe).activeRecipeSlug;
    const recipes: { [prop: string ]: APIRecipePreview } = useAppSelector((state) => state.recipes).recipes
    
    switch (activeRecipeType) {
        case ActiveRecipeType.None:
            return <div></div>;
        case ActiveRecipeType.View:
            return <Recipe preview={recipes[activeRecipeSlug ? activeRecipeSlug : ""]} />
        case ActiveRecipeType.Edit:
            return <RecipeEditor recipe={recipes[activeRecipeSlug ? activeRecipeSlug : ""]} />
    }
}

export default ActiveRecipeContainer;