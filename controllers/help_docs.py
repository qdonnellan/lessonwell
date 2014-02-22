from models.helpDocs import HelpDocs

def get_docs(category):
    '''
    get all of the help docs
    '''
    docs = HelpDocs.query(HelpDocs.category == category).order(HelpDocs.title)
    return docs

def get_doc_by_id(docID):
    '''
    get a particular help doc given it's id
    '''
    if docID is None:
        return None
    elif not str(docID).isdigit():
        raise NameError("Invalid doc identifier")
    else:
        theKey = ndb.Key(HelpDocs, int(docID))
        return theKey.get()

def edit_doc_by_id(title, content, docID):
    '''
    edit an existing help doc
    '''
    doc = get_doc_by_id(docID)
    if doc is not None:
        doc.title = title       
        doc.body = content
        key = doc.put()

def newDoc(category, content, title):
    '''
    create a new help doc
    '''
    newDoc = HelpDocs(category = category, body = content, title = title)
    key = newDoc.put()
    return key.id()