import os
import json
import re
from modules.monitoring_handler import MonitoringHandler
from modules.utils import getValue

class Handler(MonitoringHandler):
    def __init__(self, config):
        self.initConfig(config)
        self.specific_words_pattern = re.sub("_", " ", "---Specific_Words---")

        self.source_file = getValue(config['monitoring'], 'source', None)

        if not self.source_file:
            raise Exception("source file is not defined")

        self.getLastdata()

        if self.initial_check:
            self.setMonitoringFile()
            self.check()

        if self.report:
            self.drain_handler.report(self.name)

        self.initial_complete_flag = True

    def setMonitoringFile(self):
        training_json = None

        try:
            with open(self.source_file, 'r', encoding='UTF8') as f:
                training_json = json.load(f)
        except:
            raise Exception("source file is not exist")
        
        cluster_json = training_json["id_to_cluster"]["_Cache__data"]
        cluster_list = list()
        cluster_id_list = list()
        for values in cluster_json.values():
            cluster_id = values["cluster_id"]
            cluster_size = values["size"]

            cluster_tokens = values["log_template_tokens"]["py/tuple"]
            cluster_tokens_str = f"{' '.join(cluster_tokens)}"
            cluster_tokens_id_str = f"{cluster_id}({cluster_size}): {' '.join(cluster_tokens)}"


            if cluster_tokens_str[:len(self.specific_words_pattern)] != self.specific_words_pattern:
                cluster_list.append(cluster_tokens_str)
                cluster_id_list.append(cluster_tokens_id_str)

        self.file_fullpath = os.path.dirname(os.path.abspath(__file__))
        filename = self.monitoring_file
        self.monitoring_filename = f"{self.monitoring_directory}\\{filename}.{self.monitoring_extension}"
        self.monitoring_id_filename = f"{self.monitoring_directory}\\{filename}_id.{self.monitoring_extension}"

        try:
            with open(self.monitoring_filename, 'w', encoding='UTF8') as f:
                f.write("\n".join(cluster_list))
        except:
            raise Exception("source file is not exist")

        try:
            with open(self.monitoring_id_filename, 'w', encoding='UTF8') as f:
                f.write("\n".join(cluster_id_list))
        except:
            raise Exception("source file is not exist")



def recursive_training_data_check(config):
    handler = Handler(config)
