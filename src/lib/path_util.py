
class PathHelper:
    def __init__(self, data_dir):
        self.data_dir = data_dir

    def get_data_file(self):
        return "%s/data.txt" % self.data_dir

    def get_latest_data_file(self):
        return "%s/latest.txt" % self.data_dir

    def get_most_viewed_data_file(self):
        return "%s/most_viewed.txt" % self.data_dir

    def get_skip_file(self):
        return "%s/skip.txt" % self.data_dir
