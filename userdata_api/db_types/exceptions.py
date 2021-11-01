class ModelNotFound(Exception):
    pass


class RelationshipRequiresBindToSession(Exception):
    pass


class RelationshipRequiresModel(Exception):
    pass


class ModelAlreadyPresent(Exception):
    pass
