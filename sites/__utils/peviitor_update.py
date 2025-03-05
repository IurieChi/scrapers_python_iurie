#
#
#
#  Send data to Peviitor API!
#  ... OOP version
#
#
import requests
import json


class UpdateAPI:
    """
    - Method for update logo,
    - Method to get token,
    - Method for update data.
    """

    def __init__(self):
        self.logo_url = "https://api.peviitor.ro/v3/logo/add/"
        self.logo_header = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }

        self.EMAIL = "chigaiiura@yahoo.com"
        self.DOMAIN = "https://api.peviitor.ro/v5/"  # "http://127.0.0.1:8000/"  #
        self.header = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }

        self.TOKEN_ROUTE = "get_token/"  # "get_token"  #
        self.ADD_JOBS_ROUTE = "add/"  # "jobs/add/"  #

    def update_logo(self, id_company: str, logo_link: str):
        """update logo on peviitor.ro"""

        data = json.dumps([{"id": id_company, "logo": logo_link}])
        response = requests.post(self.logo_url, headers=self.logo_header, data=data)

        print(f"Logo update {response}")

    def get_token(self):
        """
        Returnează token-ul necesar pentru a face request-uri către API.
        :return: token-ul necesar pentru a face request-uri către API
        """
        url = f"{self.DOMAIN}{self.TOKEN_ROUTE}"

        response = requests.post(url, json={"email": self.EMAIL}, headers=self.header)
        if response.status_code != 200:
            raise Exception("Get token conection code", response.status_code)
        else:
            return response.json()["access"]

    def publish(self, data):
        """This method publish scraped data using API to Validator with post method
        using token to make API request.
        Args:
            data (_type_): Json
        """

        route = self.ADD_JOBS_ROUTE
        url = f"{self.DOMAIN}{route}"
        token = self.get_token()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        }

        responce = requests.post(url, headers=headers, json=data)

        print(json.dumps(data, indent=4))

        if responce.status_code != 200:
            print(f"something wrong {responce.status_code}")


# print(UpdateAPI().get_token())
