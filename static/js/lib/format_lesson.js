define(function (markdown) {

    var marked = require('marked');

    return {
        formatInput : function(input_str) {
            var links = input_str.match(/\bhttps?[:][\/][\/]\S*\b/g);
            if (links) {
                for (var i = 0; i < links.length; i++) {
                    var link = links[i];
                    // inject a placeholder so we don't screw stuff up
                    var escaped_link = link.replace('http', '::LINK::PLACEHOLDER::');
                    if (escaped_link.match(/\S*[.]png|jpg|bmp|jpeg|tiff|tif|gif|jp2\b/)) {
                        var image_link = "![" + escaped_link + "](" + escaped_link + ")";
                        input_str = input_str.replace(link, image_link);
                    }
                }
            }
            //remove the link placeholder
            input_str = input_str.replace(new RegExp('::LINK::PLACEHOLDER::', 'g'), 'http');

            var equations = input_str.match(/\$\$?(.*?)\$\$?/g);
            if (equations) {
                for (var i = 0; i < equations.length; i++) {
                    var eqn = equations[i];
                    // add these placeholders to avoid mixing behaviour between
                    // markdown syntax and mathjax (TeX) syntax
                    var new_eqn = eqn.replace(/_/g, '::MATH::UNDERSCORE::PLACEHOLDER::');
                    new_eqn = new_eqn.replace(/\*/g, '::MATH::ASTERISKS::PLACEHOLDER::')
                    input_str = input_str.replace(eqn, '$' + new_eqn + '$');
                }
            }

            var post_markdown_str = marked(input_str);

            // remove the math placeholder in math equation now that markdown is over!
            post_markdown_str = post_markdown_str.replace(/::MATH::UNDERSCORE::PLACEHOLDER::/g, '_');
            post_markdown_str = post_markdown_str.replace(/::MATH::ASTERISKS::PLACEHOLDER::/g, '*');

            return post_markdown_str;
        }
    };
});
