from locust import HttpUser, task


class QuickstartUser(HttpUser):

    def on_start(self):
        response = self.client.post(
            "/accounts/api/v2/jwt/create/",
            data={"username": "reza", "password": "123456789ab"},
        ).json()
        self.client.headers = {
            "Authorization": f"Bearer {response.get('access', None)}"
        }

    @task
    def todo_list(self):
        self.client.get("/blog/api/v1/task/")

    @task
    def status_list(self):
        self.client.get("/blog/api/v1/category/")
