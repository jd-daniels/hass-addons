import requests


class SupervisorAPIError(Exception):
    pass


class _BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


class SupervisorAPI:
    BASE_URL = "http://supervisor"

    def __init__(self, token: str):
        """Interact with the Home Assistant Supervisor API

        Args:
            token (str): Supervisor bearer token
        """
        self.auth = _BearerAuth(token)

    def _get(self, path: str) -> requests.Response:
        url = f"{SupervisorAPI.BASE_URL}{path}"
        try:
            response = requests.get(url, auth=self.auth)
        except requests.exceptions.ConnectionError as err:
            raise SupervisorAPIError(
                f"Error connecting to Home Assistant Supervisor API: {err}")
        except requests.exceptions.Timeout as err:
            raise SupervisorAPIError(
                "Timeout connecting to Home Assistant Supervisor API")
        else:
            json = None
            if response.ok:
                try:
                    json = response.json()
                except ValueError as err:
                    raise SupervisorAPIError(
                        "Error decoding response from Home Assistant Supervisor API")
            return json

    def _post(self, path: str) -> requests.Response:
        url = f"{SupervisorAPI.BASE_URL}{path}"
        try:
            response = requests.post(url, auth=self.auth)
        except requests.exceptions.ConnectionError as err:
            raise SupervisorAPIError(
                f"Error connecting to Home Assistant Supervisor API: {err}")
        except requests.exceptions.Timeout as err:
            raise SupervisorAPIError(
                "Timeout connecting to Home Assistant Supervisor API")
        else:
            json = None
            if response.ok:
                try:
                    json = response.json()
                except ValueError as err:
                    raise SupervisorAPIError(
                        "Error decoding response from Home Assistant Supervisor API")
            return json

    def get_backups(self):
        """Get list of all backups

        Returns:
            List: List of backups
        """
        response = self._get("/backups")
        return response.get("data", {}).get("backups", [])

    def get_backup(self, slug: str):
        """Get details of a single backup

        Args:
            slug (str): Slug of backup to retrieve

        Returns:
            dict: Dictionary containing backup details
        """
        response = self._get(f"/backups/{slug}/info")
        return response.get("data")

    def remove_backup(self, slug: str) -> bool:
        """Delete a backup

        Args:
            slug (str): Slug of backup to delete

        Returns:
            bool: True if successful
        """
        response = self._post(f"/backups/{slug}/remove")
        return True if response.get("result") == "ok" else False
