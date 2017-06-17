"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""


from __future__ import print_function
import urllib2
import string,ast

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
    card_title = "Welcome"
    speech_output = "OK, the waiter is coming."
    response = urllib2.urlopen('http://183.175.14.209:6228/waiter/')

    reprompt_text = speech_output
    should_end_session = False

    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def fail_session(intent, session):

    card_title = intent['name']
    session_attributes = session['attributes']
    should_end_session = False


    speech_output = 'Sorry, I cannot understand your speech.'
    reprompt_text = 'Sorry, I cannot understand your speech.'

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()

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
        elif event['request']['type'] == "SessionEndedRequest":
            return on_session_ended(event['request'], event['session'])
    except ValueError:
        return fail_session(event['request'], event['session'])
