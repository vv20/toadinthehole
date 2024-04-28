type DocumentType = null | boolean | number | string | DocumentType[] | {
    [prop: string]: DocumentType;
};

interface APIRecipePrevew {
  title?: string;
  imageId?: string;
  description?: string;
  tags?: [string];
}

interface APINewImageInfo {
  imageId?: string;
  presignedUrl?: string;
}

export type { APINewImageInfo, APIRecipePrevew, DocumentType };