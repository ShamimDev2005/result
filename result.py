import urllib.request
import urllib.parse
import json
import datetime

# ANSI color codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
BLUE = '\033[94m'
RESET = '\033[0m'

# Board names and their corresponding IDs
BOARD_NAMES = {
    "1": "Dhaka",
    "2": "Rajshahi",
    "3": "Chittogram",
    "4": "Jashore",
    "5": "Cumilla",
    "6": "Barishal",
    "7": "Sylhet",
    "8": "Dinajpur",
    "9": "Madrasah",
    "10": "Mymensingh",
    "11": "Technical",
    "12": "BOU"
}

def show_board_list():
    print(f"\n{CYAN}Choose a board:{RESET}")
    print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")
    
    # Calculate the maximum width needed for proper alignment
    max_id_length = max(len(key) for key in BOARD_NAMES.keys())
    
    # Create two columns of boards for better space utilization
    boards = list(BOARD_NAMES.items())
    half = (len(boards) + 1) // 2  # Ceiling division for odd numbers
    
    for i in range(half):
        left_id, left_name = boards[i]
        # Format the left column with proper padding
        left_display = f"{left_id.rjust(max_id_length)}. {left_name.ljust(12)}"
        
        # Check if there's a right column item
        if i + half < len(boards):
            right_id, right_name = boards[i + half]
            right_display = f"{right_id.rjust(max_id_length)}. {right_name}"
            print(f"{CYAN}{left_display}     {right_display}{RESET}")
        else:
            print(f"{CYAN}{left_display}{RESET}")
    
    print(f"{CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━{RESET}")

def get_input_with_back_option(prompt, current_step, show_back_hint=True):
    if show_back_hint and current_step > 1:  # Don't show back hint for first step
        print(f"{BLUE}[Type 'back' to return to previous step]{RESET}")
    
    user_input = input(prompt).strip()
    
    # Make 'back' case-insensitive
    if user_input.lower() == 'back' and current_step > 1:  # Only allow back if not at first step
        return "BACK", current_step - 1
    return user_input, current_step + 1

