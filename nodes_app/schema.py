import graphene

from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from . import models


class NodeType(DjangoObjectType):
    class Meta:
        model = models.Node
        filter_fields = ('name', )
        interfaces = (graphene.relay.Node, )


class ClassifierType(DjangoObjectType):
    class Meta:
        model = models.Classifier
        filter_fields = {
            'name': ['exact', 'icontains', ],
        }
        interfaces = (graphene.relay.Node, )


class AnswerMessageType(DjangoObjectType):
    class Meta:
        model = models.AnswerMessage
        filter_fields = ('text', )
        interfaces = (graphene.relay.Node, )


class Query(graphene.AbstractType):
    nodes = DjangoFilterConnectionField(NodeType)
    classifiers = DjangoFilterConnectionField(ClassifierType)
    answer_messages = DjangoFilterConnectionField(AnswerMessageType)

    def resolve_classifiers(self, info, **kwargs):
        return models.Classifier.objects.all()

    def resolve_nodes(self, info, **kwargs):
        return models.Node.objects.select_related(
            'classifier', 'answer_message'
        ).all()


class CreateNode(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        data_set = graphene.String()

    ok = graphene.Boolean()

    def mutate(self, info, name, data_set):
        node = models.Node(
            name=name,
            description='some description',
            classifier_id=1,
            answer_message_id=1,
            data_set=data_set
        )
        node.save()
        return CreateNode(ok=True)

