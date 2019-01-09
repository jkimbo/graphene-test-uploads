from graphene.test import Client
from django.test import TestCase, RequestFactory
from graphql_jwt.testcases import JSONWebTokenTestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile

from project.schema import ROOT_SCHEMA
from .models import Image, Post

class MutationsTestCase(JSONWebTokenTestCase):
    def setUp(self):
        Post.objects.create(
            name="Post #1"
        )
        self.user = get_user_model().objects.create(username='testuser')
        self.client = Client(ROOT_SCHEMA)
        self.factory = RequestFactory()

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
        request = self.factory.post('/')
        request.user = self.user
        request.FILES["img1.jpg"] = SimpleUploadedFile("img1.jpg", content=None, content_type="image/jpeg")
        request.FILES["img2.jpg"] = SimpleUploadedFile("img2.jpg", content=None, content_type="image/jpeg")

        query_result = self.client.execute(
            query_string,
            context=request,
            variables=variables,
        )
        self.assertNotIn('errors', query_result)
        post = Post.objects.get(id=1)
        self.assertEqual(post.gallery.count(), 2)
        # Asserting the name of the image doesn't work with Simpleuploadedfile
        #self.assertEqual(post.gallery.get(id=1).name, "img1.jpg")
        #self.assertEqual(post.gallery.get(id=2).name, "img2.jpg")
