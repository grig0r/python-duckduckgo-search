python-duckduckgo-search
======
Simple duckduckgo client library

Installation
----

.. code-block:: bash

  python setup.py install

one-liner

.. code-block:: bash

  git clone https://github.com/grig0r/python-duckduckgo-search && cd python-duckduckgo-search/ && python setup.py install

Usage
----

.. code-block:: pycon

  >>> import ddgclient

create search instance

.. code-block:: pycon

  >>> search = ddgclient.Search('perl')

get list of result objects

.. code-block:: pycon

  >>> results = search.results(20)
  >>> results
  [<Result: The Perl Programming Language - www.perl.org (https://www.perl.org/)>,
   <Result: Perl - Wikipedia (https://en.wikipedia.org/wiki/Perl)>,
   <Result: Perl - Introduction - tutorialspoint.com (http://www.tutorialspoint.com/perl/perl_introduction.htm)>,
  [...]

get attributes from result object

.. code-block:: pycon

  >>> first_result = results[0]
  >>> first_result.title
  'The Perl Programming Language - www.perl.org'
  >>> first_result.url
  'https://www.perl.org/'
  >>> first_result.description
  'The Perl Programming Language at Perl.org. Links and other helpful resources for new and experienced Perl programmers.'
