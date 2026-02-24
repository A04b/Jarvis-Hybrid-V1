#JARVIS as Linux terminal assistant
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_ai_response(prompt):
    model = genai.GenerativeModel('models/gemini-2.5-flash')
    response = model.generate_content(f"You are a Linux Terminal Expert. {prompt}")
    return response.text
    
def jarvis_linux():
    print("# ---   JARVIS LINUX MODE ACTIVATED   --- #")
    while True:
        user_input = input("Jarvis@Ubuntu:~$ ").lower()
        if "exit" in user_input or "stop" in user_input:
            break


        elif "clear" in user_input:
            os.system('clear')
        
        #using command 'cd directory' (navigates to that directory as in terminal)
        elif "cd" in user_input:
                folder = user_input.replace("cd","").strip()
                
                if not folder:
                    print("Please specify a folder name!!!")
                    continue

                if folder in ["..", "~"]:
                    found_path = folder 
                else:    
                    items= os.listdir('.')
                    found_path = None
                    for item in items:
                        if item.lower() == folder.lower() and os.path.isdir(item):  #since used lower() for user_input, check as such
                            found_path = item
                            print(item)
                            break
                   
                try:
                    print(f"Attempting to navigate to '{folder}' ...")
                    #print(f"Found path: {found_path}")
                    os.chdir(found_path)
                    print(f"Systems moved to {os.getcwd()}")
                except Exception as e:
                    print(f"Folder not found: {e}")

        #using command 'list' or 'ls', lists the files/folders of current directory
        elif "list" in user_input or "ls" in user_input:
            files = os.listdir('.')
            print(f"Contents of {os.getcwd()}:")
            for item in files:
                print(f"  - {item}")

        #using command 'compile file_name.extension'(but first navigate to that folder using go to)
        elif "compile" in user_input:   #compile and run any file of c, cpp and py
            print("Locating the file...")
            raw_name = user_input.replace("compile","").strip()     #Problem of case sensitivity solved! (Implemented Fuzzy Search Feature)

            items = os.listdir('.')         #Scan files of current directory
            file_name = None
            
            for item in items:
                if item.lower() == raw_name:
                    file_name = item
                    break
            if file_name and os.path.exists(file_name):
                if(file_name.endswith(".c")):
                    status = os.system(f"gcc {file_name} -o output && ./output")
                    if status != 0:
                        print("There was an error compiling or running the C file.")    

                elif(file_name.endswith(".py")):
                    status = os.system(f"python3 {file_name}")
                    if status != 0:
                        print("There was an error compiling or running the Python file.")    
                
                elif(file_name.endswith(".cpp")):
                    status = os.system(f"g++ {file_name} -o output && ./output")
                    if status != 0:
                        print("There was an error compiling or running the C file.")    
                
                else:
                    print(f"Unsupported file type: {file_name}")

            else:
                print(f"I cannot find the file: {file_name}")   #Above else just checks file types and this for checking file names


        else:
            print("Thinking...")
            print(get_ai_response(user_input))


if __name__ == "__main__":
    jarvis_linux()