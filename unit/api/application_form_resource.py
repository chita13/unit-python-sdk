from unit.api.base_resource import BaseResource
from unit.models.application_form import *
from unit.models.codecs import DtoDecoder


class ApplicationFormResource(BaseResource):
    def __init__(self, api_url, token):
        super().__init__(api_url, token)
        self.resource = "application-forms"

    def create(self, request: CreateApplicationFormRequest) -> Union[UnitResponse[ApplicationFormDTO], UnitError]:
        payload = request.to_json_api()
        response = super().post(self.resource, payload)
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            return UnitResponse[ApplicationFormDTO](DtoDecoder.decode(data), None)
        else:
            return UnitError.from_json_api(response.json())

    def get(self, application_form_id: str, include: Optional[str] = "") -> Union[UnitResponse[ApplicationFormDTO], UnitError]:
        response = super().get(f"{self.resource}/{application_form_id}")
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[ApplicationFormDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())

    def list(self, offset: int = 0, limit: int = 100) -> Union[UnitResponse[list[ApplicationFormDTO]], UnitError]:
        response = super().get(self.resource, {"page[limit]": limit, "page[offset]": offset})
        if super().is_20x(response.status_code):
            data = response.json().get("data")
            included = response.json().get("included")
            return UnitResponse[ApplicationFormDTO](DtoDecoder.decode(data), DtoDecoder.decode(included))
        else:
            return UnitError.from_json_api(response.json())
