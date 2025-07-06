import yamale

def validate_yaml(schema_yaml, data_yaml):
    schema = yamale.make_schema(schema_yaml)
    data = yamale.make_data(data_yaml)

    # 执行验证
    try:
        yamale.validate(schema, data)
        print("配置验证通过！")
    except yamale.YamaleError as e:
        print("配置错误：")
        for result in e.results:
            print(f"文件: {result.data}")
            for error in result.errors:
                print(f"  - {error}")
    except Exception as e:
        print(str(e))