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
    parser.add_argument('-u', '--url', type=str, help='Url where you want to find XSS', required=True)
    parser.add_argument('-a', '--affects', type=str, help='Url which could be affected by an XSS', required=False)
    #parser.add_argument('-d', '--display', action='store_true', help='Display the browser', required=False)

    args = parser.parse_args()

    return args.url, args.affects, False#args.display


def get_params(url, affected):
    method = int(input("""
Choose the attack method:
[1] - AUTO
[2] - MANUAL
          
->"""))
    
    if method == 2:
        config = {}
        config['url'] = url
        config['affects'] = affected
        config['vector'] = {}
        By_possibilities_index = int(input(f"""
How to locate the vector ?
[0] - In cookies
{By_possibilities_str}
[9] - In URL
->"""))
        
        if By_possibilities_index != 0 and By_possibilities_index != 9:
            config['vector']['isCookies'] = False
            config['vector']['by'] = By_possibilities[By_possibilities_index-1]
        
        elif By_possibilities_index == 0:
            # if the vector is a cookie param, we dont need to know how to locate it in the DOM and to fill a form
            # we only need to know the name of the cookie param
            config['vector']['isCookies'] = True

        config['vector']['name'] = input("""
Enter the name of the vector (id name, or class name, etc..., depending on the method you chose):
->""")
        
        # if there are some other inputs to fill in the form in order to correctly send the payload
        misc_inputs = {}
        print("\nNow you can add other needed inputs for the request")
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
            config['submit']['by'] = By_possibilities[submit_By-1]
            config['submit']['name'] = input("""
Enter the name of the submit button (id name, or class name, etc..., depending on the method you chose):
->""")
            
        return config

    return 


def config_already_exists(url, affects):
    hash = xxhash.xxh64(f"{url}{affects}").hexdigest()
    file_path = f"saved_configs/{hash}.yaml"
    if os.path.exists(file_path):
        return True, file_path

    return False, file_path


def save_config(url, affects, config):
    hash = xxhash.xxh64(f"{url}{affects}").hexdigest()
    path = f"saved_configs/{hash}.yaml"
    with open(path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

    return path


def get_config(path):
    with open(path, 'r') as file:
        config = yaml.safe_load(file)

    return config


def add_attack_types_to_config(path, attack_types):
    config = get_config(path)
    config['attack_types'] = attack_types
    with open(path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)


def print_config(config):
    first = True
    print("="*60)
    for k, v in config.items():
        print("-"*60)
        print(f"{k}: {v}")
    
    print("-"*60)
    print("="*60)
