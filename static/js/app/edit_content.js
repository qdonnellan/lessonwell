define(
    ['knockout', './editContentViewModel', 'jquery', 'rangyinputs'], 
    function (ko, viewModel, $, rangy) {

        var vm = new viewModel();
        ko.applyBindings( vm );

        $(document).ready(function() {
            vm.activateSpecificContent();
            vm.updateCustomer();
        });

        $("#lesson-textarea").on('keyup', function () {
            vm.refreshOutputStyle();
        });

        // A huge thanks to @timdown for rangyinputs, on top of which this is built
        // https://github.com/timdown/rangyinputs

        $(document).ready(function() {
            var $ta = $(".inputContent");
            var $startIndex = $("#startIndex"), $endIndex = $("#endIndex");

            function reportSelection() {
                var sel = $ta.getSelection();
                $startIndex.text(sel.start);
                $endIndex.text(sel.end);
            };

            $(document).on("selectionchange", reportSelection);
            $ta.on("keyup input mouseup textInput", reportSelection);
            $ta.focus();
            reportSelection();

            $(".shorthand-button").mousedown(function(e) {
                vm.lessonChange();
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
                        $ta.replaceSelectedText('\n> Replace this text with a quote\n> just keep adding lines with the ">" character \n\n');
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
                    $ta.replaceSelectedText('http://www.google.com \n');
                    break;

                }
                $ta.focus();
                // For IE, which always shifts the focus onto the button
                window.setTimeout(function() {
                    $ta.focus();
                }, 0);

                vm.current_lesson_body( $ta.val() );
            });
        });
    });
