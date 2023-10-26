import requests


class ServerCreatorHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ServerCreator")(handler_input)

    def handle(self, handler_input):
        speak_output = "Give me 2-3 minutes and it will be ready"
        
        
        server_size = ask_utils.request_util.get_slot(handler_input, "SERVER_SIZE").value
        sever_name = ask_utils.request_util.get_slot(handler_input, "SERVER_NAME").value
        
        url = "REPLACE_ME"
        params = {'server_size': server_size, 'server_name': sever_name}

        requests.post(url, params=params)

        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
