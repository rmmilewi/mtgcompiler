# Arbor

![alt text](https://github.com/rmmilewi/mtgcompiler/raw/master/images/arbor_logo_alpha.jpeg "Arbor pre-alpha logo")

Arbor is an open-source platform for the analysis of Magic: The Gathering cards.

This is a labor of love co-developed by Reed Milewicz and Peter Klavins. The project is not yet ready, but we hope it will be soon! Check back later for more details.

## What is Arbor?

Arbor is an analysis framework inspired by source-to-source compilers, namely the [ROSE compiler infrastructure](http://rosecompiler.org) developed at Lawrence Livermore National Laboratory (LLNL). The core feature of the Arbor that it can parse Magic cards and produce a graph that is a sophisticated intermediate representation (IR) for those cards. So, given a card like this:

![alt text](https://github.com/rmmilewi/mtgcompiler/raw/master/images/black_lotus_example.png "Black Lotus Card")

Arbor produces, among other things, an abstract syntax tree (AST) like this:

![alt text](https://github.com/rmmilewi/mtgcompiler/raw/master/images/black_lotus_ast.png "Black Lotus AST")

Once cards are converted into this abstract format, Arbor provides interfaces for querying, editing, and analyzing those cards. Additionally, the Arbor IR can be unparsed to retrieve the original card text or to convert it to another format.

## What can Arbor do?

Arbor aims to be a platform upon which a user can easily build their own tools for working with Magic cards. Potential use cases include:

* Linter-like analysis for custom Magic cards (e.g. checking for type-correctness, stylistic errors)
* Deck analysis (e.g. How often will I be able to cast this card on turn 5?)
* Metagame analysis (e.g. How many creatures can this kill spell hit in standard?)
* Support for rich queries on card databases (e.g. find all cards that can give a creature haste.)
* Source code generation (e.g. Generating Java code for XMage directly from cards)

As Arbor becomes more mature and stable, we hope to provide mini-applications that demonstrate these use cases. 