def get_result():
    try:
        print(f"\n{GREEN}═══════════════════════════════════{RESET}")
        print(f"{GREEN}    EDUCATION BOARD RESULT CHECKER  {RESET}")
        print(f"{GREEN}═══════════════════════════════════{RESET}\n")
        
        # Variable to track current step in the input flow
        current_step = 1
        exam = None
        year = None
        roll = None
        reg = None
        board_id = None
        board_name = None
        
        # Main input loop with back navigation
        while current_step <= 4:  # We have 4 input steps
            # Step 1: Get exam (no back option here as it's the first step)
            if current_step == 1:
                while True:
                    if exam:
                        print(f"{CYAN}Current exam: {exam}{RESET}")
                    
                    # First step should not show back hint
                    user_input, next_step = get_input_with_back_option(
                        f"{CYAN}Enter exam (jsc, ssc, hsc): {RESET}", 
                        current_step, 
                        show_back_hint=False)
                    
                    if user_input.lower() in ["jsc", "ssc", "hsc"]:
                        exam = user_input.lower()
                        current_step = next_step
                        break
                    else:
                        print(f"{RED}Invalid exam. Please try again.{RESET}\n")
            
            # Step 2: Get year
            elif current_step == 2:
                current_year = datetime.datetime.now().year
                while True:
                    if year:
                        print(f"{CYAN}Current year: {year}{RESET}")
                        
                    user_input, next_step = get_input_with_back_option(
                        f"{CYAN}Enter {exam} year (1996-{current_year}): {RESET}", current_step)
                    
                    if user_input == "BACK":
                        current_step = next_step
                        exam = None  # Reset exam when going back
                        break
                        
                    if user_input.isdigit() and len(user_input) == 4 and 1996 <= int(user_input) <= current_year:
                        year = user_input
                        current_step = next_step
                        break
                    else:
                        print(f"{RED}Invalid year. Must be between 1996 and {current_year}.{RESET}\n")
            
            # Step 3: Get roll and reg
            elif current_step == 3:
                # Reset roll and reg for this step if coming from a different step
                if roll is not None or reg is not None:
                    # Display current values if they exist
                    if roll:
                        print(f"{CYAN}Current roll: {roll}{RESET}")
                    if reg:
                        print(f"{CYAN}Current reg: {reg}{RESET}")
                
                # Get roll number
                while True:
                    roll_prompt = f"{CYAN}Enter {exam} roll (6 digits or Enter to skip): {RESET}"
                    user_input, temp_step = get_input_with_back_option(roll_prompt, current_step)
                    
                    if user_input == "BACK":
                        current_step = temp_step
                        year = None  # Reset year when going back
                        roll = None  # Reset roll
                        reg = None   # Reset reg
                        break
                        
                    # If user wants to skip roll
                    if not user_input:
                        roll = None
                        break
                        
                    # Validate roll
                    if user_input.isdigit() and len(user_input) == 6:
                        roll = user_input
                        break
                    else:
                        print(f"{RED}Roll must be exactly 6 digits. Please try again.{RESET}\n")
                
                # If we went back from roll input, continue the outer loop
                if user_input == "BACK":
                    continue
                
                # Get reg number
                while True:
                    reg_prompt = f"{CYAN}Enter {exam} reg (10 digits or Enter to skip): {RESET}"
                    user_input, temp_step = get_input_with_back_option(reg_prompt, current_step)
                    
                    if user_input == "BACK":
                        # If user wants to go back from reg, go back to roll input
                        # but stay in the current step
                        roll = None
                        break
                    
                    # If user wants to skip reg
                    if not user_input:
                        reg = None
                        break
                        
                    # Validate reg
                    if user_input.isdigit() and len(user_input) == 10:
                        reg = user_input
                        break
                    else:
                        print(f"{RED}Reg must be exactly 10 digits. Please try again.{RESET}\n")
                
                # If we went back from reg input, continue with roll input again
                if user_input == "BACK":
                    continue
                
                # Ensure at least one of roll or reg is provided
                if not roll and not reg:
                    print(f"{RED}You must provide either roll or reg number. Both cannot be skipped.{RESET}\n")
                    continue
                
                # If we've made it here, move to the next step
                current_step = 4
            
            # Step 4: Get board
            elif current_step == 4:
                if board_id:
                    print(f"{CYAN}Current board: {board_name}{RESET}")
                
                show_board_list()  # Show board list before asking for input
                
                while True:
                    user_input, next_step = get_input_with_back_option(
                        f"{CYAN}Enter board number: {RESET}", current_step)
                    
                    if user_input == "BACK":
                        current_step = 3  # Go back to roll/reg step
                        board_id = None
                        board_name = None
                        break
                        
                    if user_input in BOARD_NAMES:
                        board_id = user_input
                        board_name = BOARD_NAMES[user_input]
                        current_step = next_step
                        break
                    else:
                        print(f"{RED}Invalid board number. Try again.{RESET}\n")
        
        # All inputs collected, now fetch the result
        print(f"\n{YELLOW}Summary of inputs:{RESET}")
        print(f"{YELLOW}Exam: {exam.upper()}{RESET}")
        print(f"{YELLOW}Year: {year}{RESET}")
        if roll:
            print(f"{YELLOW}Roll: {roll}{RESET}")
        if reg:
            print(f"{YELLOW}Reg: {reg}{RESET}")
        print(f"{YELLOW}Board: {board_name}{RESET}")
        
        # Confirm and proceed (empty input defaults to yes)
        print(f"\n{BLUE}(Press Enter to proceed, type 'back' to go back, or 'n' to cancel){RESET}")
        confirm = input(f"{CYAN}Proceed with these details? [Y/n/back]: {RESET}").strip().lower()
        
        if confirm == "back":
            # Go back to board selection if user wants to change something
            current_step = 4
            board_id = None
            board_name = None
            # Go back to step 4 and continue the input loop
            get_result()
            return
        elif confirm == "n" or confirm == "no":
            print(f"{RED}Search cancelled.{RESET}\n")
            return
        # Empty input or 'y'/'yes' will proceed (default behavior)
        
        # Construct the URL with the obtained parameters
        base_url = "http://app.rajshahiboard.gov.bd/esif/ajax/get_result.php"
        params = {
            "exam": exam,
            "exam_year": year,
            "roll": roll if roll else "",
            "reg": reg if reg else "",
            "board": board_id
        }
        query_string = urllib.parse.urlencode(params)
        full_url = f"{base_url}?{query_string}"

        print(f"\n{YELLOW}Fetching result...{RESET}")
        
        # Fetch the result
        with urllib.request.urlopen(full_url, timeout=10) as response:
            result = response.read().decode().strip()

            if result:
                try:
                    parsed = json.loads(result)
                    print(f"\n{GREEN}Result found:{RESET}")
                    
                    # Format the result for better readability
                    if isinstance(parsed, dict):
                        # Extract student information
                        if "name" in parsed:
                            print(f"{GREEN}Name: {RESET}{parsed.get('name', 'N/A')}")
                        if "roll" in parsed:
                            print(f"{GREEN}Roll: {RESET}{parsed.get('roll', 'N/A')}")
                        if "reg" in parsed:
                            print(f"{GREEN}Registration: {RESET}{parsed.get('reg', 'N/A')}")
                        if "father" in parsed:
                            print(f"{GREEN}Father's Name: {RESET}{parsed.get('father', 'N/A')}")
                        if "mother" in parsed:
                            print(f"{GREEN}Mother's Name: {RESET}{parsed.get('mother', 'N/A')}")
                        if "institute" in parsed:
                            print(f"{GREEN}Institute: {RESET}{parsed.get('institute', 'N/A')}")
                        if "gpa" in parsed:
                            print(f"{GREEN}GPA: {RESET}{parsed.get('gpa', 'N/A')}")
                        if "result" in parsed:
                            print(f"{GREEN}Result: {RESET}{parsed.get('result', 'N/A')}")
                        
                        # Show detailed subject results if available
                        if "subjects" in parsed and isinstance(parsed["subjects"], dict):
                            print(f"\n{GREEN}Subject Results:{RESET}")
                            for subject, details in parsed["subjects"].items():
                                if isinstance(details, dict):
                                    grade = details.get("grade", "N/A")
                                    point = details.get("point", "N/A")
                                    print(f"{GREEN}{subject}: {RESET}Grade: {grade}, Point: {point}")
                                else:
                                    print(f"{GREEN}{subject}: {RESET}{details}")
                        
                        # Display raw JSON for debugging
                        print(f"\n{BLUE}Raw Data:{RESET}")
                        print(f"{YELLOW}{json.dumps(parsed, indent=2, ensure_ascii=False)}{RESET}")
                    else:
                        # Just print the parsed result if it's not a dict
                        print(f"{YELLOW}{json.dumps(parsed, indent=2, ensure_ascii=False)}{RESET}")
                        
                except json.JSONDecodeError:
                    print(f"{RED}Invalid response from the server.{RESET}")
                    print(result)
            else:
                print(f"{RED}No result found for the provided information.{RESET}")
    except Exception as e:
        print(f"{RED}An error occurred. Check your connection or input.{RESET}")

# Main loop
while True:
    get_result()
    print(f"\n{BLUE}(Press Enter to check another result, or type 'n' to exit){RESET}")
    again = input(f"{CYAN}Check another result? [Y/n]: {RESET}").strip().lower()
    if again == 'n' or again == 'no':
        print(f"{GREEN}Thank you for using the result checker!{RESET}")
        break