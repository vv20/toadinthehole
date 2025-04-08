import { faX } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { useAppDispatch, useAppSelector } from "../../redux/hooks";
import { clearImage } from "../../redux/imageSlice";
import ThemeType from "../../util/ThemeType";

import "../../styles/editor/ClearImageButton.css";

function ClearImageButton() {
    const dispatch = useAppDispatch();
    const themeType: ThemeType = useAppSelector((state) => state.theme).theme;

    function clearImageFile() {
        dispatch(clearImage());
    }

    return (
        <div className={"ClearImageButton ClearImageButton-" + themeType} onClick={clearImageFile}>
            <FontAwesomeIcon icon={faX} />
        </div>
    )
}

export default ClearImageButton;