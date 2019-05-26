class ParserError(ValueError):
    """
    Exception raised when syntax errors are encountered parsing PugSQL files.
    """
    def __init__(self, message, token):
        super(ParserError, self).__init__(
            'Error in %s:%s:%s - %s' % (
                token.context.sqlfile,
                token.context.line,
                token.context.col,
                message))
        self.token = token
