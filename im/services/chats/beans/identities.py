from pycloudia.uitls.beans import DataBean


class PublicThread(DataBean):
    entity_scope = None
    entity_id = None


class PrivateThread(DataBean):
    thread_id = None


class PersonalThread(DataBean):
    source_id = None
    target_id = None
