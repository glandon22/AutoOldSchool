import shutil
import copy
import os

plugin_name = 'glglassblower'
plugin_description = 'blows glass - up to orbs'
# IMPORTANT: plugin must have tag "goonlite" to be loaded into the client!!!!!!!!!!!!!!!!!!!!!!!!!!
plugin_tags = '{"crafting", "glass", "goonlite"}'
script_cmd = 'crafting/blow_glass_v3.py'
'''{
    'key_name': 'fish',
    'key_desc': 'fish to catch',
    'key_position': '1',
    'return_type': 'fishEnum',
    'default_return_value': 'fishEnum.SHRIMP'
}'''
dropdowns_configs = [
]
# NOT IMPLEMENTED YET!!!!!

number_configs = [

]

'''''''''''''''''''''''''''''
 ^^^^^^^^^^^^^^^^^^^^^^^^^^^ALL VARS ABOVE NEED TO BE CONFIGURED FOR EACH PLUGIN! ^^^^^^^^^^^^^^^^^^^^^^^^
'''''

config_items_all = ''
os.mkdir(f'./{plugin_name}')
dest_file_name = f'./{plugin_name}/{plugin_name}Plugin.java'
dest_config_file_name = f'./{plugin_name}/{plugin_name}Config.java'

shutil.copy('./tpl/index', dest_file_name)
shutil.copy('./tpl/config', dest_config_file_name)

number_config_item = '''
    @Range(
            max = $max$
    )
    @ConfigItem(
            keyName = "$key_name$",
            name = "$key_name$",
            description = "$key_desc$",
            position = $key_position$
    )
    default int $key_name$()
    {
        return $key_default$;
    }
'''

dropdown_config_item = '''
    @ConfigItem(
        keyName = "$key_name$",
        name = "$key_name$",
        description = "$key_desc$",
        position = $key_position$
    )
    default $return_type$ $key_name$()
    {
        return $default_return_value$;
    }
'''


def build_dropdown(vars):
    print(vars)
    stub = copy.deepcopy(dropdown_config_item)
    stub = stub.replace('$key_name$', vars['key_name'])
    stub = stub.replace('$key_desc$', vars['key_desc'])
    stub = stub.replace('$key_position$', vars['key_position'])
    stub = stub.replace('$return_type$', vars['return_type'])
    stub = stub.replace('$default_return_value$', vars['default_return_value'])
    return stub


with open(dest_file_name, 'r') as file:
    data = file.read()

    # Searching and replacing the text
    # using the replace() function
    data = data.replace('$plugin_name$', plugin_name)
    data = data.replace('$plugin_description$', plugin_description)
    data = data.replace('$plugin_tags$', plugin_tags)
    data = data.replace('$script_cmd$', script_cmd)

# Opening our text file in write only
# mode to write the replaced content
with open(dest_file_name, 'w') as file:
    # Writing the replaced data in our
    # text file
    file.write(data)


with open(dest_config_file_name, 'r') as file:
    data = file.read()

    # Searching and replacing the text
    # using the replace() function
    data = data.replace('$plugin_name$', plugin_name)
    for item in dropdowns_configs:
        config_items_all += build_dropdown(item)
    data = data.replace('$config_items$', config_items_all)

with open(dest_config_file_name, 'w') as file:
    # Writing the replaced data in our
    # text file
    file.write(data)