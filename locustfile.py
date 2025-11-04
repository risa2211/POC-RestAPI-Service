from locust import HttpUser, task, between
import json

TEST_USER = "" # need to give the mail used for API
TEST_PASS = "" # need to give the pwd used for API

class ApiUser(HttpUser):
    wait_time = between(1, 2.5) 

    host = "http://127.0.0.1:8000"

    def on_start(self):
        login_response = self.client.post("/login", data={"username": TEST_USER, "password": TEST_PASS})
        
        if login_response.status_code == 200:
            token = login_response.json().get("access_token")
            self.client.headers = {"Authorization": f"Bearer {token}"}
            print(f"User {TEST_USER} successfully logged in and token set.")
        else:
            print(f"Login failed for {TEST_USER}. Status: {login_response.status_code}")
            self.environment.runner.quit()

    @task(3) 
    def get_user_profile(self):
        self.client.get("/profile", name="/profile [JWT Auth]")

    @task(1) 
    def get_sports_list(self):
        self.client.get("/sports")