import { Dispatch, ReactNode } from "react";
import { ThemeType } from "./ThemeType";
import "./ClearActiveRecipeButton.css";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faX } from "@fortawesome/free-solid-svg-icons";

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