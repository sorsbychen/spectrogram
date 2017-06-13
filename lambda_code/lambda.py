"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""


from __future__ import print_function
import urllib2

menu = ['Smoked Haddock Fish Cakes',
        'Chicken & Mushroom Risotto',
        'Mushroom Pasta',
        'Roasted Salmon Fillet',
        'Jumbo Hot Dog',
        'Premium Fresh Rib-Eye Steak',
        'Fajita Chicken Wings',
        'House salad',
        'American style burger']


def make_order(table, name, order, remark):
    name = name.replace(' ','%20')
    order = order.replace(' ','%20')
    remark = remark.replace(' ','%20')
    response = urllib2.urlopen('http://183.175.14.209:6228/order/%s/%s/%s/%s/'%(table, name, order, remark))  



# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {'status':0,'info':[],'usr':'xxx','order':'xxx'}
    card_title = "Welcome"
    speech_output = "Welcome to the BP restaurant. My name is Alexa. "\
                    "I am your waiter today. Let me tell you about our specials today. "\
                    " We have a miso-glazed Chilean Sea Bass, with a side of mashed sweet potatoes, and sauteed spinach. "\
                    "You can ask me questions about the menu. To order your food, you just need to say, Alexa, start ordering."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = speech_output
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def create_favorite_color_attributes(favorite_color):
    return {"favoriteColor": favorite_color}


def set_usr_in_session(intent, session):

    card_title = intent['name']
    session_attributes = session['attributes']
    session_attributes['status'] = 2

    should_end_session = False

    usr_name_str = intent['slots']['Name']['value']
    speech_output = "Hello," + usr_name_str + ". What can get for you?"     
    session_attributes['usr'] = usr_name_str

    reprompt_text = speech_output

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def set_order_in_session(intent, session):

    card_title = intent['name']
    session_attributes = session['attributes']
    session_attributes['status'] = 3

    should_end_session = False

    order_name_str = intent['slots']['Food']['value']
    usr_name_str = session_attributes['usr']
    session_attributes['order'] = order_name_str
    session_attributes['info'].append([usr_name_str,order_name_str])

    speech_output = "Sure, a " + order_name_str + " for " + usr_name_str
    if 'steak' in order_name_str or 'Steak' in order_name_str:
        speech_output = speech_output + '. Hi, '+ usr_name_str + ', how do you like your steak done?'
        session_attributes['status'] = -3        

    make_order('01', session_attributes['usr'], session_attributes['order'], '')

    reprompt_text = 'sorry I cannot recognize you.'

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def set_steak_in_session(intent, session):

    card_title = intent['name']
    session_attributes = session['attributes']
    session_attributes['status'] = 3

    should_end_session = False

    stk_name_str = intent['slots']['SteakValue']['value']
    speech_output = "Sure, " + stk_name_str + " it is." 

    reprompt_text = 'sorry I cannot recognize you.'

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def start_order_session(intent, session):
    """ Start ordering
    """

    card_title = intent['name']
    session_attributes = session['attributes']
    session_attributes['status'] = 1

    should_end_session = False


    speech_output = "Thank you. May I have your name please?"
    reprompt_text = 'Sorry, I cannot understand your speech.'

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def fail_session(intent, session):

    card_title = intent['name']

    should_end_session = False


    speech_output = 'Sorry, I cannot understand your speech.'
    reprompt_text = 'Sorry, I cannot understand your speech.'

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def reply_query_session(intent, session):
    """ Start ordering
    """

    card_title = intent['name']
    session_attributes = session['attributes']

    should_end_session = False

    order_name_str = intent['slots']['Food']['value']

    if order_name_str == 'mushroom pasta':
        speech_output = 'Calories per serving of mushroom pasta: 200 calories of Pasta, 65 calories of Cream of Mushroom Soup. In total 265 calories.'
    else:
        speech_output = 'Sorry, I have no idea.'

    reprompt_text = 'Sorry, I cannot understand your speech.'

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def handle_order_end_request(intent, session):
    card_title = "Order Ended"
    speech_output = "Good choices. Your food will be ready in 10 minutes."
    session_attributes = session['attributes']
    session_attributes['status'] = 0

    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def pay_session(intent, session):
    card_title = "Pay"
    speech_output = 'Sure. The bill is on its way. Before paying, you can leave your comments to me.'
    session_attributes = session['attributes']
    session_attributes['status'] = 0

    # Setting this to true ends the session and exits the skill.
    should_end_session = False
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))    


def handle_session_end_request(intent, session):
    card_title = "Session Ended"
    speech_output = "Good choices. Your food will be ready in 10 minutes."
    session_attributes = session['attributes']
    session_attributes['status'] = 0

    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))




def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    session_attributes = session['attributes']
    try:
        if  intent_name == "StartOrderIntent":
            return start_order_session(intent, session)

        if  intent_name == "QueryIntent":
            return reply_query_session(intent, session)
        if  intent_name == "FinishIntent":
            return handle_order_end_request(intent, session)
        if  intent_name == "PayIntent":
            return pay_session(intent, session)

        if session_attributes['status'] == 1: # after start ordering
            if intent_name == 'StartOrderIntent':
                return start_order_session(intent, session) #repeat if start ordering is asked again
            elif intent_name == "MyNameIsIntent":
                return set_usr_in_session(intent, session) #after my name is ..., then status is 2
        if session_attributes['status'] == 2:  #after my name is ...
            if intent_name == "MyNameIsIntent":
                return set_usr_in_session(intent, session) #repeat if new name
            elif intent_name == "MakeOrderIntent":
                return set_order_in_session(intent,session)
        if session_attributes['status'] == 3:  #after my name is ...
            if intent_name == "MakeOrderIntent":
                return set_order_in_session(intent,session)
        if session_attributes['status'] == -3:
            if intent_name == 'SteakIntent':
                return set_steak_in_session(intent,session)
    except ValueError:
        return fail_session(intent,session)

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    try:
        print("event.session.application.applicationId=" +
              event['session']['application']['applicationId'])

        """
        Uncomment this if statement and populate with your skill's application ID to
        prevent someone else from configuring a skill that sends requests to this
        function.
        """
        # if (event['session']['application']['applicationId'] !=
        #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
        #     raise ValueError("Invalid Application ID")

        if event['session']['new']:
            on_session_started({'requestId': event['request']['requestId']},
                               event['session'])

        if event['request']['type'] == "LaunchRequest":
            response_r = on_launch(event['request'], event['session'])
            return response_r
        elif event['request']['type'] == "IntentRequest":
            response_r = on_intent(event['request'], event['session'])
            return response_r
        elif event['request']['type'] == "SessionEndedRequest":
            return on_session_ended(event['request'], event['session'])
    except ValueError:
        return fail_session(event['request'], event['session'])
