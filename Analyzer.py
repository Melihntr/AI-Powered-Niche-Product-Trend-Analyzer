from collections import Counter
class Analyzer:
    def __init__(self, data):
        self.data = data

    def analyze_trends(self):
        words = []
        for item in self.data:
            words.extend(item.split())
        return Counter(words).most_common(10)