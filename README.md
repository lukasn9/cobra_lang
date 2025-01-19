# CobraLang Programming Language and Custom IDE
CobraLang is a Python-like programming language designed for simplicity and readability. It offers a familiar structure, and also includes a custom IDE designed for CobraLang, in which you can create and write `.cl` files.

## Table of Contents
1. [Keywords and Syntax](#keywords-and-syntax)
   1. [Classes](#classes)
   2. [Function Definition](#function-definition)
   3. [Output (Print)](#output-print)
   4. [Conditional Statements](#conditional-statements)
   5. [Loops](#loops)
   6. [Loop Control](#loop-control)
   7. [Return Value](#return-value)
   8. [Logical Operators](#logical-operators)
   9. [Membership Operators](#membership-operators)
   10. [Equality and Comparison](#equality-and-comparison)
   11. [Arithmetic Operators](#arithmetic-operators)
   12. [Variable Assignment](#variable-assignment)
2. [Examples](#examples)
3. [IDE](#ide)
4. [Installation](#installation)

## Keywords and Syntax
Below is a list of CobraLang keywords, their Python equivalents, and examples.

### Function Definition

**Python**  
`def greet(name):`  
**CobraLang**  
`define greet(name):`

### Classes

**Python**
`def __init__`
**CobraLang**
`define _initialize`

**Python**
`self.name`
**CobraLang**
`own.name`

### Output (Print)

**Python**  
`print("Hello")`  
**CobraLang**  
`output "Hello"`

### Conditional Statements

#### If Statement

**Python**  
`if x > 10:`  
**CobraLang**  
`if x is greater than 10:`

#### Else Statement

**Python**  
`else:`  
**CobraLang**  
`otherwise:`

#### Else If (Elif) Statement

**Python**  
`elif y < 5:`  
**CobraLang**  
`else if y is less than 5:`

### Loops

#### For Loop

**Python**  
`for i in range(1, 11):`  
**CobraLang**  
`repeat i from 1 to 10:`

#### While Loop

**Python**  
`while x < 10:`  
**CobraLang**  
`loop while x < 10:`

### Loop Control

#### Break

**Python**  
`break`  
**CobraLang**  
`exit`

#### Continue

**Python**  
`continue`  
**CobraLang**  
`skip`

### Return Value

**Python**  
`return result`  
**CobraLang**  
`give result`

### Logical Operators

#### And

**Python**  
`if x > 0 and y < 0:`  
**CobraLang**  
`if x is positive and y is negative:`

#### Or

**Python**  
`if x > 0 or y == 0:`  
**CobraLang**  
`if x is positive or y is zero:`

#### Not

**Python**  
`if not condition:`  
**CobraLang**  
`if not condition:`

### Membership Operators

#### In

**Python**  
`if item in collection:`  
**CobraLang**  
`if item within collection:`

### Equality and Comparison

#### Equality

**Python**  
`if a == b:`  
**CobraLang**  
`if a is equal to b:`

#### Not Equal

**Python**  
`if a != b:`  
**CobraLang**  
`if a is not equal to b:`

#### Greater Than

**Python**  
`if a > b:`  
**CobraLang**  
`if a is greater than b:`

#### Less Than

**Python**  
`if a < b:`  
**CobraLang**  
`if a is less than b:`

#### Greater Than or Equal To

**Python**  
`if a >= b:`  
**CobraLang**  
`if a is at least b:`

#### Less Than or Equal To

**Python**  
`if a <= b:`  
**CobraLang**  
`if a is at most b:`

### Arithmetic Operators

#### Addition

**Python**  
`result = a + b`  
**CobraLang**  
`result = a add b`

#### Subtraction

**Python**  
`result = a - b`  
**CobraLang**  
`result = a subtract b`

#### Multiplication

**Python**  
`result = a * b`  
**CobraLang**  
`result = a multiply b`

#### Division

**Python**  
`result = a / b`  
**CobraLang**  
`result = a divide b`

#### Integer Division

**Python**  
`result = a // b`  
**CobraLang**  
`result = a integer divide b`

#### Modulus

**Python**  
`result = a % b`  
**CobraLang**  
`result = a modulus b`

#### Exponentiation

**Python**  
`result = a ** b`  
**CobraLang**  
`result = a power b`

### Variable Assignment

**Python**  
`x = 5`  
**CobraLang**  
`x becomes 5`

## Examples

### Example 1: Simple Function

**CobraLang**
```plaintext
define greet(name):
    output "Hello"

repeat i from 1 to 3:
    greet("Alice")
```

**Python Translation**
```python
def greet(name):
    print("Hello, " + name)

for i in range(1, 4):
    greet("Alice")
```

### Example 2: Conditional and Loop

**CobraLang**
```plaintext
define check_number(x):
    if x is greater than 0:
        output "Positive"
    else if x is equal to 0:
        output "Zero"
    otherwise:
        output "Negative"

repeat n from -2 to 2:
    check_number(n)
```

**Python Translation**
```python
def check_number(x):
    if x > 0:
        print("Positive")
    elif x == 0:
        print("Zero")
    else:
        print("Negative")

for n in range(-2, 3):
    check_number(n)
```

## IDE
The IDE included with the CobraLang programming language is specially designed to work with the language flawlessly and without any issues. It introduces a minimalistic and modern design, and a lot of features to help with development with more coming soon.

## Installation
There are two ways to install the programming language and the IDE. The simple way is to download a `.zip` file from the `releases` section, and run the `.exe` file. The other option is to clone the repository and build the program yourself.