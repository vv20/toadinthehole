import { faX } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { clearActiveRecipe } from "../../redux/activeRecipeSlice";
import { useAppDispatch, useAppSelector } from "../../redux/hooks";
import ThemeType from "../../util/ThemeType";

import "../../styles/viewer/ClearActiveRecipeButton.css";

function ClearActiveRecipeButton() {
    const dispatch = useAppDispatch();
    const themeType: ThemeType = useAppSelector((state) => state.theme).theme;

    function clearRecipe() {
        dispatch(clearActiveRecipe());
    }

    return (
        <div className={"ClearActiveRecipeButton ClearActiveRecipeButton-" + themeType} onClick={clearRecipe}>
        <div>
        <FontAwesomeIcon icon={faX} />
        </div>
        </div>
    )
}

export default ClearActiveRecipeButton;