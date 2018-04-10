import urllib2
import json
# import pymysql.cursors


API_BASE="http://bartjsonapi.elasticbeanstalk.com/api"

def lambda_handler(event, context):
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.213fc40b-f6db-4781-a81f-f4108307ff35"):
        raise ValueError("Invalid Application ID")
    
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

def on_session_started(session_started_request, session):
    print "Starting new session."

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "GetInfo":
        return get_info(intent)
    elif intent_name == "GetInstructor":
        return get_instructor(intent)
    elif intent_name == "GetAvailableSeats":
        return get_seats(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print "Ending session."
    # Cleanup goes here...

def handle_session_end_request():
    card_title = "BART - Thanks"
    speech_output = "Thank you for using the BART skill.  See you next time!"
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def get_welcome_response():
    session_attributes = {}
    card_title = "UVAclasses"
    speech_output = "Welcome to the Alexa UVA CS Course schedule skill. " 
    reprompt_text = ""
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_info(intent):
    session_attributes = {}
    card_title = "Course Description"
    reprompt_text = ""
    should_end_session = False

    coursenum = "tests"
    description = ""
    if "coursenum" in intent["slots"]:
        coursenum = intent["slots"]["coursenum"]["value"]
    #query database to get description of course name

    #store coursename description 
    speech_output = get_class_info(coursenum)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_instructor(intent):
    session_attributes = {}
    card_title = "Course Instructor"
    reprompt_text = ""
    should_end_session = False

    coursenum = "tests"
    description = ""
    if "coursenum" in intent["slots"]:
        coursenum = intent["slots"]["coursenum"]["value"]
    #query database to get description of course name

    #store coursename description 
    speech_output = get_class_instructor(coursenum)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def get_seats(intent):
    session_attributes = {}
    card_title = "Course Available Seats"
    reprompt_text = ""
    should_end_session = False

    coursenum = "tests"
    description = ""
    if "coursenum" in intent["slots"]:
        coursenum = intent["slots"]["coursenum"]["value"]
    #query database to get description of course name

    #store coursename description 
    speech_output = get_available_seats(coursenum)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def connect_to_db():
    connection = pymysql.connect(host='uvaclasses.martyhumphrey.info',
                             user='UVAClasses',
                             password='TalkingHeads12',
                             db='uvaclasses',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    return connection

def get_class_info(classnum):
    connection = connect_to_db()
    output = "unable to retrieve class information"
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = 'Select Description from CS1188Data WHERE Number= %d' % int(classnum)
            cursor.execute(sql)
            result = cursor.fetchone()
            output = result['Description']
    finally:
        connection.close()
    return output

def get_class_instructor(classnum):
    connection = connect_to_db()
    output = "unable to retrieve information"
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = 'Select Instructor from CS1188Data WHERE Number= %d' % int(classnum)
            cursor.execute(sql)
            result = cursor.fetchone()
            output = result['Instructor']
    finally:
        connection.close()
    return output

def get_available_seats(classnum):
    connection = connect_to_db()
    output = "unable to retrieve information"
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = 'Select Enrollment, EnrollmentLimit from CS1188Data WHERE Number= %d' % int(classnum)
            cursor.execute(sql)
            result = cursor.fetchone()
            output = int(result['EnrollmentLimit']) - (result['Enrollment'])
    finally:
        connection.close()
    return output

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }