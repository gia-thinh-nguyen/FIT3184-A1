from locust import HttpUser, task, between
import uuid
import random

class ParkingUser(HttpUser):
    wait_time = between(0.5, 2)

    @task
    def find_carparks(self):
        user_uuid = str(uuid.uuid4())
        n = random.randint(1, 5)
        self.client.get(f"/api/find-carparks?uuid={user_uuid}&n={n}")