from locust import HttpUser, task, between
from locust.exception import StopUser


class GudliftUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def user_journey(self):
        # 1. Connexion + récupération de la liste des compétitions
        with self.client.post(
            "/showSummary",
            data={"email": "john@simplylift.co"},
            name="/showSummary - competitions",
            catch_response=True,
        ) as response:
            if response.elapsed.total_seconds() >= 5:
                response.failure(
                    "Competition list took more than 5 seconds"
                )

        # 2. Achat d'une place et mise à jour des points
        with self.client.post(
            "/purchasePlaces",
            data={
                "competition": "Fall Classic",
                "club": "Simply Lift",
                "places": "1",
            },
            name="/purchasePlaces - points update",
            catch_response=True,
        ) as response:
            if "Great-booking complete!" not in response.text:
                response.failure(
                    "Booking was not completed"
                )
            elif response.elapsed.total_seconds() >= 2:
                response.failure(
                    "Points update took more than 2 seconds"
                )

        # 3. Tableau public des points
        self.client.get(
            "/points",
            name="/points",
        )

        # Chaque utilisateur exécute le scénario une seule fois.
        raise StopUser()
