import { uploadData } from 'aws-amplify/storage';
import { ChangeEvent, Dispatch, SetStateAction } from "react";
import { v4 as uuidv4 } from 'uuid';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCamera } from "@fortawesome/free-solid-svg-icons";

import { APIRecipePreview } from "../../api/APIModel";
import { useAppSelector } from '../../redux/hooks';
import ThemeType from "../../util/ThemeType";

import "../../styles/editor/ImageUpload.css";

function ImageUpload({
    imageId,
    setFormData,
}: {
    imageId?: string,
    setFormData: Dispatch<SetStateAction<APIRecipePreview>>,
}) {
    const themeType: ThemeType = useAppSelector((state) => state.theme).theme;

    async function uploadImage(event: ChangeEvent<HTMLInputElement>) {
        if (event?.target?.files) {
            const imageId = uuidv4();
            try {
                const result = await uploadData({
                    key: imageId + '.jpg',
                    data: event.target.files[0],
                }).result
                console.log("Image uploaded: ", result);
                setFormData((prevFormData) => ({ ...prevFormData, image_id: imageId }));
            }
            catch (error) {
                console.log("Error: ", error);
            }
        }
    }
    
    if (imageId == null) {
        return (
            <div className={"ImageUpload ImageUpload-" + themeType}>
            <div>
            <FontAwesomeIcon icon={faCamera} />
            </div>
            <input type="file" onChange={uploadImage} />
            </div>
        )
    }
    else {
        return (
            <img src={"https://dev.toadinthehole.com/images/" + imageId} alt="" />
        )
    }
}

export default ImageUpload;