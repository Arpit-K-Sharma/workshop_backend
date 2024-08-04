from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Any, Union, List

def serialize_data(data: Any) -> Any:
    if isinstance(data, BaseModel):
        # If data is a single DTO, convert it to a dictionary
        return data.dict()
    elif isinstance(data, list):
        # If data is a list, convert each DTO in the list to a dictionary
        return [item.dict() if isinstance(item, BaseModel) else item for item in data]
    else:
        # If data is not a DTO or a list of DTOs, return it as is
        return data

def get_response(
    status: str,
    message: Optional[str] = None,
    data: Optional[Union[dict, BaseModel, List[BaseModel]]] = None,
    status_code: int = 200
):
    response = {
        "status": status,
        "status_code": status_code
    }

    if message:
        response["message"] = message

    if data:
        # Serialize the data to ensure DTOs are converted to dictionaries
        response["data"] = serialize_data(data)

    return JSONResponse(content=response, status_code=status_code)
