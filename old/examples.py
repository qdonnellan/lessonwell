def link(example_code):
  return '''<a class="btn btn-success" href='/playground?example=%s'><i class="icon-eye-open"></i> See An Example in the Playground</a>''' % example_code

quote = link("quote::The block quote feature is designed to give longer quotes an emphasized resting place, separated from the rest of your content. Use this for muiltiple-line quotes::quote")
video = link("video:: http://www.youtube.com/watch?v=nKIu9yen5nc ::video")
gslide = link("gslide::https://docs.google.com/presentation/d/1f0c_-cEay8wcPE2lReY_h0TjOyckkuHj0-kfyJUU1RU/pub?start=false&loop=false&delayms=3000::gslide")
gdraw = link("gdraw:: https://docs.google.com/drawings/d/1cCrTvU94AqOWedLBYwN-bBmy1NBir7ZV63ZCKNXmEm8/pub?w=960&h=720 ::gdraw")
gdoc = link("gdoc:: https://docs.google.com/document/d/1R6hzH_q5NK7dj9pAU143x7VP04lOfhu6kh0yDG_syD8/pub ::gdoc")
gsheet = link("gsheet:: <iframe width='500' height='300' frameborder='0' src='https://docs.google.com/spreadsheet/pub?key=0ArZBt00TOweMdC10cU5vb0NBSTJ3QnQ4eG5KR1RXVHc&output=html&widget=true'></iframe> ::gsheet")
