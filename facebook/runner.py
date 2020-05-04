import os
from analyzer import FbMessageAnalyzer
from utils import MarkdownGenerator


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), 'data')

    with open('stopwords.txt', 'r', encoding='utf-8') as f:
        stopwords = f.read().split('\n')

    analyzer = FbMessageAnalyzer(lang='eng', stopwords=stopwords)
    analyzer.load_json_in_dir(path=path)
    analyzer.parse_data(rm_stopword=True, max_num=10)

    senders = analyzer.senders
    freq_words = analyzer.freq_words
    sender_freq_words = analyzer.sender_freq_words

    analyzer.make_graphs(time_series='time_series.png',
                         sender_ratio='message_ratio.png')

    md = MarkdownGenerator(title='Message analysis')
    md.add_text('## Message ratio')
    md.add_image('message_ratio.png')
    md.add_text('## Messages over time')
    md.add_image('time_series.png')

    md.add_text('## Frequent words')
    md.add_table(freq_words)

    for sender in senders:
        sender_words = sender_freq_words[sender]
        md.add_text(f'## {sender}\'s frequent words')
        md.add_table(sender_words)

    md.write('sample.md')
