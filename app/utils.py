import json
import random

"""
Generates a queue of elements for the corresponding applications. 
Assumes that the applications are all zero indexed. 
"""
def generate_queue_from_application(application):
    num_applications = application.num_apps
    rev_per_app = application.reviews_per_app
    app_queue = _generate_queue(num_applications, rev_per_app) 
    return app_queue

"""
Generates a list that contains num_applications * rev_per_app elements.
"""
def _generate_queue(num_applications, rev_per_app):
    queue = [i for i in range(num_applications) for _ in range(rev_per_app)]
    random.shuffle(queue)
    return queue

"""
Gets the next application off the queue for the current user.
If the user has already reviewed this application, then push
it to the end of the queue and pop another one off.
"""
def get_next_application(user):
    apps_reviewed = set(user.applications_reviewed)
    app_number = user.application.application_queue.pop(0)
    while app_number in apps_reviewed:
        user.application.application_queue.append(app_number)
        app_number = user.application.application_queue.pop(0)
    return app_number


"""
Helper Functions
"""
def serialize(obj):
    return json.dumps(obj)

def deserialize(obj):
    return json.loads(obj)
