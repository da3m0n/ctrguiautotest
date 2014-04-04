class Part(object):
    def __init__(self, code="p", content=None, style=None, id=None, attributes=None):
        self.style = style
        self.id = id
        self.pieces = []
        self.code = code
        if attributes is None:
            self.attributes = {}
        else:
            self.attributes = attributes
        if isinstance(content, list):
            self.addPieces(content)
        elif content is not None:
            self.addPiece(content)

    def addPiece(self, thePart):
        self.pieces.append(thePart)

    def addPieces(self, theParts):
        for part in theParts:
            self.addPiece(part)

    def addAttribute(self, attributename, attributevalue):
        self.attributes[attributename] = attributevalue

    def addPart(self, code='p', content=None, style=None, id=None, attributes=None):
        newPart = Part(code, content, style, id, attributes)
        self.addPiece(newPart)

    def make(self, tab="\t"):
        startHTML = '<' + self.code

        if self.attributes:
            for attribute in self.attributes:
                content = self.attributes[attribute]
                if content is None:
                    startHTML += ' ' + attribute
                else:
                    startHTML += ' ' + attribute + '="' + str(content) + '"'

        if self.style:
            startHTML += ' class="' + self.style + '"'

        if self.id:
            startHTML += ' id="' + self.id + '"'

        if self.pieces:
            startHTML += '>'

            partItems = [startHTML]

            if len(self.pieces) > 1:
                sep = "\n" + tab
                finalSep = sep[:-1]
                newtab = tab + "\t"
            else:
                newtab = tab
                sep = ""
                finalSep = ""

            for piece in self.pieces:
                if isinstance(piece, str):
                    partItems.append(piece)
                elif isinstance(piece, int) or isinstance(piece, float):
                    partItems.append(str(piece))
                elif piece is None:
                    partItems.append("")
                else:
                    partItems.append(piece.make(newtab))

            code = sep.join(partItems)
            code += finalSep + '</' + self.code + '>'
            return code

        else:
            startHTML += ' />'
            return startHTML