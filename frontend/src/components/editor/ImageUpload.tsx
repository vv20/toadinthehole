import { ReactNode } from "react";

import { ChangeEvent } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCamera } from "@fortawesome/free-solid-svg-icons";

import ClearImageButton from "./ClearImageButton";
import { uploadImage } from "../../redux/imageSlice";
import { useAppDispatch, useAppSelector } from '../../redux/hooks';
import ThemeType from "../../util/ThemeType";
import { getImageUrl } from '../../util/UrlUtil';

import "../../styles/editor/ImageUpload.css";

function ImageUpload({
    editable,
}: {
    editable: boolean,
}) {
    const dispatch = useAppDispatch();
    const themeType: ThemeType = useAppSelector((state) => state.theme).theme;
    const imageId: string|undefined = useAppSelector((state) => state.image).imageId;
    const imageFile: File|undefined = useAppSelector((state) => state.image).imageFile;
    
    async function uploadImageFile(event: ChangeEvent<HTMLInputElement>) {
        if (event?.target?.files) {
            dispatch(uploadImage({ file: event.target.files[0] }));
        }
    }
    
    var clearImageButton: ReactNode = <div></div>;
    var innerNode: ReactNode = <div></div>;
    if (editable && imageId !== undefined) {
        clearImageButton = <ClearImageButton />;
    }
    if (editable && imageFile !== undefined) {
        innerNode = <img src={URL.createObjectURL(imageFile)} alt=""/>;
    } else if (editable && imageId === undefined) {
            innerNode = (
                <div className={"ImageUpload ImageUpload-" + themeType}>
                    <div>
                        <FontAwesomeIcon icon={faCamera} />
                    </div>
                    <input type="file" onChange={uploadImageFile} />
                </div>
            );
    } else {
        innerNode = <img src={getImageUrl({ imageId: imageId })} alt=""/>;
    }
    return (
        <div className={"ImageUploadOuter ImageUploadOuter-" + themeType}>
            {clearImageButton}
            {innerNode}
        </div>
    )
}

export default ImageUpload;