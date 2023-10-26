class ServerCreatorHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ServerCreator")(handler_input)

    def handle(self, handler_input):
        speak_output = "I STILL DIDN'T IMPLEMENT THIS ONE!"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )