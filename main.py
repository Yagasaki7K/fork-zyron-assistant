import time
from listener import listen_for_command, take_user_input, speak
from brain import process_command
from muscles import execute_command

def main():
    print("⚡ SYSTEM ONLINE: Say 'Hey Pikachu' to start...")
    
    while True:
    
        if listen_for_command():
            
            user_query = take_user_input()
            
            if user_query:
               
                action_json = process_command(user_query)
                
               
                if action_json:
                   
                    response_text = execute_command(action_json)
                    
                   
                    if response_text and isinstance(response_text, str) and not response_text.endswith(".png"):
                        speak(response_text)
                    else:
                        speak("Done.")
                else:
                    speak("I am not sure how to do that yet.")
            
     
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚡ System shutting down.")