from analyzer import FbMessageAnalyzer

if __name__ == "__main__":
    import os
    json_path = os.path.join(os.getcwd(), 'data')
    output_name = 'facebook.md'

    analyzer = FbMessageAnalyzer()
    analyzer.parse_data(path=json_path)
    analyzer.write_markdown(file_name=output_name)

    raise NotImplementedError
