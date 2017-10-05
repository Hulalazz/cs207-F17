# Project Rubric

| Component                   | Percentage |
| :-------------------------: | :--------: |
| Model Document              |            |
| Code documentation          |            | 
| Input file + parsing        |            |
| Code design                 |            |
| Test suite                  |            |

---

## Model Document
Write a document that describes the API and how to run the code.  The sections of the 
document should be:
1. Introduction:  Describe what problem the code is solving.  You may borrow the Latex 
   expressions from my lecture notes.  Discuss in broad strokes what the purpose of the 
   code is along with any features.  Do not describe the details of the code yet.
2. Installation:  Describe where the code can be found and downloaded.  Tell the user 
   how to run the test suite.  We are not releasing this code as a package yet, but 
   when we do that this section will include instructions how how to install the package.
3. Basic Usage and Examples:  Provide a few examples on using your software in some 
   common situations.  You may want to show how the code works with a small set of 
   reactions.

## Code Documentation
All modules, classes, and methods must be documented.  Try 
not to repeat things.  Make sure you include doctests as appropriate.

## Input file
Your code must be able to read in and parse an `XML` input file (as discussed in class).  I will 
provide you with the form of the input file.

## Code design
Your code must be written in an object oriented manner.  Here is an outline of the required 
structural components:
* You should include all classes in a single file called `chemkin.py`.  
* Make a class for reaction rate coefficients.  So far we have only talked about three types 
  of reaction rate coefficients:  constant, Arrhenius, and modified Arrhenius.  There are 
  other types and your code should be easily extensible to handle new types of reaction 
  rate coefficients in future verions.
* Make a class for reactions.  So far we have only talked about elementary reactions.  
  There are other types of reactions.  For example, *three-body reactions* and *duplicate* 
  reactions are common.  There could be other types as well.  Your code should be 
  written in such a way that it can be easily extended to these other types of reactions 
  in future versions.
* Note that we have only worked with **irreversible** reactions.  Most reactions are 
  actually reversible.  Your code should be aware of this fact and have hooks for 
  future modifications that can handle fully reversible reactions.

## Test suite
Be sure to include a comprehensive test suite.  You must use Travis CI to run your tests 
and use Coveralls to test code coverage.  All tests **must** pass!  Your code coverage 
should be greater than 70%.  Put build and coverage status badges in your project repo 
README.md.
