import { ChangeEvent, Dispatch, SetStateAction } from "react";
import "./ImageUpload.css";
import { ThemeType } from "./ThemeType";
import { APIMethod, callAPI } from "./APIService";
import { APINewImageInfo } from "./APIModel";

function ImageUpload({
  themeType,
  imageId,
  setFormData,
}: {
  themeType: ThemeType,
  imageId: string | null,
  setFormData: Dispatch<SetStateAction<{ title: string; imageId: string | null; description: string; }>>,
}) {
  async function uploadImage(event: ChangeEvent<HTMLInputElement>) {
    if (event.target.files && event.target.files[0]) {
      // get a presigned URL
      const newImageInfo: APINewImageInfo = await callAPI({'path': '/image', 'apiMethod': APIMethod.GET}) as APINewImageInfo;
      console.log(newImageInfo);
      if (!newImageInfo.presignedUrl || !newImageInfo.imageId) {
        console.log("Missing required information on the API response!")
        return;
      }

      // upload the image to the presigned URL
      fetch(newImageInfo.presignedUrl, {
        'method': 'PUT',
        'mode': 'cors',
        'body': event.target.files[0],
      });

      // save the image ID to render the uploaded image
      const imageId: string = newImageInfo.imageId;
      setFormData((prevFormData) => ({ ...prevFormData, 'imageId': imageId }));
    }
  }

  if (imageId == null) {
    return (
      <div className={"ImageUpload ImageUpload-" + themeType}>
        <div>
          <span>
            <i className="fa fa-camera" />
          </span>
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