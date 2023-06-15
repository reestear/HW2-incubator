from typing import List

from fastapi import Depends, Response, UploadFile

from ..service import Service, get_service
from . import router


@router.post("/{shanyrak_id:str}/media")
def add_shanyrak_media(
    shanryrak_id: str,
    file: UploadFile,
    svc: Service = Depends(get_service),
):
    """
    file.filename: str - Название файла
    file.file: BytesIO - Содержимое файла
    """
    url = svc.s3_service.upload_media(file.file, file.filename)
    svc.repository.put_shanyrak_media_by_id(shanryrak_id, url)

    return Response(status_code=200)


@router.post("/{shanyrak_id:str}/medias")
def add_shanyrak_medias(
    shanryrak_id: str,
    files: List[UploadFile],
    svc: Service = Depends(get_service),
):
    """
    file.filename: str - Название файла
    file.file: BytesIO - Содержимое файла
    """

    for file in files:
        url = svc.s3_service.upload_media(file.file, file.filename)
        svc.repository.put_shanyrak_media_by_id(shanryrak_id, url)

    return Response(status_code=200)
