from stix_shifter_utils.modules.base.stix_translation.base_results_translator import BaseResultTranslator
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import json_to_stix_translator
from os import path
import json


class ResultTranslator(BaseResultTranslator):

    def __init__(self, options, dialect):
        super().__init__(options, dialect, path.dirname(__file__))

    def translate_results(self, data_source, data):
        """
        Translates JSON data into STIX results based on a mapping file
        :param data: JSON formatted data to translate into STIX format
        :type data: str
        :param mapping: The mapping file path to use as instructions on how to translate the given JSON data to STIX.
            Defaults the path to whatever is passed into the constructor for JSONToSTIX (This should be the to_stix_map.json in the module's json directory)
        :type mapping: str (filepath)
        :return: STIX formatted results
        :rtype: str
        """

        json_data = json.loads(data)
        data_source = json.loads(data_source)

        results = json_to_stix_translator.convert_to_stix(data_source, self.map_data, json_data, self.transformers, self.options)

        if len(results['objects']) - 1 == len(json_data):
            for i in range(1, len(results['objects'])):
                results['objects'][i]['number_observed'] = 1
        else:
            raise RuntimeError("Incorrect number of result objects after translation. Found: {}, expected: {}.".format(len(results['objects']) - 1, len(json_data)))

        return results
