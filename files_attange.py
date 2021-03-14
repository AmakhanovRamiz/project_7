
class SortingZip:

    def __init__(self, file_name, result_file_name):
        self.file_name = file_name
        self.result_file_name = result_file_name
        self.result_dir_path = None

    def unzip(self):
        zfile = zipfile.ZipFile(self.file_name, 'r')
        for z_item in zfile.infolist():
            zfile.extract(z_item)
            date_time = time.mktime(z_item.date_time + (0, 0, -1))
            os.utime(z_item.filename, (date_time, date_time))
        self.file_name = os.path.splitext(self.file_name)[0]
        zfile.close()

    def create_result_dir(self):
        dirpath = os.path.dirname(__file__)
        self.result_dir_path = os.path.join(dirpath, self.result_file_name)
        os.mkdir(self.result_dir_path)

    def iterate_files(self):
        dirpath = os.path.dirname(__file__)
        current_path = os.path.join(dirpath, self.file_name)
        for dirpath, dirname, filenames in os.walk(current_path):
            if filenames:
                for file in filenames:
                    path_of_file = os.path.join(dirpath, str(file))
                    modified = self._check_data(dirpath, file)
                    year_path = self._create_year_dir(modified)
                    month_path = self._create_month_dir(modified, year_path)
                    self._move_file(from_path=path_of_file, to_path=month_path)

    def _check_data(self, dirpath, filename):
        file_path = os.path.join(dirpath, filename)
        modified = time.gmtime(os.path.getmtime(file_path))
        return modified

    def _create_year_dir(self, modified):
        year_path = os.path.join(self.result_dir_path, str(modified.tm_year))
        if not os.path.exists(year_path):
            os.mkdir(year_path)
        return year_path

    def _create_month_dir(self, modified, year_path):
        month_path = os.path.join(year_path, str(modified.tm_mon))
        if not os.path.exists(month_path):
            os.mkdir(month_path)
        return month_path

    def _move_file(self, from_path, to_path):
        shutil.copy2(from_path, to_path)


# test = SortingZip('icons.zip', 'icons_by_year')
# test.create_result_dir()
# test.unzip()
# test.iterate_files()