
Table of content

1. Code structure

All code shall follow the following general structure for naming convention;
* Namespace or package name should be ADC
* Files, classes and most (see below for exceptions) function names are named with initial upper case letter and upper case letters starting each new word. An abbreviation shall be spelt in all upper case letters.
Examples: file TigerTreeHashImplementation.h, class TTHImplementation, function CalculateTTH()
* All member variables shall be named with first word in lower case and upper case letters starting each new word. An abbreviation shall be spelt in all upper case letters. All variables shall be prefixed with an underscore ('_') or as the language recommendation unless the language is listed as below;
  C++: m_
  C#: _
Examples: m_fooBar, _fooBar
* All member properties (e.g. in C#) shall be named similarly as Files, classes and functions. In languages that do not support properties, function implementation of properties (get/set), 'get' and 'set' shall be prefixed with the 'property' name.
Examples: MessageType, getMessageType(), setMessageType(...)
* Function scoped variables shall be named with first word in lower case and upper case letters starting each new word. An abbreviation shall be spelt in all upper case letters. 
Examples: lifeAndMeaningOfLife, debugSource

Block structure
* Ifs and loops should always be surrounded by a code block, regardless if the code blocks are needed or not.
Example: 
a) OK: if( 42 == lifeAndMeaningOfLife ) { print "42" }
b) Not OK: if ( 42 == lifeAndMeaningOfLife ) print "42"

Code/Type safety
* Implementations should always strive to be as compile-time safe as possible. 
* Functions should be as const-correct as possible. All get() functions should be constant. 
Example: int getFooBar() const;

Documentation
* All files, classes, functions and member variables shall be documented.
* All files shall contain a copyright notice pointing to the ADCProject and the New BSD license. See 2. Code license below.

Return values
* Functions should return as few values as possible and instead rely on references as funtion parameters. 

2. Code license

All code that is submitted to the ADCProject should have a note specifying the transfer of copyright to the ADCProject.

The LICENSE is New BSD License (3-clause BSD license).

See the file LICENSE for the text to use in each file.