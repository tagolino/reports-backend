import jmespath
from jmespath import functions


class CustomFunctions(functions.Functions):
    @functions.signature({"types": ["string"]}, {"types": ["array"]})
    def _func_custom_join(self, separator, array):
        non_empty_strings = [s for s in array if s is not None and s != ""]

        return separator.join(non_empty_strings)

    @functions.signature({"types": ["number", "string"]})
    def _func_percentage(self, percentage):
        return "{:.0f}%".format(float(percentage) * 100)


options = jmespath.Options(custom_functions=CustomFunctions())


def search(expression, json_data):
    return jmespath.search(expression, json_data, options=options)
