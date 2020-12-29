import json


class Setting(object):
    path = '/home/summus/script/python-script/ui/config.json'

    def __init__(self):
        with open(Setting.path, 'r') as config_file:
            settings = json.load(config_file)

        self.current_function = settings['current_function']
        self.function_setting_records = list(
            map(
                lambda x: FunctionSettingRecord(
                    x['function_type'], x['output_path'], x['input_content'], x['output_content']),
                settings['function_setting_records']))

    def set_function_type(self, function_type):
        self.current_function = function_type

    def get_function_type(self):
        return self.current_function

    def save_config(self):
        with open(Setting.path, 'w') as config_file:
            json.dump(self, config_file, indent=4, sort_keys=True, default=lambda obj: obj.__dict__)

    def get_record(self, function_type):
        matched_records = list(
            filter(lambda x: x.function_type == function_type, self.function_setting_records))
        if len(matched_records) > 0:
            return matched_records[0]
        else:
            return None

    def get_current_record(self):
        return self.get_record(self.current_function)

    def set_setting_record(self, function_type, target_record):
        for i, record in enumerate(self.function_setting_records):
            if record.function_type == function_type:
                self.function_setting_records[i] = target_record
                break
        else:
            self.function_setting_records.append(target_record)


class FunctionSettingRecord(object):
    def __init__(self, function_type, output_path, input_content, output_content):
        self.function_type = function_type
        self.output_path = output_path
        self.input_content = input_content
        self.output_content = output_content


if __name__ == '__main__':
    setting = Setting()
    print(setting.current_function)
    setting.current_function = 2
    setting.function_setting_records[0].function_type = 3
    setting.save_config()
