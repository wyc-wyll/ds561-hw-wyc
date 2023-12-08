import apache_beam as beam
from apache_beam.io import fileio
from apache_beam.options.pipeline_options import PipelineOptions


class ExtractOutgoingLinkCount(beam.DoFn):
    result = 0
    def process(self, element):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(element[1], 'html.parser')
        links = soup.find_all('a')
        yield (element[0], len(links))

class ExtractIncomingLinkCount(beam.DoFn):
    def process(self, element):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(element, 'html.parser')
        links = soup.find_all('a')
        for i in links:
            yield (i.get('href'), 1)

class MyOptions(PipelineOptions):
    @classmethod
    # Define a custom pipeline option that specfies the Cloud Storage bucket.
    def _add_argparse_args(cls, parser):
        parser.add_argument("--output1", required=True)
        parser.add_argument("--output2", required=True)

options = MyOptions()

def run():
    with beam.Pipeline(options=options) as pipe:
        getContent = pipe | 'Read From Google Cloud Storage Bucket' >> fileio.MatchFiles("gs://hw2-ds561/*.html")
        content = getContent | 'Reading Content' >> fileio.ReadMatches()
        htmlContent = content | 'Converting to (Filename, HTML Content)' >> beam.Map(lambda x: (x.metadata.path.split('/')[-1], x.read_utf8()))
        
        pureHtmlContent = content | 'Converting to HTML content' >> beam.Map(lambda x: x.read_utf8())
        

        countingOut = htmlContent | 'Getting outgoing count' >> beam.ParDo(ExtractOutgoingLinkCount())
        countOutResult = countingOut | 'Extracting top 5 outgoing' >> beam.combiners.Top.Of(5, key=lambda x: x[1])
        countOutResult | 'Output outgoing results' >> beam.io.WriteToText(options.output1, file_name_suffix=".txt")

        countingInS1 = pureHtmlContent | 'Getting incoming count' >> beam.ParDo(ExtractIncomingLinkCount())
        summed_countIn = countingInS1 | 'Summing Up The Incoming Count' >> beam.CombinePerKey(sum)
        countInResult = summed_countIn | 'Extracting top 5 incoming' >> beam.combiners.Top.Of(5, key=lambda x: x[1])
        countInResult | 'Output incoming results' >> beam.io.WriteToText(options.output2, file_name_suffix=".txt")



    # print(options._all_options)

    # blob = bucket.blob('gs://hw2-ds561/1.html')
    # text = blob.download_as_text()
    # print(text)

if __name__ == '__main__':
    run()


