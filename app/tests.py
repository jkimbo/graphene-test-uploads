from django.test import TestCase
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model
import tempfile

from .models import Image, Post

class MutationsTestCase(JSONWebTokenTestCase):
    def setUp(self):
        Post.objects.create(
            name="Post #1"
        )
        self.user = get_user_model().objects.create(username='testuser')
        self.client.authenticate(self.user)

    def test_add_images_to_post(self):
        query_string = """
            mutation($input: AddImagesToPostMutationInput!){
                addImagesToPost(input: $input){
                    post{
                        name
                    }
                }
            }
        """
        variables = {
            "input": {
                "postId": "UG9zdE5vZGU6MQ==",
                "images": [
                    "img1.jpg",
                    "img2.jpg"
                ]
            }
        }
        context = {
            "img1.jpg": tempfile.NamedTemporaryFile(suffix=".jpg"),
            "img2.jpg": tempfile.NamedTemporaryFile(suffix=".jpg")
        }
        query_result = self.client.execute(
            query_string,
            context=context,
            variables=variables,
        )
        post = Post.objects.get(id=1)
        self.assertEqual(post.gallery.get(id=1).name, "img1.jpg")
        self.assertEqual(post.gallery.get(id=2).name, "img2.jpg")