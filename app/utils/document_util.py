from app.database import Database
from app.models.pdv import Pdv
from pycpfcnpj import cpfcnpj

class DocumentUtil:
    def document_is_unique(self, document):
        document = self.format_document(document)
        mongodb = Database().get_connection()
        if Pdv.objects(document=document).count() > 0:
            return False
        return True

    def document_is_valid(self, document):
        document = self.format_document(document)
        for number in document:
            if number.isalpha():
                return False

        validate = cpfcnpj.validate(document)
        return validate

    def format_document(self, document):
        document = document.replace('.', '')
        document = document.replace('/', '')
        document = document.replace('-', '')
        return document
