import httpx

from filmweb_cli.exceptions.exceptions import ContentNotFoundError, InvalidContentError


class BaseService:
    @staticmethod
    def _validate_response(
        response: httpx.Response,
        resource_id: int,
        *,
        allow_missing: bool = False,
    ) -> bool:
        if response.status_code == httpx.codes.OK:
            return True

        if response.status_code == httpx.codes.NO_CONTENT:
            if allow_missing:
                return False

            msg = f"Content not found for id: {resource_id}"
            raise ContentNotFoundError(msg)

        if response.status_code == httpx.codes.BAD_REQUEST:
            try:
                data = response.json()
                error_msg = data.get("message", "Type mismatch or malformed request")
            except (ValueError, AttributeError):
                error_msg = "Invalid request (could not parse error body)"

            msg = f"Filmweb API error ({resource_id}): {error_msg}"
            raise InvalidContentError(msg)

        response.raise_for_status()
        return True
