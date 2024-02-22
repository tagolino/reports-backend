import jmespath
from jmespath import functions


class CustomFunctions(functions.Functions):
    @functions.signature({"types": ["string"]}, {"types": ["array"]})
    def _func_custom_join(self, separator, array):
        non_empty_strings = [
            str(item) for item in array if item is not None and item != ""
        ]

        return separator.join(non_empty_strings)

    @functions.signature({"types": ["number", "string"]})
    def _func_percentage(self, percentage):
        return "{:.0f}%".format(float(percentage) * 100)

    @functions.signature(
        {"types": ["number", "string"]},
        {"types": ["string"]},
        {"types": ["string"]},
    )
    def _func_substring(self, value, start, end):
        return str(value)[int(start) : int(end)]


options = jmespath.Options(custom_functions=CustomFunctions())


def search(expression, json_data):
    return jmespath.search(expression, json_data, options=options)
