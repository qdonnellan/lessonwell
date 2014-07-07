requirejs.config({
    baseUrl: 'static/js',
    paths: {
        app: './app',
        jquery: 'lib/jquery-1.11.1.min',
        knockout: 'lib/knockout-3.0.0',
        highlight: 'lib/highlight.pack',
        markdown: 'lib/markdown',
        formatLesson: 'lib/format_lesson'
    },
    shim : {
        "markdown": {
            exports: "markdown"
        }
    }
});