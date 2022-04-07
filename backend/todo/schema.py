import graphene
from graphene_django import DjangoObjectType
from .models import Project, Todo


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = '__all__'


class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        fields = '__all__'



class Query(graphene.ObjectType):
    all_projects = graphene.List(ProjectType)

    def resolve_all_projects(root, info):
        return Project.objects.all()

    all_todos = graphene.List(TodoType)

    def resolve_all_todos(root, info):
        return Todo.objects.all()

    project_by_id = graphene.Field(ProjectType, pk=graphene.Int(required=True))

    def resolve_project_by_id(root, info, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return None

    project_by_name = graphene.List(ProjectType, name=graphene.String(required=False))

    def resolve_project_by_name(root, info, name=None):
        project = Project.objects.all()
        if name:
            project = Project.objects.filter(project_users=name)
        return project


class ProjectCreateMutation(graphene.Mutation):
    class Arguments:
        project_users = graphene.String(required=True)
        project_name = graphene.String(required=True)
        git_name = graphene.Int(required=True)

    project = graphene.Field(ProjectType)

    @classmethod
    def mutate(cls, root, info, project_users, project_name, git_name):
        project = Project(project_users=project_users, project_name=project_name, git_name=git_name)
        project.save()
        return cls(project)


class  ProjectUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        project_users = graphene.String(required=False)
        project_name = graphene.String(required=False)
        git_name = graphene.Int(required=False)

    project = graphene.Field(ProjectType)


    @classmethod
    def mutate(cls, root, info, id, project_users=None, project_name=None, git_name=None):
        project = Project.objects.get(pk=id)
        if project_users:
            project.project_users = project_users
        if project_name:
            project.project_name = project_name
        if git_name:
            project.git_name = git_name
        if project_users or project_name or git_name:
            project.save()
        return cls(project)


class Mutations(graphene.ObjectType):
    create_project = ProjectCreateMutation.Field()
    update_project = ProjectUpdateMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)