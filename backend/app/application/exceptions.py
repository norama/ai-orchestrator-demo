class WorkflowNotFound(Exception):
    pass


class InvalidWorkflowOperation(Exception):
    pass


class CatalogItemNotFound(Exception):
    pass


class SnapshotNotFound(Exception):
    pass


class SnapshotWorkflowMismatch(Exception):
    pass


class MissingWorkspaceId(Exception):
    pass


class InvalidWorkspaceId(Exception):
    pass
