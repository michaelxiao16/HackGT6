# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import json
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_core.dispatch_components import (AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name

from ask_sdk_model import Response

from CanvasApi import CanvasApi
canvas = CanvasApi()


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome to Canvas! Try asking for grades, assignments, or courses"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
class UserIntentHandler(AbstractRequestHandler):
    """Handler for NotificationsIntentHandler"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("UserIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Your current user in Canvas is " + str(canvas.get_my_name())
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class NotificationsIntentHandler(AbstractRequestHandler):
    """Handler for NotificationsIntentHandler"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("NotificationsIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Send a text of your phone number to 2-4-0, 3-4-8, 1-3-5-8. That's two four zero, three four eight, one three five eight"
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class ClassListIntentHandler(AbstractRequestHandler):
    """Handler for ClassListIntent"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ClassListIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # classes_json = json.loads(canvas.get_course_names)
        # print(classes_json)
        speak_output = "Here are your classes: " + str(canvas.get_course_names())
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class OfficeHourIntentHandler(AbstractRequestHandler):
    """Handler for OfficeHourIntentHandler"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("OfficeHourIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Searching your classes for office hours"
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("What class do you want to check office hours for?")
                .response
        )
    
class AssignmentIntentHandler(AbstractRequestHandler):
    """Handler for AssignmentIntentHandler"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AssignmentIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        # myh = (handler_input.requestEnvelope)
        assignment_class = str(handler_input.request_envelope.request.intent.slots['AssignmentClass'].value)
        speak_output = str(canvas.get_assignments(assignment_class))
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("What class do you want to check office hours for?")
                .response
        )

class GradesIntentHandler(AbstractRequestHandler):
    """Handler for GradesIntentHandler"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GradesIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = str(canvas.get_all_grades())
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("What class do you want to check office hours for?")
                .response
        )

class QuizzesIntentHandler(AbstractRequestHandler):
    """Handler for Course Announcement Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("QuizzesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        quizzes_class = str(handler_input.request_envelope.request.intent.slots['QuizzesClass'].value)
        speak_output = str(canvas.get_quizzes(quizzes_class))

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

    
class CourseAnnouncementIntentHandler(AbstractRequestHandler):
    """Handler for Course Announcement Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CourseAnnouncementIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        course_announcement_class = str(handler_input.request_envelope.request.intent.slots['CourseAnnouncementClass'].value)
        speak_output = str(canvas.get_announcement(course_announcement_class))

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class NewAnnouncementIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("NewAnnouncementIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = str(canvas.get_all_announcements())
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

""" Amazon Built-in Intents """ 
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(UserIntentHandler())
sb.add_request_handler(NotificationsIntentHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(ClassListIntentHandler())
sb.add_request_handler(OfficeHourIntentHandler())
sb.add_request_handler(AssignmentIntentHandler())
sb.add_request_handler(GradesIntentHandler())
sb.add_request_handler(QuizzesIntentHandler())
sb.add_request_handler(CourseAnnouncementIntentHandler())
sb.add_request_handler(NewAnnouncementIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()