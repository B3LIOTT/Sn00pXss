from selenium.webdriver.common.by import By
import argparse
import yaml
import xxhash
import os



By_possibilities = [
    By.ID,
    By.NAME,
    By.XPATH,
    By.LINK_TEXT,
    By.PARTIAL_LINK_TEXT,
    By.TAG_NAME,
    By.CLASS_NAME,
    By.CSS_SELECTOR
]


By_possibilities_str = """[1] - By.ID
[2] - By.NAME
[3] - By.XPATH
[4] - By.LINK_TEXT
[5] - By.PARTIAL_LINK_TEXT
[6] - By.TAG_NAME
[7] - By.CLASS_NAME
[8] - By.CSS_SELECTOR"""



def get_args() -> list:
    parser = argparse.ArgumentParser(description='Sn00pXss - XSS detection tool')
    parser.add_argument('-u', '--url', type=str, help='Un argument optionnel', required=True)
    parser.add_argument('-a', '--affects', type=str, help='Url which could be affected by an XSS', required=False)

    args = parser.parse_args()

    return args.url, args.affects


def get_params():
    method = int(input("""
Choose the attack method:
[1] - AUTO
[2] - MANUAL
          
->"""))
    
    if method == 2:
        config = {}
        config['vector'] = {}
        config['vector']['by'] = By_possibilities[int(input(f"""
How to locate the vector ?
{By_possibilities_str}
->"""))]
        
        config['vector']['name'] = input("""
Enter the name of the vector (id name, or class name, etc..., depending on the method you chose):
->""")
        
        misc_inputs = {}
        print("Now you can add onther needed inputs for the request")
        while True:
            misc_input = int(input(f"""
How to locate the input ?
[0] - I don't need to add more inputs
{By_possibilities_str}
->"""))
            if misc_input == 0:
                break

            misc_input = By_possibilities[misc_input-1]

            misc_name = input("""
Enter the name of the input (id name, or class name, etc..., depending on the method you chose):
->""")
            misc_inputs[misc_name] = misc_input

        config['misc_inputs'] = misc_inputs

        submit_By = int(input(f"""
How to locate the submit button ?
[0] - Just need to press ENTER (No submit button, or submit button is not needed)
{By_possibilities_str}
->"""))
        
        if submit_By != 0:
            config['submit'] = {}
            config['submit']['by'] = submit_By
            config['submit']['name'] = input("""
                        Enter the name of the submit button (id name, or class name, etc..., depending on the method you chose):
                        ->""")
            
        return config

    return 


def config_already_exists(url, affects):
    file_path = f"saved_configs/{xxhash.xxh64(f"{url}{affects}").hexdigest()}.yaml"
    if os.path.exists(file_path):
        return True, file_path

    return False, file_path


def save_config(path, params):
    config = {}
    if submit_button:=params[0]:
        # If submit button is needed
        vector_By, vector_name, submit_By, submit_name, misc_inputs = params[1:]
        config
        config['submit_button'] = {
            'By': submit_By,
            'name': submit_name
        }
    else:
        vector_By, vector_name, misc_inputs = params[1:]


def get_config(path):
    with open(path, 'r') as file:
        data = yaml.safe_load(file)

    return data