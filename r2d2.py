# PEP 257 -- docstring conventions
#
# Use tripple double quotes;
# No space between quotes and docstring;
# No blank line either before or after single line docstrings;
# The summary line may apear on the same line of the opening docstrings;
# Insert blank line after class docstring;
# Insert blank line between methods in class;

# Standard python packages
import os
import jinja2
import yaml
# Custom python modules
import filters
# Temporary imports
from pdb import set_trace as st

class TemplateManager(object):
    """Provides the methods to manage the template files"""

    def __init__(self):
        """Constructor"""
        # The path to the Loader should be configurable
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader('./'),
            trim_blocks=True, lstrip_blocks=True,
            extensions=[],
            undefined=jinja2.DebugUndefined
            )

    def load_template(self, template):
        """Loads Jinja2 template file and returns a Jinja2 object"""
        return self.env.get_template(template)

    def render_template(self, data):
        """Read template file"""
        return print(template.render(data))

    def load_yaml_file(self, file_name):
        """Loads given YAML file and returns a dictionary"""
        with open(file_name) as file:
            try:
               return yaml.safe_load(file)
            except yaml.YAMLError as exception:
                print(exception)

    def display_yaml_dict(self, dict, style='yaml'):
        """Render YAML content to screen

        If style is False, the contents will be displayed in yaml
        format and in dictionaty format if style is True.
        It seems to display the dictionary keys alphabeticaly.
        """
        if style=='yaml':
            style=False
        else:
            style=True
        print(yaml.dump(dict, default_flow_style=style))

    def write_yaml_to_file(self, dict):
        """Writes dict to yaml file"""
        with open('data.yaml', 'w') as file:
            yaml.dump(dict, file)

    def _dict_merge(self, d1, d2):
        """Merge two dictionaries

        Update two dicts of dicts recursively, if either mapping has
        leaves that are non-dicts, the second's leaf overwrites the first's.
        """
        for k, v in d1.items():
            if k in d2:
                if all(isinstance(e, MutableMapping) for e in (v, d2[k])):
                    d2[k] = self._dict_merge(v, d2[k])
        d3 = d1.copy()
        d3.update(d2)
        return d3

if __name__ == "__main__":
    obj = TemplateManager()
    # Simple dictionary for testing purpose
    dict = {
        'os': 'ubuntu',
        'gcc': {'version': '9.3.0', 'architcture': 'core-avx512'}
    }

    # Displays dict in yaml format
    obj.display_yaml_dict(dict)
    # Writes dict to yaml file
    obj.write_yaml_to_file(dict)
    # Loads an yaml file
    data = obj.load_yaml_file('syrah.yaml')
    # Displays the data as it is returned by the yaml.safe_load method
    print(data)
    # Displays the data using yaml structure
    obj.display_yaml_dict(data)
    template = obj.load_template('spack.yaml.j2')
    # Print rendered template
    obj.render_template(data)
    exit(0)
