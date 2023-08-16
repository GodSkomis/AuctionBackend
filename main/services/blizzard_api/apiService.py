import datetime
import dateutil.parser
import requests


class ApiService:
    _access_token: str = None
    _auction_response: dict = None
    _time_of_update: datetime.datetime = None

    @property
    def time_of_update(self) -> datetime.datetime | None:
        return self._time_of_update

    @property
    def auction_response(self) -> dict | None:
        return self._auction_response

    @property
    def access_token(self) -> str | None:
        return self._access_token

    def refresh_access_token(self) -> str:
        url = "https://oauth.battle.net/token"
        user_id = "4af01c166cee45dfbba6c835285a154d"
        user_pswd = "6DAB2sZCKAkC4scZHDGw4rAtwxyk9mSf"
        data = {"grant_type": "client_credentials"}
        response = requests.post(url=url, auth=(user_id, user_pswd), data=data)

        j = response.json()
        api_token = j['access_token']

        self._access_token = api_token
        return api_token

    def get_access_token(self) -> str:
        if self._access_token:
            return self._access_token
        api_token = self.refresh_access_token()
        return api_token

    def get_auction_response(self) -> (datetime.datetime, dict):
        if self._auction_response:
            return self._auction_response

        access_token = self.get_access_token()
        url = f"https://eu.api.blizzard.com/data/wow/auctions/commodities?namespace=dynamic-eu&locale=en_US" \
              f"&access_token={access_token}"

        response = requests.get(url=url)
        if response.status_code >= 400:
            raise NotImplemented(f"STATUS: {response.status_code}\n")

        data = response.json()
        time_header = response.headers.get('Last-Modified')
        time_of_last_update = dateutil.parser.parse(time_header)

        self._auction_response = data
        self._time_of_update = time_of_last_update.replace(microsecond=0)
        return time_of_last_update, data
