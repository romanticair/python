import codecs
import time


class DataOutput:
    def __init__(self):
        self.filepath = 'baike_%s.html' % time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime())
        self.output_head(self.filepath)
        self.data = []

    def store_data(self, data):
        if data is None:
            return
        self.data.append(data)
        if len(self.data) > 10:
            self.output_html(self.filepath)

    def output_head(self, path):
        """
        将HTML头写进去
        :param path:
        :return:
        """
        fout = codecs.open(path, 'w', encoding='utf-8')
        fout.write('<html>')
        fout.write('<body>')
        fout.write('<table>')
        fout.close()

    def output_html(self, path):
        """
        将数据写入HTML文件中
        :param path: 文件路径
        :return:
        """
        fout = codecs.open(path, 'w', encoding='utf-8')
        for data in self.data:
            fout.write('<tr>')
            fout.write('<td>%s<td>' % data['url'])
            fout.write('<td>%s<td>' % data['title'])
            fout.write('<td>%s<td>' % data['summary'])
            fout.write('</tr>')
            self.data.remove(data)
        fout.close()

    def output_end(self, path):
        """
        输出HTML结束
        :param path: 文件存储路径
        :return:
        """
        fout = codecs.open(path, 'w', encoding='utf-8')
        fout.write('</html>')
        fout.write('</body>')
        fout.write('</table>')
        fout.close()
