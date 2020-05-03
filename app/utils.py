import json
import random
import requests
from threading import Lock

APPLICATION_RESPONSES = dict()
APPLICATION_LOCKS = dict()
AUTH_CODE = 'HbiQ2D6qCqspi36TLvENqLSkXuwVf2Z5bXWJtDJG2xX'

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
    application = user.get_application()
    acquire_lock(application)
    app_queue = application.get_application_queue()
    if app_queue is None or len(app_queue) == 0:
        release_lock(application)
        return None
    apps_reviewed = user.get_reviewed_applications()
    app_number = app_queue.pop(0)
    if apps_reviewed is not None:
        count = 0
        while app_number in apps_reviewed:
            if count > len(apps_reviewed):
                release_lock(application)
                return None
            app_queue.append(app_number)
            app_number = app_queue.pop(0)
            count += 1
    else:
        apps_reviewed = []
    apps_reviewed.append(app_number)
    application.application_list = serialize(app_queue)
    user.applications_reviewed = serialize(apps_reviewed)
    release_lock(application)
    return app_number

"""
Removes the last application from the user's reviewed list and adds it to back to the application queue. 
"""
def put_application_back(user):
    application = user.get_application()
    acquire_lock(application)
    app_queue = application.get_application_queue()
    apps_reviewed = user.get_reviewed_applications()
    app_queue.append(apps_reviewed.pop())
    user.applications_reviewed = serialize(apps_reviewed)
    application.application_list = serialize(app_queue)
    release_lock(user.get_application())
    return

def get_app_with_id(application, response_id):
    if application.id not in APPLICATION_RESPONSES:
        data = get_typeform_responses(AUTH_CODE, application.typeform_id)
        APPLICATION_RESPONSES[application.id] = data
    return APPLICATION_RESPONSES[application.id][response_id]

"""
Uses Typeform Responses API to get the responses for a 
particular form given auth code and form id. 

NOTE: Will break if trying to receive more than 1000 responses. 
"""
def get_typeform_responses(code, form_id):
    URL = 'https://api.typeform.com/forms/{0}/responses?page_size=1000'.format(form_id)
    header = {"Authorization": "Bearer " + code}
    data = []
    response = requests.get(URL, headers=header).json()
    data = response['items']
    print('[DEBUG] Found %d items' % len(data))
    return data

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

def acquire_lock(app):
    if app.id not in APPLICATION_LOCKS:
        APPLICATION_LOCKS[app.id] = Lock()
    APPLICATION_LOCKS[app.id].acquire() 
    return

def release_lock(app):
    APPLICATION_LOCKS[app.id].release()
    return
