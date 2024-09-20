import { ChangeEvent, Dispatch, SetStateAction } from "react";
import "./ImageUpload.css";
import { ThemeType } from "./ThemeType";
import { APICallResponse, APIMethod, callAPI } from "./APIService";
import { APINewImageInfo, APIRecipePrevew } from "./APIModel";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCamera } from "@fortawesome/free-solid-svg-icons";

function ImageUpload({
  themeType,
  imageId,
  setFormData,
}: {
  themeType: ThemeType,
  imageId?: string,
  setFormData: Dispatch<SetStateAction<APIRecipePrevew>>,
}) {
  async function uploadImage(event: ChangeEvent<HTMLInputElement>) {
    if (event.target.files && event.target.files[0]) {
      // get a presigned URL
      const newImageResponse: APICallResponse = await callAPI({
        path: '/image',
        apiMethod: APIMethod.GET,
        parseResponseJson: true,
      });
      if (!newImageResponse.success) {
        // TODO: alert the user
        return;
      }
      const newImageInfo = newImageResponse.payload as APINewImageInfo;
      if (!newImageInfo.presignedUrl || !newImageInfo.imageId) {
        console.log("Missing required information on the API response!")
        return;
      }

      // upload the image to the presigned URL
      const formData = new FormData()
      formData.append('fileupload', event.target.files[0])
      fetch(newImageInfo.presignedUrl, {
        'method': 'PUT',
        'headers': {
          'Content-Type': 'image/jpeg',
        },
        'body': event.target.files[0],
      }).then(() => {
        // save the image ID to render the uploaded image
        const imageId: string = newImageInfo.imageId ? newImageInfo.imageId : '';
        setFormData((prevFormData) => ({ ...prevFormData, 'imageId': imageId }));
      });
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
      <img src={"images/" + imageId} alt="" />
    )
  }
}

export default ImageUpload;