function getImageUrl({imageId}: {imageId: string}) {
    return "/public/" + imageId + ".jpg";
}

export { getImageUrl }