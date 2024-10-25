import { Dispatch, ReactNode } from "react";
import { faX } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { ThemeType } from "../../util/ThemeType";

import "../../styles/viewer/ClearActiveRecipeButton.css";

function ClearActiveRecipeButton({
    themeType,
    setActiveRecipe
}: {
    themeType: ThemeType;
    setActiveRecipe: Dispatch<ReactNode>;
}) {
    function clearActiveRecipe() {
        setActiveRecipe(<div></div>);
    }
    return (
        <div className={"ClearActiveRecipeButton ClearActiveRecipeButton-" + themeType} onClick={clearActiveRecipe}>
        <div>
        <FontAwesomeIcon icon={faX} />
        </div>
        </div>
    )
}

export default ClearActiveRecipeButton;