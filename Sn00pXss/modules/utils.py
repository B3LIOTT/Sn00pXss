# Special characters
SPECIAL_CHARS = {
    'plain': ['<', '>', '(', ')', '[', ']', '{', '}', '=', '+', '-', '*', '/', '\\', '|', '&', '^', '%', '$', '#', '@', '!', '~', '`', '?', ':', ';', ',', '.', ' ', '\t', '\n'],
    'encoded': ['&lt;', '&gt;', '&#40;', '&#41;', '&#91;', '&#93;', '&#123;', '&#125;', '&#61;', '&#43;', '&#45;', '&#42;', '&#47;', '&#92;', '&#124;', '&#38;', '&#94;', '&#37;', '&#36;', '&#35;', '&#64;', '&#33;', '&#126;', '&#96;', '&#63;', '&#58;', '&#59;', '&#44;', '&#46;', '&#32;', '&#9;', '&#10;'],
    'url_encoded': ['%3C', '%3E', '%28', '%29', '%5B', '%5D', '%7B', '%7D', '%3D', '%2B', '%2D', '%2A', '%2F', '%5C', '%7C', '%26', '%5E', '%25', '%24', '%23', '%40', '%21', '%7E', '%60', '%3F', '%3A', '%3B', '%2C', '%2E', '%20', '%09', '%0A']
}

SPECIAL_CHARS['for_html_tags'] = {
    '<': ['<', '&lt;', '%3C'],
    '>': ['>', '&gt;', '%3E'],
    '/': ['/', '&#47;', '%2F']
}

SPECIAL_CHARS['for_js_escape'] = {
    '"': ['"', '&quot;', '&#34;', '%22'],
    "'": ["'", '&apos;', '&#39;', '%27'],
    '`': ['`', '&#96;', '%60'],
    '\\': ['\\', '&#92;', '%5C'],
    '\n': ['\n', '&#10;', '%0A'],
    '\r': ['\r', '&#13;', '%0D'],
    '\t': ['\t', '&#9;', '%09'],
    '\b': ['\b', '&#8;', '%08'],
    '\f': ['\f', '&#12;', '%0C'],
    '\v': ['\v', '&#11;', '%0B']
}

HTML_TAGS = [
    'html', 'head', 'title', 'base', 'link', 'meta', 'style', 'script', 'noscript',
    'body', 'section', 'nav', 'article', 'aside', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'header', 'footer', 'address', 'main', 'p', 'hr', 'pre', 'blockquote', 'ol', 'ul',
    'li', 'dl', 'dt', 'dd', 'figure', 'figcaption', 'div', 'a', 'em', 'strong', 'small',
    's', 'cite', 'q', 'dfn', 'abbr', 'data', 'time', 'code', 'var', 'samp', 'kbd', 'sub',
    'sup', 'i', 'b', 'u', 'mark', 'ruby', 'rt', 'rp', 'bdi', 'bdo', 'span', 'br', 'wbr',
    'ins', 'del', 'picture', 'source', 'img', 'iframe', 'embed', 'object', 'param',
    'video', 'audio', 'track', 'map', 'area', 'table', 'caption', 'colgroup', 'col',
    'tbody', 'thead', 'tfoot', 'tr', 'td', 'th', 'form', 'label', 'input', 'button',
    'select', 'datalist', 'optgroup', 'option', 'textarea', 'output', 'progress', 'meter',
    'fieldset', 'legend', 'details', 'summary', 'dialog', 'script', 'noscript', 'template',
    'canvas', 'svg', 'math'
]

USEFUL_JS_FUNCTION = [
    'alert', 'fetch', 'document.write', 'document.writeln', 'document.writeIn', 'document.createElement'
]