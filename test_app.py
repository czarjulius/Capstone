
import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor

EXECUTIVE_PRODUCER = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJqQkdRVGMwTkRBd016WkNOek5DUVRjeU5VUXdOVGRHTVVKR01UQXhNekU0TkVORU4wVkJOUSJ9.eyJpc3MiOiJodHRwczovL2p1bGl1cy1jemFyLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGY4Y2ZiY2MyMjQ3ZjBlYTIwZmVlY2UiLCJhdWQiOiJtb3ZpZSIsImlhdCI6MTU3Njk1NjQ5MSwiZXhwIjoxNTc2OTYzNjkxLCJhenAiOiI0S3FjeHFWbklXd0ZFRkRlNjBwdHNEVUVBZDVaUDZORyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.pyfFZi3p-1cArJtWssk9JCVf1fJaWsYmRZZCknbkszExJTSWNQXk4py5gIsgpxAj5bWnHmIj04Lv8wiSCTNlXe6mNteQg1ehZsxmwsdpgamJ634NZtI8xRGlPC3sJ_cmAPdNxYWGYx2NFxXd2SyoTuEVsaT8O2LfODt0zeae00p2jyHcbGZIirUFIKnq_f5exORD_czw5RhT-MssNzYSVJGG3s9sgq16IHBhtmjVOS8ImKWCc23kh48mfla-w3E1gXugjax2puoVxRS_GcXaq_NywgPkd2bK2b3xPXuqIR4ywuTDMi9iwKKmHOtNka9KsO1sTVeGIFVv2wKUQv96sQ'

CASTING_DIRECTOR = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJqQkdRVGMwTkRBd016WkNOek5DUVRjeU5VUXdOVGRHTVVKR01UQXhNekU0TkVORU4wVkJOUSJ9.eyJpc3MiOiJodHRwczovL2p1bGl1cy1jemFyLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGZjOWYyNjk0ZDdhNTE1MzY1ZjdhMzgiLCJhdWQiOiJtb3ZpZSIsImlhdCI6MTU3Njk1NjY2NCwiZXhwIjoxNTc2OTYzODY0LCJhenAiOiI0S3FjeHFWbklXd0ZFRkRlNjBwdHNEVUVBZDVaUDZORyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.AAoJ1Y3-GBq8Bc40MK9uQ_prIS5HEXwP4LyCyelHbGr-eIkm9iCnF3wqqjkBll54A6JhZ3W0lRrP8DSxLZXbBBOswHrrip8Kon4-_9L1yxn_Sz3v5hZgZ0lQ6YOoYTyQMC6afVoEOkghs3eeEd1ZKzZPv03qjSHbPrSb5VltjspHwvh9N53XqRYEs0QYAws-bioTDGyzgvDGo6ny86Y_-YMwqcU9Uf4MpdLOYpan_Ja-4quXWKi8g1B92BENhcGAMmSiYiOqETMeDL8Oed1tpn9hij5zjNxIsYh4j4jCzD5AFxD3n09rIEh1E6BNtY51E0FQm3L8AbVGQ12ekNEBtw'

CASTING_ASSISTANT = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJqQkdRVGMwTkRBd016WkNOek5DUVRjeU5VUXdOVGRHTVVKR01UQXhNekU0TkVORU4wVkJOUSJ9.eyJpc3MiOiJodHRwczovL2p1bGl1cy1jemFyLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGZjOWZmNDk0ZDdhNTE1MzY1ZjdhNDEiLCJhdWQiOiJtb3ZpZSIsImlhdCI6MTU3Njk2NDQyMSwiZXhwIjoxNTc2OTcxNjIxLCJhenAiOiI0S3FjeHFWbklXd0ZFRkRlNjBwdHNEVUVBZDVaUDZORyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.jIv3RWi6DmbXjPo5ec6ZhXDjQItYW1pwa-bowFPWpLW5cm8iejS8tp9gCN93INCs-UqqR7lM1gMhT22JNGAHcl9CHdldtiuG0q0N3yt1x4WsazxIw_WFEdwE3AgeYzkkXRmxDyHHo70DF2OCoHY5TyVYgEtfGXUiRxbdeDSQ0Uh5YzYR_AYQaqjwoHgivaU00dCg-ALhqTb3uZx6okQo1DRVZ3Fl9NpaOCJVIrgAKGu5Mm4lBq_nyGoBl7PiHJgDgWt3Wm1xZExqn09bNTXMJ0DrLxY1Sab97ltJay4QNw6O-bp-ijbMJhfGpyuvwXYURDNGSMPVALbUyfCxVCKHDg'


class MHTestCase(unittest.TestCase):
    """This class represents the movies-hub test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['TEST_DB_URL']

        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after reach test"""
        pass

#####################    MOVIE TEST STARTS #################################################

    #  GET /movies
    def test_get_movies(self):
        response = self.client().get(
            '/movies',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # GET /movies/id
    def test_get_movie_by_id(self):
        response = self.client().get(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Black Panther')

    def test_get_movie_byId_404(self):
        response = self.client().get(
            '/movies/10000',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Resource not found')

#####################    MOVIE TEST ENDS #################################################

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()