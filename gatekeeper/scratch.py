import yaml


class Foo(yaml.YAMLObject):

    yaml_tag = '!Foo'

    def __init__(self, name: str) -> None:
        self.name = name




f = Foo(name='bar')

print(f.name)
