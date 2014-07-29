// A huge thanks to @timdown for rangyinputs, on top of which this is built
// https://github.com/timdown/rangyinputs

define(
    ['rangyinputs', 'jquery'], function (rangy, $) {

    return function qSelect(viewModel) {
        var self = this;
        var $ta = $(".inputContent");
        var $startIndex = $("#startIndex"), $endIndex = $("#endIndex");

        self.reportSelection = function() {
            var sel = $ta.getSelection();
            $startIndex.text(sel.start);
            $endIndex.text(sel.end);
        };

        $(document).on("selectionchange", self.reportSelection());
        $ta.on("keyup input mouseup textInput", self.reportSelection());
        $ta.focus();
        self.reportSelection();

        $(".shorthand-button").mousedown(function(e) {
            viewModel.lessonChange();
            e.preventDefault();
            var qsel = $ta.getSelection();
            switch (this.name) {
                case "bold":
                    if (qsel.start === qsel.end) {
                        $ta.replaceSelectedText("**a-bold-word** "); 
                        break;
                    } else { 
                        $ta.surroundSelectedText("**", "** ");  
                        break;
                    }

                case "ital":
                    if (qsel.start === qsel.end) {
                        $ta.replaceSelectedText("*italics-word* ");
                        break;
                    } else {
                        $ta.surroundSelectedText("*", "* ");
                        break;
                    }

                case "quote":
                    if (qsel.start === qsel.end) {
                        $ta.replaceSelectedText('\n> Replace this text with a quote;\n> just keep adding lines with the ">" character \n\n');
                        break;
                    } else {
                        $ta.surroundSelectedText("\n>", "\n\n");
                        break;
                    }

                case "bullets":
                    $ta.replaceSelectedText('\n- First Item\n- Second Item\n- Third Item\n\n');
                    break;

                case "enums":
                    $ta.replaceSelectedText('\n1. First Item\n- Second Item\n- Third Item\n\n');
                    break;
            
                case "heading1":
                    if (qsel.start === qsel.end) {
                        $ta.replaceSelectedText('\n# Large Heading\n');
                        break;
                    } else {
                        $ta.surroundSelectedText("\n# ", "\n");
                        break;
                    }

                case "heading2":
                    if (qsel.start === qsel.end) {
                        $ta.replaceSelectedText('\n## Medium Heading\n');
                        break;
                    } else {
                        $ta.surroundSelectedText("\n## ", "\n");
                        break;
                    }

                case "heading3":
                    if (qsel.start === qsel.end) {
                        $ta.replaceSelectedText('\n### Small Heading\n');
                        break;
                    } else {
                        $ta.surroundSelectedText("\n### ", "\n");
                        break;
                    }

                case "link":
                    $ta.replaceSelectedText('http://www.google.com\n');
                    break;

                case "image":
                    $ta.replaceSelectedText(
                        'http://donnellan.smugmug.com/photos/i-nvj7H7L/0/L/i-nvj7H7L-L.jpg\n'
                        );
                    break;

                case "youtube":
                    $ta.replaceSelectedText(
                        'https://www.youtube.com/watch?v=V58_jPeLnrs\n'
                        );
                    break;


            }
            $ta.focus();
            // For IE, which always shifts the focus onto the button
            window.setTimeout(function() {
                $ta.focus();
            }, 0);

            viewModel.current_lesson_body( $ta.val() );
        });
    };
});
