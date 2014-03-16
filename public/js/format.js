formatInput = function(input_str) {
    links = input_str.match(/\bhttps?[:][\/][\/]\S*\b/g);
    if (links) {
        for (var i = 0; i < links.length; i++) {
            var link = links[i];
            input_str = input_str.replace(link, formatLink(link));
        }
    }
    //remove the link placeholder
    input_str = input_str.replace(new RegExp('::LINK::PLACEHOLDER::', 'g'), 'http');
    return markdown.toHTML(input_str);
};

formatLink = function(link) {
    //add a link placeholder so that we don't replace the same link more than once
    link = link.replace('http', '::LINK::PLACEHOLDER::');
    if (link.match(/\S*[.]png|jpg|bmp|jpeg|tiff|tif|gif|jp2\b/)) {
        return "![" + link + "](" + link + ")";
    }
    else {
        return "[" + link + "](" + link + ")";
    }  
};

