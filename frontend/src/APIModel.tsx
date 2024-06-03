type DocumentType = null | boolean | number | string | DocumentType[] | {
    [prop: string]: DocumentType;
};

type APIRecipePrevew = {
  title?: string;
  imageId?: string;
  description?: string;
  tags?: string[];
}

type APINewImageInfo = {
  imageId?: string;
  presignedUrl?: string;
}

export type { APINewImageInfo, APIRecipePrevew, DocumentType };