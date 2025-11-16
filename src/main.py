import asyncio

from loops.agent_loop import test_gen_loop, PromptType
from util.read_test_file import read_test_file

PLAN_FILE_PATH = '../plan.txt'
TEST_FILE_PATH = '../test.txt'
SUCCESS_INDICATOR = 'success'

def display_menu():
    """Display menu and get user selection"""
    print("\n" + "="*50)
    print("Test Agent Menu")
    print("="*50)
    print("1) Generate Test Plan")
    print("2) Generate Test Script")
    print("="*50)
    
    while True:
        choice = input("\nSelect an option (1 or 2): ").strip()
        if choice in ['1', '2']:
            return choice
        print("Invalid selection. Please enter 1 or 2.")

def main():
    """Entry point for the test agent. Displays menu and runs selected test mode."""
    choice = display_menu()
    
    if choice == '1':
        print("\n[Generating Test Plan...]")
        
        test = read_test_file(PLAN_FILE_PATH)
        
        final_agent_message = asyncio.run(test_gen_loop(
            test['website'], 
            test['instructions'],
            prompt_type=PromptType.PLAN
        ))
        status = final_agent_message.split('\n')[-1]

        if SUCCESS_INDICATOR in status.lower():
            print("\033[32mTest Plan Generation Passed\033[0m")
        else:
            print("\033[31mTest Plan Generation Failed\033[0m")
            
    elif choice == '2':
        print("\n[Generating Test Script...]")

        test = read_test_file(TEST_FILE_PATH)

        final_agent_message = asyncio.run(test_gen_loop(
            test['website'], 
            test['instructions'],
            prompt_type=PromptType.SCRIPT
        ))
        status = final_agent_message.split('\n')[-1]

        if SUCCESS_INDICATOR in status.lower():
            print("\033[32mTest Passed\033[0m")
        else:
            print("\033[31mTest Failed\033[0m")

if __name__ == "__main__":
    main()