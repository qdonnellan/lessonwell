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
    e.preventDefault();
    var qsel = $ta.getSelection();
    switch (this.name) {
      case "bold":
        if (qsel.start === qsel.end) {
          $ta.replaceSelectedText("**a-bold-word**");
          break;
        }
        else {
          $ta.surroundSelectedText("**", "**");
          break;
        }
      case "ital":
        if (qsel.start === qsel.end) {
          $ta.replaceSelectedText("*italics-word*");
          break;
        }
        else {
          $ta.surroundSelectedText("*", "*");
          break;
        }
      case "video":
        if (qsel.start === qsel.end) {
          $ta.replaceSelectedText("\nvideo:: replace-this-with-youtube-link ::video\n\n");
          break;
        }
        else {
          $ta.surroundSelectedText("\nvideo:: ", " ::video\n\n");
          break;
        }
      case "image":
        if (qsel.start === qsel.end) {
          $ta.replaceSelectedText("\nimage:: replace-this-with-image-link ::image\n\n");
          break;
        }
        else {
          $ta.surroundSelectedText("\nimage:: ", " ::image\n\n");
          break;
        }
      case "quote":
        if (qsel.start === qsel.end) {
          $ta.replaceSelectedText("quote:: replace these words with the text you'd like to quote ::quote\n");
          break;
        }
        else {
          $ta.surroundSelectedText("quote:: ", " ::quote\n");
          break;
        }
      case "code":
        if (qsel.start === qsel.end) {
          $ta.replaceSelectedText("code::\nreplace this with your code block\n::code\n");
          break;
        }
        else {
          $ta.surroundSelectedText("code::\n", "\n::code\n");
          break;
        }
      case "link":
        if (qsel.start === qsel.end) {
          $ta.replaceSelectedText("[Link Title](http://www.google.com)");
          break;
        }
        else {
          $ta.surroundSelectedText("[Link Title](", ")");
          break;
        }
      case "quiz":
        $ta.replaceSelectedText(
          "\nquiz::\n\nWhat is the answer to this question?\n@@ This answer\n@@ This one\n@@ Or this one**\n\nreason::The third one is correct\n\n::quiz\n\n",
          "collapseToEnd");   
          break;

      case "equation":
        $ta.replaceSelectedText(
          "$ f(x) = mx + b $\n");  
          break;

      case "fraction":
        $ta.replaceSelectedText(
          "$ \\frac{a}{b} $\n");  
          break;

      case "inequality":
        $ta.replaceSelectedText(
          "$ 0 \\le x \\le 1 $\n"); 
          break; 

      case "greek_ddelta":
        $ta.replaceSelectedText(
          "$ \\Delta $\n"); 
          break;

      case "greek_delta":
        $ta.replaceSelectedText(
          "$ \\delta $\n"); 
         break;

      case "greek_equation":
        $ta.replaceSelectedText(
          "$ \\alpha + x^2 $\n"); 
         break;
    }
    $ta.focus();

    // For IE, which always shifts the focus onto the button
    window.setTimeout(function() {
      $ta.focus();
    }, 0);
  });
});