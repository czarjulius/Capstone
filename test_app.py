
import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor

EXECUTIVE_PRODUCER = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJqQkdRVGMwTkRBd016WkNOek5DUVRjeU5VUXdOVGRHTVVKR01UQXhNekU0TkVORU4wVkJOUSJ9.eyJpc3MiOiJodHRwczovL2p1bGl1cy1jemFyLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGY4Y2ZiY2MyMjQ3ZjBlYTIwZmVlY2UiLCJhdWQiOiJtb3ZpZSIsImlhdCI6MTU3NzAyNzExNywiZXhwIjoxNTc3MDM0MzE3LCJhenAiOiI0S3FjeHFWbklXd0ZFRkRlNjBwdHNEVUVBZDVaUDZORyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.ytyDlhAc55Tf1R24-rViVB75xchNgmrpHr1lyTAV7cWFiqjcgXRS-iqvMM6BOMyC0Uo_57wNfPwJPavjPc160aRh7nKfUY1iMGIfqLQ-WvMAN0U99vcjHa6nSzoXlrfMpnP8rQHTM4aM4tJOM5WM756yh4ZKQq516RrRNP0FTSyTDcIrayrYes1eyQCMoDq8Y_kx924ABqtknSGPzDrQqqyunJIBTo2KHgsOGRw2_4t4GHYlNShkLwUe07OSwO4M49JwU5-3dYPJeh2hTjz6nyHQW8CT29lqHoFysQVAZJ364n1HxAO0X__dE7j0qcgFbVi7xbDRlUqaIqmeheth7Q'

CASTING_DIRECTOR = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJqQkdRVGMwTkRBd016WkNOek5DUVRjeU5VUXdOVGRHTVVKR01UQXhNekU0TkVORU4wVkJOUSJ9.eyJpc3MiOiJodHRwczovL2p1bGl1cy1jemFyLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGZjOWYyNjk0ZDdhNTE1MzY1ZjdhMzgiLCJhdWQiOiJtb3ZpZSIsImlhdCI6MTU3NzAyNjk3NCwiZXhwIjoxNTc3MDM0MTc0LCJhenAiOiI0S3FjeHFWbklXd0ZFRkRlNjBwdHNEVUVBZDVaUDZORyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.lhEP76HON-2o2zgcpja830uoFOYdyQbpEl3ZF6OuDYVn-ENM7WiGYfDaNHfOe32Tt49mKsJzBZsUOayoyMLkaIx94S-1lUCnr2YKSkkTK2L06LrXZI1df03DC_zP5mIrg2cMrnQB0RG455Yo3l9XdlnTt2HLU7I2TmQLLc_Y-vDS4nwrCd3FhtYQuzWvwIqLAka9rifZFv9XiVw374knDaX0ui3YtrBvF_ZyjJE-s65pxPQXcgLOpGzBPEm46-VknVX-G1i7qG1dbUW8Nj3UweOhwEQCsOwGCrUWQlTKt3n7xVAdbiqbbCxFs4rHo0rczFG81rfbI2nQEPNOUPusXg'

CASTING_ASSISTANT = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJqQkdRVGMwTkRBd016WkNOek5DUVRjeU5VUXdOVGRHTVVKR01UQXhNekU0TkVORU4wVkJOUSJ9.eyJpc3MiOiJodHRwczovL2p1bGl1cy1jemFyLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGZjOWZmNDk0ZDdhNTE1MzY1ZjdhNDEiLCJhdWQiOiJtb3ZpZSIsImlhdCI6MTU3NzAyNTQ3MywiZXhwIjoxNTc3MDMyNjczLCJhenAiOiI0S3FjeHFWbklXd0ZFRkRlNjBwdHNEVUVBZDVaUDZORyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.ncExksZzJtV-OescOXL5iskWE-bPC8Iejijvt_gldBIWl6Bjo14SOmY0ZayDm2T4FIziCyDhxetAfOOao0GUVP2mw3Eyr2Uxn6W2gwK_swLPSKZqAJJ5umBncDjc43vOT80c5WRfRnqRhds0iOS7lvUFd5h5USQMmXYggZQ7oQgLsNWPQNerEsXXaG3ytL2FRnDAuxKhRYOZ_dxBVf0ZpVCOU_4XwXHMJfyFzIR2ab7ao2OL_dWsgcFzMDXRR7HyilTbRjyqRjQpYcZw4NtEehrHy6RB1JmT_ku4At5eZPqRCiVof8KUKcwuQ0o1zcqsSyMab1hkABBADHeO2vJjDA'


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

    # def test_get_movie_byId_404(self):
    #     response = self.client().get(
    #         '/movies/10000',
    #         headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
    #     )
    #     data = json.loads(response.data)
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])
    #     self.assertEqual(data['message'], 'Resource not found')

    # POST /movies
    def test_post_movie(self):
        response = self.client().post(
            '/movies',
            json={'title': 'Jumanji', 'release_date': "1981-02-19"},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie created successfully')
        self.assertEqual(data['movie']['title'], 'Jumanji')

    def test_post_movie_400(self):
        response = self.client().post(
            '/movies',
            json={'title': '', 'release_date': ""},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    def test_post_movie_401(self):
        response = self.client().post(
            '/movies',
            json={'title': 'Wrong movie', 'release_date': "1984-01-23"},
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    # PATCH /movies
    def test_edit_movie(self):
        response = self.client().patch(
            '/movies/2',
            json={'title': 'The Hangover', 'release_date': "2018-10-12"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie updated')
        self.assertEqual(data['movie']['title'], 'The Hangover')


    def test_edit_movie_400(self):
        response = self.client().patch(
            '/movies/1',
            json={'title': '', 'release_date': ""},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')


    def test_edit_movie_404(self):
        response = self.client().patch(
            '/movies/50000',
            json={'title': 'Black Panther 2', 'release_date': "2019-11-12"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')


    # DELETE /movies/id
    def test_delete_movie(self):
        response = self.client().delete(
            '/movies/3',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie deleted')

    # def test_delete_movie_404(self):
    #     response = self.client().delete(
    #         '/movies/110000',
    #         headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
    #     )
    #     data = json.loads(response.data)
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(data['message'], 'Resource not found')

    def test_delete_movie_401(self):
        response = self.client().delete(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

#####################    MOVIE TEST ENDS #################################################



#####################    ACTORS TEST START #################################################
    #  GET /actors
    def test_get_actors(self):
        response = self.client().get(
            '/actors',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])


    # GET /actors/id
    def test_get_actor_by_id(self):
        response = self.client().get(
            '/actors/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], 'Pierce Brosnan')

    # def test_get_actor_by_id_404(self):
    #     response = self.client().get(
    #         '/actors/10000',
    #         headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
    #     )
    #     data = json.loads(response.data)
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(data['success'], False)
    #     self.assertTrue(data['message'])
    #     self.assertEqual(data['message'], 'Resource not found')

    # POST /actors
    def test_post_actor(self):
        response = self.client().post(
            '/actors',
            json={'name': 'David', 'age': 44, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor added')
        self.assertEqual(data['actor']['name'], 'David')


    def test_post_actor_400(self):
        response = self.client().post(
            '/actors',
            json={'name': '', 'age': '', "gender": ""},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')

    
    def test_post_actor_401(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Jude', 'age': 44, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()