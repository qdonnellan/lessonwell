import markdown2
import cgi
import re
import logging
import examples
import hashlib
import random
import string

def formatContent(contents, helpdoc = False):
  newContents= []
  for content in contents:
    newContents.append(formatted(content, helpdoc))        
  return newContents

class formatted():
  def __init__(self, content, helpdoc):
    # Passing everything, including the formatted body, to the new formatted class
    self.body = shorthand(content.body)
    self.title = content.title
    if not helpdoc:
        self.contentType = content.contentType 
    self.id = content.key.id()

def shorthand(body):
  # Escaping underscore charcters before Markdown

  questionmark = 'question_mark' + ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(20))
  underscore = 'underscore' + ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(20))

  body = re.sub('[?]', questionmark, body)
  body = re.sub('_', underscore, body)



  # Escaping user-supplied HTML injection
  body = cgi.escape(body)


  #escaping double backslash \\
  backslash = 'backslash' + ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(20))
  body = re.sub(r'\\', backslash, body)

  #escaping asterisks in code-blocks
  if len(re.findall('code::', body)) == len(re.findall('::code', body)):    
    code_pattern = re.compile('code::(.*?)::code', re.DOTALL)
    code_blocks = re.findall(code_pattern, body)    
    for code_block in code_blocks:
      logging.info(code_block)
      code_block = re.sub('[*]', '\*', code_block)
      embed_code = '!@!modified_code!@!::%s::!@!modified_code!@!' % (code_block.strip())
      body = re.sub(code_pattern, embed_code, body, count = 1)

  body = re.sub('!@!modified_code!@!', 'code', body)


  body = re.sub('::image', '', body)
  body = re.sub('image::', '', body)
  body = re.sub('video::', '', body)
  body = re.sub('::video', '', body)

  # Escape links inside code blocks
  code_link = 'code' + ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(20))
  if len(re.findall('code::', body)) == len(re.findall('::code', body)):    
    code_pattern = re.compile('code::(.*?)::code', re.DOTALL)
    code_blocks = re.findall(code_pattern, body)    
    for code_block in code_blocks:
      code_block = re.sub(r'][(]http', code_link, code_block)
      embed_code = "code::%s::code" % code_block
      body = re.sub(code_pattern, embed_code, body, count = 1)
      logging.info(code_block)


  # escape links that have already been formatted with markdown syntax
  md_link_placeholder1 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(20))
  md_link_placeholder2 = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(20))
  body = re.sub(r'\]\(https:', md_link_placeholder2, body)
  body = re.sub(r'\]\(http:', md_link_placeholder1, body)


  # find and collect all links not already escaped
  links = re.findall(r"\bhttps[:][/][/]\S*\b", body)
  links += re.findall(r"\bhttp[:][/][/]\S*\b", body)

  # reintroduce excaped links in markdown
  
  body = re.sub(md_link_placeholder1,'](http:', body )
  body = re.sub(md_link_placeholder2,'](https:', body )

  # for each found link, determine if it is a link, image, or video
  link_bank = {}
  for link in links:
    logging.info(link)
    random_placeholder = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(20))
    if not (link.startswith('](') and link.endswith(')')):
      body = re.sub(link, random_placeholder, body, count = 1)
    if link.endswith((".png", ".jpeg", ".jpg", ".svg", ".bmp", ".tiff", ".gif", ".jp2", ".tif")):
      link_bank[random_placeholder] = "image:: %s ::image" % link
    elif 'youtube.com' in link or '//youtu.be/' in link or '/vimeo.com/' in link:
      logging.info(link)
      link_bank[random_placeholder] = "video:: %s ::video" % link
    else:
      link_bank[random_placeholder] = "link:: %s ::link" % link

  # Markdown!
  body = markdown2.markdown(body)

  # Un-escaping underscore characters (post-Markdown)

  for ref in link_bank:
    body = re.sub(ref, link_bank[ref], body, count = 1)

  # un-escaping links inside code blocks
  logging.info(body)
  body = re.sub(code_link, "](http", body)

  body = re.sub(underscore, '_', body)
  body = re.sub(questionmark, '?', body)
  body = re.sub(backslash, r'\\', body)


  # Code shorthands
  if len(re.findall('code::', body)) == len(re.findall('::code', body)):    
    code_pattern = re.compile('code::(.*?)::code', re.DOTALL)
    code_blocks = re.findall(code_pattern, body)    
    for code_block in code_blocks:
      code_block = re.sub('<p>', '', code_block)
      code_block = re.sub('</p>', '', code_block)
      code_type = 'prettyprint'
      if code_block.startswith('=latex'):
        code_block = re.sub('=latex', ' ', code_block, count = 1)
        code_type += 'lang-tex'
      elif code_block.startswith('=clear'):
        code_block = re.sub('=clear', '', code_block, count = 1)
        code_type = ''
      embed_code = '''
        <pre class="%s code-block">%s</pre>''' % (code_type, code_block.strip())
      body = re.sub(code_pattern, embed_code, body, count = 1 )

  # Formatting for code blocks (post-Markdown)
  if 'code=latex' in body:
    body = re.sub('code=latex', '', body)
    body = re.sub(r'<pre><code>', r'<pre class="prettyprint lang-tex">', body)
  elif 'code=blank' in body:
    body = re.sub('code=blank', '', body)
    body = re.sub(r'<pre><code>', r'<pre>', body)
  else:
    body = re.sub(r'<pre><code>', r'<pre class="prettyprint">', body)
  body = re.sub(r'</code></pre>', r'</pre>', body)    

  # Re-formatting double-escaped stuff (post-Markdown)
  body = re.sub(r'&amp;lt;',r'&lt;', body)
  body = re.sub(r'&amp;gt;',r'&gt;', body)
  body = re.sub(r'&amp;amp;',r'&amp;', body)

  quotePre = '''
  <div class="lesson-quote well"><p class="lead">
  <span><i class="icon-quote-left icon-4x pull-left icon"></i></span>       
  '''
  if len(re.findall('quote::', body)) == len(re.findall('::quote', body)):
    body = re.sub('quote::', quotePre, body)
    body = re.sub('::quote', '</p></div>', body)

  body = re.sub('cite::', '<div class="col-lg-12"><p class="pull-right lesson-citation"><i class="icon-user"></i> ', body)
  body = re.sub('::cite', '</p></div>', body)

  #Embedding Youtube and Vimeo Videos 
  if len(re.findall('video::', body)) == len(re.findall('::video', body)):
    pattern = re.compile('video::(.*?)::video', re.DOTALL)
    videos = re.findall(pattern, body)
    for video in videos:
      if 'youtube' in video or '//youtu.be/' in video:
        if '?v=' in video:
          if '&' in video:
            youtube_id = re.search('[?]v=(.*)&', video).group(1)
          else:
            youtube_id = re.search('v=(.*)', video).group(1)  
        else:
          youtube_id = video  
        youtube_video_code = '''
          <section class="row">
            <div class="col-lg-12">
              <div class="flex-video widescreen">
                <iframe src="https://www.youtube-nocookie.com/embed/%s" frameborder="0" allowfullscreen=""></iframe>
              </div>
            </div>
          </section>
        ''' % youtube_id
        body = re.sub(pattern, youtube_video_code, body, count = 1)
      elif 'vimeo' in video:
        vimeo_id = re.search('/vimeo.com/(.*)', video).group(1)
        vimeo_video_code = '''
          <section class="row">
            <div class="col-lg-12">
              <div class="flex-video widescreen">
                <iframe src="//player.vimeo.com/video/%s" width="500" height="281" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>
              </div>
            </div>
          </section>
        ''' % vimeo_id
        body = re.sub(pattern, vimeo_video_code, body, count = 1)
        

 
  # (DEPRECATED) For codeblocks with instructions to embed videos 
  # see the below ;-; method for the new version of this...
  body = re.sub('video;;', 'video::', body)
  body = re.sub(';;video', '::video', body)

  # Embedding Links with link tags
  if len(re.findall('link::', body)) == len(re.findall('::link', body)):
    link_pattern = re.compile('link::(.*?)::link', re.DOTALL)
    link_publish_links = re.findall(link_pattern, body)    
    for link in link_publish_links:
      link_embed_code = "<a href=%s>%s</a>" % (link, link)
      body = re.sub(link_pattern, link_embed_code, body, count = 1 )

  # Embedding Images with the Image Tags (image:: ::image)
  if len(re.findall('image::', body)) == len(re.findall('::image', body)):
    image_pattern = re.compile('image::(.*?)::image', re.DOTALL)
    image_publish_links = re.findall(image_pattern, body)    
    for image_link in image_publish_links:
      image_embed_code = '''
          <section class="image-div col-lg-12">
            <img class="image-holder" src="%s" alt=""/>
          </section>''' % image_link.strip()
      body = re.sub(image_pattern, image_embed_code, body, count = 1 )

  # Embedding Google Drive Presentations
  if len(re.findall('gslide::', body)) == len(re.findall('::gslide', body)):
    gslide_pattern = re.compile('gslide::(.*?)::gslide', re.DOTALL)
    gslide_publish_links = re.findall(gslide_pattern, body)    
    for gslide_link in gslide_publish_links:
      gslide_id = re.search('/presentation/d/(.*)/pub', gslide_link)
      if gslide_id is not None:
        gslide_embed_code = '''
            <section class="row">
                <div class="col-lg-12">
                    <div class="flex-video">
                        <iframe src="https://docs.google.com/presentation/d/%s/embed?start=false&loop=false&delayms=3000" frameborder="0" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
                    </div>
                </div>
            </section>''' % gslide_id.group(1)
        body = re.sub(gslide_pattern, gslide_embed_code, body, count = 1 )


  # Embedding Google Drive Spreadsheets
  if len(re.findall('gsheet::', body)) == len(re.findall('::gsheet', body)):
    gsheet_pattern = re.compile('gsheet::(.*?)::gsheet', re.DOTALL)
    gsheet_publish_links = re.findall(gsheet_pattern, body)    
    for gsheet_link in gsheet_publish_links:
      gsheet_id = re.search(r'key=(.*)&amp;', gsheet_link)
      if gsheet_id is not None:
        gsheet_embed_code = '''
            <section class="row-fluid">
                <div class="span12">
                    <div class="flex-video">
                        <iframe src="https://docs.google.com/spreadsheet/pub?key=%s&output=html&widget=true" frameborder="0" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
                    </div>
                </div>
            </section>''' % gsheet_id.group(1)
        body = re.sub(gsheet_pattern, gsheet_embed_code, body, count = 1 )

  # Embedding Google Drive Documents  
  if len(re.findall('gdoc::', body)) == len(re.findall('::gdoc', body)):
    gdoc_pattern = re.compile('gdoc::(.*?)::gdoc', re.DOTALL)
    gdoc_publish_links = re.findall(gdoc_pattern, body)    
    for gdoc_link in gdoc_publish_links:      
      gdoc_id = re.search('document/d/(.*)/pub', gdoc_link)
      if gdoc_id is not None:
        gdoc_embed_code = '''
            <section class="row-fluid">
                <div class="span12">
                    <div class="flex-video">
                        <iframe src="https://docs.google.com/document/d/%s/pub?embedded=true" frameborder="0" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
                    </div>
                </div>
            </section>''' % gdoc_id.group(1)
        body = re.sub(gdoc_pattern, gdoc_embed_code, body, count = 1 )

  # Embedding Google Drive Drawings 
  if len(re.findall('gdraw::', body)) == len(re.findall('::gdraw', body)):
    gdraw_pattern = re.compile('gdraw::(.*?)::gdraw', re.DOTALL)
    gdraw_publish_links = re.findall(gdraw_pattern, body)    
    for gdraw_link in gdraw_publish_links:      
      gdraw_id = re.search('drawings/d/(.*)/pub', gdraw_link)
      if gdraw_id is not None:
        gdraw_embed_code = '''
            <section class="row-fluid">
                <div class="span12">
                    <img src="https://docs.google.com/drawings/d/%s/pub?w=1440&amp;h=1080">
                </div>
            </section>''' % gdraw_id.group(1)
        body = re.sub(gdraw_pattern, gdraw_embed_code, body, count = 1 )


  #Quizzes
  if len(re.findall('quiz::', body)) == len(re.findall('::quiz', body)):
    pattern = re.compile('quiz::(.*?)::quiz', re.DOTALL)    
    quizzes = re.findall(pattern, body) 
    q = 1      
    for quiz in quizzes:   
      try:
        answer_pattern = re.compile('@@(.*)')
        reason_pattern = re.compile('reason::(.*)')
        reason = re.search(reason_pattern, quiz)
        if reason is None:
          reason = ''
        else:
          reason = reason.group(1)
          quiz = re.sub(reason_pattern, '', quiz)

        answers = re.findall(answer_pattern, quiz) 
        a = 1
        verification = ''
        a_prefix=' ABCDEFGHIJKLMNOPQRSTUV'
        for answer in answers:
          if '**' in answer:
            answer = re.sub('[**]', '', answer)
            verification = hashlib.sha1(answer).hexdigest()
          replace_answer = '''
            <label class="radio answer-choice">
              <input type="radio" name="quiz%s" id="answer%s-%s" value="%s">
              %s) <span class="quiz-answer">%s</span>
            </label>    
                   
          ''' % (q, q, a, answer, a_prefix[a], answer)
          a +=1
          quiz = re.sub(answer_pattern, replace_answer, quiz, count=1)
        replacement = '''
          <div class="quiz-well">
            <form class="quiz-form" method="post" action="/ajax_quiz" id="quiz-%s">
              <input type="hidden" name="quiz-identity" value="quiz%s">
              <input type="hidden" name="quiz-verify" value="%s">
              <p>%s</p>   
              <div class="alert alert-danger incorrect-answer">
                <p><strong><i class="icon-remove"></i> Incorrect,</strong> please try again</p>
              </div> 
              <div class="alert alert-success correct-answer">
                <p><strong><i class="icon-ok"></i> Correct!</strong> %s</p>
              </div>    
              <button class="btn btn-info" id="submit-quiz" type="submit">Check Answer</button>
            </form>
          </div>
        ''' % (q, q, verification, quiz, reason)
        
      except Exception as e:
        error_message = '''
          <div class="alert alert-error">
            <h4>Error!</h4> Something isn't quite right with the shorthand you used to create this quiz.
          </div>
        '''
        body = re.sub(pattern, error_message, body, count = 1 )
      else:
        body = re.sub(pattern, replacement, body, count = 1 )

      q +=1

  # Formatting for step-by-step directions as a label (post-Markdown)
  # DEPRECATED, REPLACED BY THE CODE IMMEDIATELY FOLLOWING
  if len(re.findall(r'@@', body)) == 2*len(re.findall(r'/@@', body)):
    body = re.sub(r'/@@', r'</strong></button>', body)
    body = re.sub(r'@@',r'<button class="btn btn-primary disabled"> STEP <strong>', body)

  #step_pattern = re.compile('@@([^\s]+)')
  #found_steps = re.findall(step_pattern, body)
  #for step in found_steps:  
  #  logging.info('found one' + step)  
  #  step_html = '<button class="btn btn-primary disabled"> STEP <strong>%s</strong></button>' % step
  #  body = re.sub(pattern, step_html, body, count=1)


  # Unescaping helpdocs things
  body = re.sub('&amp;#64;', '@', body)


  # Allow the display of some shorthand by converting the temp ;-; key to :: 
  # so that video;-; will render as video:: and so on...
  body = re.sub('tag_code_tag', 'code', body)
  body = re.sub(';-;', '::', body)
  body = re.sub('tag_back_quote_tag::', '`', body)
  body = re.sub('::tag_back_quote_tag', '`', body)


  # Pre-set links which will populate the playground with example content
  body = re.sub('playground_example_quote', examples.quote, body)
  body = re.sub('playground_example_video', examples.video, body)
  body = re.sub('playground_example_gslide', examples.gslide, body)
  body = re.sub('playground_example_gdoc', examples.gdoc, body)
  body = re.sub('playground_example_gdraw', examples.gdraw, body)
  body = re.sub('playground_example_gsheet', examples.gsheet, body)
  return body
