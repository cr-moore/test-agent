import asyncio

from agent_loop import test_gen_loop
from util.read_test_file import read_test_file

TEST_FILE_PATH = '../test.txt'
SUCCESS_INDICATOR = 'success'

def main():
    
    # get test
    test = read_test_file(TEST_FILE_PATH)
    print(test)

    # run agent loop
    final_agent_message = asyncio.run(test_gen_loop(test['website'], test['instructions']))
    status = final_agent_message.split('\n')[-1]

    if SUCCESS_INDICATOR in status.lower():
        print("\033[32mTest Passed\033[0m")
    else:
        print("\033[31mTest Failed\033[0m")

if __name__ == "__main__":
    main()