import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from graphql_relay.node.node import from_global_id

from .models import Image, Post

class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node,)

class ImageNode(DjangoObjectType):
    class Meta:
        model = Image
        interfaces = (graphene.relay.Node,)

class AddImagesToPostMutation(graphene.relay.ClientIDMutation):
    post = graphene.Field(PostNode)

    class Input:
        post_id = graphene.Argument(graphene.ID, required=True)
        images = graphene.Argument(
            graphene.List(graphene.String),
            required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        post_relay_id = input.get("post_id")
        post_instance = Post.objects.get(id=from_global_id(post_relay_id)[1])
        if post_instance:
            # if post exists
            images = input.get("images") # get image file names
            if info.context.FILES and images: # <- got empty FILES dict in test
                # if request have files
                for image_data in images:
                    # create image
                    image = Image(
                        post=post_instance,
                        image_file=info.context.FILES[image_data.image_file]
                    )
                    image.full_clean()
                    image.save()
                return cls(post=post_instance)
            else:
                raise IndexError()
        raise Post.DoesNotExist

class AppMutation():
    add_images_to_post = AddImagesToPostMutation.Field()