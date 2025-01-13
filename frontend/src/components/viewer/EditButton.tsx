import { APIRecipePreview } from "../../api/APIModel";
import { editRecipe } from "../../redux/activeRecipeSlice";
import { useAppDispatch, useAppSelector } from "../../redux/hooks";
import ThemeType from "../../util/ThemeType";

import "../../styles/general/Button.css";
import "../../styles/viewer/EditButton.css";

function EditButton({ preview }: { preview: APIRecipePreview }) {
    const dispatch = useAppDispatch();
    const themeType: ThemeType = useAppSelector((state) => state.theme).theme;

    function editCurrentRecipe() {
        dispatch(editRecipe({ recipeSlug: preview.slug }));
    }

    return (
        <button
        className={"Button Button-" + themeType + " EditButton EditButton-" + themeType}
        onClick={editCurrentRecipe}>
        Edit
        </button>
    )
}

export default EditButton;