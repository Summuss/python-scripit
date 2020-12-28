import os
import argparse
from util.string_util import StrUtil
from util.string_util import StrLinesPool
from string import Template


def read_input():
    return """
        sex
          1	男    
        2	女
        9	未知

    """


def read_template():
    return """
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;
import com.karrytech.ktcc.client.core.beans.BizException;
import com.karrytech.ktcc.client.core.util.TextUtil;
import lombok.AllArgsConstructor;
import lombok.NonNull;


import java.util.Arrays;

@AllArgsConstructor
public enum $CodeMstrName implements CodeMstrMethod{
$enum_instances

  private  final String code;
  private  final String desc;

  @JsonValue
  @Override
  public String code() {
    return this.code;
  }

  @Override
  public String desc() {
    return this.desc;
  }

  @JsonCreator
  public static $CodeMstrName codeOf(String code) {
    if(code == null){
        return null;
    }
    return Arrays.stream($CodeMstrName.values())
        .filter(codeMstr-> codeMstr.code.equals(code))
        .findFirst()
        .orElseThrow(() -> new BizException("$CodeMstrName 不存在code为\"" + code + "\"的实例"));
  }

  public static $CodeMstrName descOf(String desc) {
    if(desc == null){
        return null;
    }

    return Arrays.stream($CodeMstrName.values())
        .filter(codeMstr-> codeMstr.desc.equals(desc))
        .findFirst()
        .orElseThrow(() -> new BizException("$CodeMstrName 不存在desc为\"" + desc+ "\"的实例"));
  }

  public static $CodeMstrName parse( String value) {
    if (TextUtil.isBlank(value)){
      return null;
    }
    return Arrays.stream($CodeMstrName.values())
            .filter(codeMstr-> codeMstr.desc.equals(value)||codeMstr.code.equals(value))
            .findFirst()
            .orElseThrow(RuntimeException::new);
  }
}    """


def generate_java_enum(input_text, output_path):
    lines_pool = StrLinesPool(input_text)
    params = dict()
    if lines_pool.has_next():
        params['CodeMstrName'] = str.strip(lines_pool.get_line())
    else:
        raise RuntimeError
    entries = []
    while lines_pool.has_next():
        line = lines_pool.get_line()
        arg_list = StrUtil.split_omit_empty('\t', line)
        if len(arg_list) == 2:
            entries.append(
                {
                    'name': params['CodeMstrName'] + '_' + arg_list[0],
                    'code': arg_list[0],
                    'desc': arg_list[1]
                })
        else:
            raise RuntimeError
    enum_instances = '\n'.join(list(map(lambda entry: '{name}("{code}", "{desc}");'.format(**entry), entries)))
    params['enum_instances'] = StrUtil.indent(enum_instances, 1, 2)
    result = Template(read_template()).substitute(**params)

    with open(os.path.join(output_path, params['CodeMstrName'] + '.java'), 'w') as target_file:
        target_file.write(result)

    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='生成Java枚举类')
    parser.add_argument('--input_file_path', '-i', help='输入文件路径', required=True)
    parser.add_argument('--output_file_path', '-o', help='输出文件路径', required=True)
    args = parser.parse_args()

    input_text = ''
    input_file_path = args.input_file_path
    output_file_path = args.output_file_path

    if os.path.isfile(input_file_path):
        with open(input_file_path) as input_file:
            input_text = input_file.read()
    else:
        print('"%s" is not a file!' % os.path.abspath(input_file_path))
        exit(-1)

    if not os.path.isdir(output_file_path):
        print('"%s" is not a dictionary!' % os.path.abspath(output_file_path))
        exit(-1)

    result = generate_java_enum(input_text, output_file_path)

    print(result)
