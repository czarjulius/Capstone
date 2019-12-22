
import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor

EXECUTIVE_PRODUCER = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJqQkdRVGMwTkRBd016WkNOek5DUVRjeU5VUXdOVGRHTVVKR01UQXhNekU0TkVORU4wVkJOUSJ9.eyJpc3MiOiJodHRwczovL2p1bGl1cy1jemFyLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGY4Y2ZiY2MyMjQ3ZjBlYTIwZmVlY2UiLCJhdWQiOiJtb3ZpZSIsImlhdCI6MTU3NzA0NDQ3NSwiZXhwIjoxNTc3MDUxNjc1LCJhenAiOiI0S3FjeHFWbklXd0ZFRkRlNjBwdHNEVUVBZDVaUDZORyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.E4ITdm-y6cCkPXVcJvZsoKhQ43PwqMogldt1l7PvHOpXOj1q1iCd1yBAlJxNd3gUtrp5i6Sq75Yb3Cf9HlZ6es8vE5QBa0p6tYFIQAbvU8OP3Vugk0v4pUjErlVEzaplc2mvoTBW-7PNzeFtxMMP3ACsz3tp5891ELu9ZY4V6pAqcOcJmk8p4yEKzHZJVhAphpEpZ__CfcdJmjHTYPfoRG1UvQciIUr3vlGVJV9sgIbhmoJmtllF5ZPmpwirhmBy9MwNC0G5k5ri8oQ0g7Dn50Vto0TCCbpNke09T7TwQ8_YTXKLe5_cZf9ARtb1cBIZzFlRhn1xJZkYGZoVUHf84Q'

CASTING_DIRECTOR = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJqQkdRVGMwTkRBd016WkNOek5DUVRjeU5VUXdOVGRHTVVKR01UQXhNekU0TkVORU4wVkJOUSJ9.eyJpc3MiOiJodHRwczovL2p1bGl1cy1jemFyLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGZjOWYyNjk0ZDdhNTE1MzY1ZjdhMzgiLCJhdWQiOiJtb3ZpZSIsImlhdCI6MTU3NzA0NDU2NiwiZXhwIjoxNTc3MDUxNzY2LCJhenAiOiI0S3FjeHFWbklXd0ZFRkRlNjBwdHNEVUVBZDVaUDZORyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.nbxd2tw1o1PfOaxoqN-nRowjn5khpwg1H_cfceseZV_pmwcnnDkv1zXMu4mVVg8DliECmI95mKmFCzKeQWntfqPiCRs_R1_dIf3YvF3ZVZdIP5srk5mnEaluQssW4igI2mIVy5Uxzo4NaEj9jsZpC_0L5nZXAykyU_XMX8LFDmjolHqtK8DURAo__aK8lL3OtouqpaI_SLVp5TV6L5JTA_WoKh0zGiF1JF8AAKY1c44cPd3ctRLWLTBX3Lzp6L2hDdOOxJDhjbtjqapf57X7pVuin_hp-fmDFnFOpj6fCanMZoNhwncJDlT-IFBCMTLBCs8m7O2jkiKxRO9zFe3cmA'

CASTING_ASSISTANT = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJqQkdRVGMwTkRBd016WkNOek5DUVRjeU5VUXdOVGRHTVVKR01UQXhNekU0TkVORU4wVkJOUSJ9.eyJpc3MiOiJodHRwczovL2p1bGl1cy1jemFyLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZGZjOWZmNDk0ZDdhNTE1MzY1ZjdhNDEiLCJhdWQiOiJtb3ZpZSIsImlhdCI6MTU3NzA0NDY2MSwiZXhwIjoxNTc3MDUxODYxLCJhenAiOiI0S3FjeHFWbklXd0ZFRkRlNjBwdHNEVUVBZDVaUDZORyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.Gty18NQclNKdtGjzmfoApvhY5FYApio_Dq-i-3C00jcTTlbQNGQLL8ysK2fOn_N8G2NFEt1wnYUl2AgDnWD_E6C6nn37b01neAT2ecYW_LaKhCzrHxmn7l7FCPeTm2aDRGAnFB3fqGNyeo2hLP5dL_rLv_D72V2VdU9M0wT5Lbo-HWO15z57olAx7JRUQg-cxa45eiApRTgd6k8BdiPrD_EL_jblmpbrMM6hWlt9TkQ5l7L4_USzYBzaRMDsien7HYzj3RapetAz--tzJPIvzKMGfKqetucXbgNZNGY2muieNc1BLPcF4Qb8oyLGzcnJBZhXt9lPxOrU7KQlv8ofhQ'


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
    def test_get_movie_byId(self):
        response = self.client().get(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Nikita')

    def test_get_movie_byId_404(self):
        response = self.client().get(
            '/movies/333333',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Resource not found')

    # POST /movies
    def test_post_movie(self):
        response = self.client().post(
            '/movies',
            json={'title': 'Sigidi', 'release_date': "2017-02-19"},
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie created successfully')
        self.assertEqual(data['movie']['title'], 'Sigidi')

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
            json={'title': 'Unauthorize movie', 'release_date': "2019-12-23"},
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    # PATCH /movies
    def test_edit_movie(self):
        response = self.client().patch(
            '/movies/2',
            json={'title': 'The Squash', 'release_date': "2000-10-19"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Movie updated')
        self.assertEqual(data['movie']['title'], 'The Squash')


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
            '/movies/4444444',
            json={'title': 'New Life', 'release_date': "2003-09-16"},
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
        self.assertEqual(data['message'], 'Movie deleted successfully')

    def test_delete_movie_404(self):
        response = self.client().delete(
            '/movies/11111111',
            headers={"Authorization": "Bearer " + EXECUTIVE_PRODUCER}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

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
    def test_get_actor_byId(self):
        response = self.client().get(
            '/actors/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], 'Arnold Swaztnigger')

    def test_get_actor_byId_404(self):
        response = self.client().get(
            '/actors/121234',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])
        self.assertEqual(data['message'], 'Resource not found')

    # POST /actors
    def test_post_actor(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Julius', 'age': 24, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor added')
        self.assertEqual(data['actor']['name'], 'Julius')


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
            json={'name': 'Czar', 'age': 14, "gender": "female"},
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    # PATCH /actors
    def test_edit_actor(self):
        response = self.client().patch(
            '/actors/2',
            json={'name': 'Emily', 'age': 37, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor updated')
        self.assertEqual(data['actor']['name'], 'Emily')

    def test_edit_actor_400(self):
        response = self.client().patch(
            '/actors/2',
            json={'name': '', 'age': '', "gender": ""},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request, pls check your inputs')


    def test_edit_actor_404(self):
        response = self.client().patch(
            '/actors/9999999',
            json={'name': 'Mike', 'age': 65, "gender": "male"},
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')


    # DELETE /actors/id
    def test_delete_actor(self):
        response = self.client().delete(
            '/actors/3',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Actor deleted successfully')

    
    def test_delete_actor_401(self):
        response = self.client().delete(
            '/actors/2',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['message']['code'], 'unauthorized')

    
    def test_delete_actor_404(self):
        response = self.client().delete(
            '/actors/545432',
            headers={"Authorization": "Bearer " + CASTING_DIRECTOR}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()