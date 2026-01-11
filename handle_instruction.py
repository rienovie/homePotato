

def handle_instruction(instruction):

    # TODO: this does not feel very efficient but should work for now
    if instruction.__contains__("cancel" or "stop"):
        print("Cancelling")
        return
    if instruction.__contains__("weather"):
        print("weather / unhandled")
    elif instruction.__contains__("play"):
        print("playing / unhandled")
    elif instruction.__contains__("timer"):
        print("timer / unhandled")
    elif instruction.__contains__("time"):
        print("time / unhandled")
    else:
        print("Unknown instruction:", instruction)
        return

