import base64 as b64


# Special characters
SPECIAL_CHARS = {
    'plain': ['<', '>', '(', ')', '[', ']', '{', '}', '=', '+', '-', '*', '/', '\\', '|', '&', '^', '%', '$', '#', '@', '!', '~', '`', '?', ':', ';', ',', '.', ' ', '\t', '\n'],
    'encoded': ['&lt;', '&gt;', '&#40;', '&#41;', '&#91;', '&#93;', '&#123;', '&#125;', '&#61;', '&#43;', '&#45;', '&#42;', '&#47;', '&#92;', '&#124;', '&#38;', '&#94;', '&#37;', '&#36;', '&#35;', '&#64;', '&#33;', '&#126;', '&#96;', '&#63;', '&#58;', '&#59;', '&#44;', '&#46;', '&#32;', '&#9;', '&#10;'],
    'url_encoded': ['%3C', '%3E', '%28', '%29', '%5B', '%5D', '%7B', '%7D', '%3D', '%2B', '%2D', '%2A', '%2F', '%5C', '%7C', '%26', '%5E', '%25', '%24', '%23', '%40', '%21', '%7E', '%60', '%3F', '%3A', '%3B', '%2C', '%2E', '%20', '%09', '%0A']
}


# TOUT CHANGER, FAIRE UN DICT AVEC TOUS LES CARACTERES SPECIAUX ET LEURS EQUIVALENTS
# FAIRE UNE FONCTION QUI CONSTRUIT DES ÉQUIVALENTS DE FONCTIONS, EXEMPE: ALERT(ARG) = ATOB(BASE64)

SPECIAL_CHARS['for_html_tags'] = {
    '<': ['<', '&lt;', '%3C'],
    '>': ['>', '&gt;', '%3E'],
    '/': ['/', '&#47;', '%2F']
}

EQUIVALENTS = {
    '<': ['&lt;', '%3C'],
    '>': ['&gt;', '%3E'],
    '/': ['&#47;', '%2F'],
    '"': ['&quot;', '&#34;', '%22'],
    "'": ['&apos;', '&#39;', '%27'],
    '`': ['&#96;', '%60'],
    ')': ['&#41;', '%29'],
    '(': ['&#40;', '%28'],
    ';': ['&#59;', '%3B'],
    ':': ['&#58;', '%3A'],
    ',': ['&#44;', '%2C'],
    '.': ['&#46;', '%2E'],
    '+': ['&#43;', '%2B'],
    '=': ['&#61;', '%3D'],
    ' ': ['&nbsp;', '&#32;', '%20'],
    '&': ['&amp;', '&#38;', '%26'],
    '\\': ['&#92;', '%5C'],
    '\n': ['&#10;', '%0A'],
    '\r': ['&#13;', '%0D'],
    '\t': ['&#9;', '%09'],
}


HTML_TAGS = [
    'html', 'head', 'title', 'base', 'link', 'meta', 'style', 'script', 'noscript',
    'body', 'section', 'nav', 'article', 'aside', 'h1', 'h2', 'h3', 'div', 'a', 
    'data', 'time', 'code', 'span', 'br', 'picture', 'source', 'img', 'iframe', 
    'embed', 'object','video', 'audio', 'input', 'button', 'option', 'textarea', 
    'dialog', 'script','svg'
]

USEFUL_JS_FUNCTION = [
    'alert', 'fetch', 'eval', '[].filter.constructor', 'atob', 'document.write', 'document.writeln', 'document.writeIn', 'document.createElement'
]

        