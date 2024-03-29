"""数据存储器"""
import codecs


class DataOutput:
    def __init__(self):
        self.data = []

    def store_data(self, data):
        if data in None:
            return
        self.data.append(data)

    def output_html(self):
        fout = codecs.open('baike.html', 'w', encoding='utf-8')
        fout.write('<html>')
        fout.write('<body>')
        fout.write('<table>')
        for data in self.data:
            fout.write('<tr>')
            fout.write('<td>%s<td>' % data['url'])
            fout.write('<td>%s<td>' % data['title'])
            fout.write('<td>%s<td>' % data['summary'])
            fout.write('</tr>')
            self.data.remove(data)
        fout.write('</html>')
        fout.write('</body>')
        fout.write('</table>')
        fout.close()
