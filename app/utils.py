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
    user.get_application().acquire_lock()
    app_queue = user.get_application().get_application_queue()
    if app_queue is None or len(app_queue) == 0:
        user.get_application().release_lock()
        return None
    apps_reviewed = user.get_reviewed_applications()
    app_number = app_queue.pop(0)
    if apps_reviewed is not None:
        count = 0
        while app_number in apps_reviewed:
            if count > len(apps_reviewed):
                user.get_application().release_lock()
                return None
            app_queue.append(app_number)
            app_number = app_queue.pop(0)
            count += 1
    else:
        apps_reviewed = []
    apps_reviewed.append(app_number)
    user.get_application().application_list = serialize(app_queue)
    user.applications_reviewed = serialize(apps_reviewed)
    user.get_application().release_lock()
    return app_number

"""
Removes the last application from the user's reviewed list and adds it to back to the application queue. 
"""
def put_application_back(user):
    user.get_application().acquire_lock()
    app_queue = user.get_application().get_application_queue()
    apps_reviewed = user.get_reviewed_applications()
    app_queue.append(apps_reviewed.pop())
    user.applications_reviewed = serialize(apps_reviewed)
    user.get_application().application_list = serialize(app_queue)
    user.get_application().release_lock()
    return

"""
Helper Functions
"""
def serialize(obj):
    if obj is None:
        return None
    return json.dumps(obj)

def deserialize(obj):
    if obj is None:
        return None
    return json.loads(obj)
