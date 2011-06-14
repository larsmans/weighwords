**WeighWords** is a Python library for creating word weights from text. It can
be used to create word clouds.

WeighWords does not do visualization of word clouds. For that, you can paste
its output into http://wordle.net, the `IBM Word-Cloud Generator
<http://www.alphaworks.ibm.com/tech/wordcloud>`_.

Rather than use simple word frequency, it weighs words by statistical models
known as *parsimonious language models*. These models are good at picking up
the words that distinguish a text document from other documents in a
collection. The downside to this is that you can't use WeighWords to make a
word cloud of a single document; you need a bunch of document to compare to.


References
----------
D. Hiemstra, S. Robertson and H. Zaragoza (2004). Parsimonious Language Models
for Information Retrieval. Proc. SIGIR'04.

R. Kaptein, D. Hiemstra and J. Kamps (2010). How different are Language Models
and word clouds? Proc. ECIR.
