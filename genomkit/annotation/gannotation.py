class GAnnotation:
    def __init__(self, file_path, file_format):
        self.file_path = file_path
        self.file_format = file_format.lower()
        self.genes = {}
        self.transcripts = {}
        self.exons = {}
        self.load_data()

    def load_data(self):
        with open(self.file_path, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                fields = line.strip().split('\t')
                if self.file_format == 'gtf':
                    feature_type = fields[2]
                    attributes = dict(item.strip().split(' ')
                                      for item in fields[8].split(';')
                                      if item.strip())
                elif self.file_format == 'gff':
                    feature_type = fields[2]
                    attributes = dict(item.strip().split('=')
                                      for item in fields[8].split(';')
                                      if item.strip())
                else:
                    raise ValueError("Invalid file format. "
                                     "Supported formats are 'gtf' and 'gff'.")

                if feature_type == 'gene':
                    gene_id = attributes['gene_id'].strip('"')
                    self.genes[gene_id] = {
                        'chr': fields[0],
                        'start': int(fields[3]),
                        'end': int(fields[4]),
                        'strand': fields[6],
                        'gene_name': attributes.get('gene_name', ''),
                        'gene_type': attributes.get('gene_type', '')
                    }
                elif feature_type == 'transcript':
                    transcript_id = attributes['transcript_id'].strip('"')
                    gene_id = attributes['gene_id'].strip('"')
                    self.transcripts[transcript_id] = {
                        'gene_id': gene_id,
                        'chr': fields[0],
                        'start': int(fields[3]),
                        'end': int(fields[4]),
                        'strand': fields[6],
                        'transcript_type':
                            attributes.get('transcript_type', '')
                    }
                    if gene_id in self.genes:
                        self.genes[gene_id].setdefault(
                            'transcripts', set()).add(transcript_id)
                elif feature_type == 'exon':
                    exon_id = attributes['exon_id'].strip('"')
                    transcript_id = attributes['transcript_id'].strip('"')
                    self.exons[exon_id] = {
                        'transcript_id': transcript_id,
                        'chr': fields[0],
                        'start': int(fields[3]),
                        'end': int(fields[4]),
                        'strand': fields[6]
                    }
                    if transcript_id in self.transcripts:
                        self.transcripts[transcript_id].setdefault(
                            'exons', set()).add(exon_id)

    def get_gene(self, gene_id):
        return self.genes.get(gene_id)

    def get_gene_names(self):
        gene_names = [gene_info['gene_name']
                      for gene_info in self.genes.values()
                      if gene_info.get('gene_name')]
        return gene_names

    def get_gene_ids(self):
        gene_ids = list(self.genes.keys())
        return gene_ids

    def get_transcript(self, transcript_id):
        return self.transcripts.get(transcript_id)

    def get_exon(self, exon_id):
        return self.exons.get(exon_id)

    def get_transcript_ids(self):
        transcript_ids = list(self.transcripts.keys())
        return transcript_ids

    def get_exon_ids(self):
        exon_ids = list(self.exons.keys())
        return exon_ids

    def filter_elements(self, element_type, attribute=None, value=None):
        """
        Filter elements (genes, transcripts, exons) based on attribute
        criteria.

        :param element_type: Type of elements to filter ('gene', 'transcript',
                             'exon').
        :param attribute: Attribute to filter on (e.g., 'biotype').
        :param value: Value of the attribute to filter on.
        :return: List of filtered elements.
        """
        filtered_elements = []
        if element_type == 'gene':
            elements = self.genes.values()
        elif element_type == 'transcript':
            elements = self.transcripts.values()
        elif element_type == 'exon':
            elements = self.exons.values()
        else:
            raise ValueError("Invalid element type. Supported types are"
                             "'gene', 'transcript', 'exon'.")
        for element in elements:
            if attribute and value:
                if attribute in element and element[attribute] == value:
                    filtered_elements.append(element)
            else:
                filtered_elements.append(element)
        return filtered_elements

    def entries2GRegions(self, entries):
        