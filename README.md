# Server-client messaging program

## Table of Contents

[TOC]
<br/>
<br/>
<br/>
<br/>
<br/>
## Overview

### Local Network Edition
- Real-time messaging service, direct server-client communication
- Hosting and client services from user's own device
- Server name listings
- Server name - IP address resolution

### Internet (Global) Network Edition
- Switchboard like  client-server communication
- Client and Server programs communicate with central host

## Introduction

This document describes the logic behing the GUI_CHAT program(s) and design decisions made.

### Technologies
#### Python
All programming is done in Python. I was motivated to use python for several reasons. I already had a good foundation with the language, having used it in school and for minor projects. The language has a set of extensive libraries, this is significant because I have previously experimented with sockets in C, which is platform dependent, winsock for windows and sys/socket.h (BSD socket library) for UNIX. Python's libraries are often well integrated and allows me to focus on other parts of the project, rather than be bogged down in tedious tasks.
##### Tkinter
A primary feature of the Chat-server program is the use of a GUI to display information and interactive elements for the user to use. I wanted to learn something simple and easy to use, preferably already integrated in Python. For these reasons I chose Tkinter. Its simple widgets and structure was a pleasure to use, having previously worked with JavaFX.
#### AWS - EC2 Instance
In all instances of the program (local/global), the user will have to communicate with a central server to retrieve/send information. This central server had to be independent of a user's device and accessible from across the internet. AWS offers a range of services to solve this. I was initially drawn to AWS Lambda but lambda does not support TCP traffic, which is the only protocol used for sending messages in my program, as such I decided to use EC2 Instance service. As EC2 is a virtual machine, setting up the machine with my code would be easy as I can create the code on my own device and upload to the instance without making major modifications.



## Local Network Edition
### Introduction
The local network edition is the program which only allows for communication on local network. The idea behind the program is for any user to be able to host and join 'chat rooms' which are listed on the network by another user or dedicated machine. Both the server and client scripts are seperate. Therefore, if a user has created a server and wishes to join it, they will have to join via the listing menu.
![alt text](https://github.com/farnsolo/GUI_Chat/blob/main/socketDiagram.drawio.png)
> Diagram of Local Network model

### Server creation
The user first interacts with a main menu GUI (main.py). It is from here the program is initialised. The user is asked to input their username upon initilisation, which is logged and passed to the create_client function when the user decides to proceed to the listings menu. 

When creating a server, the user first inputs the servername. After this a new serverCPC object is initialised.Then a thread is created running the main server creation script (serverCPC.create_server) and the servername label is changed. Threads are used heavily in this project. To allow a user to continue using the program, a thread is used to create a background process where the server will listen and process incoming data.

In mainPC (lines 59-61):
<br/>
`self.t1 = threading.Thread(target=self.server.create_server)`
<br/>
`self.t1.daemon = True # Sets thread as background process`
<br/>
`self.t1.start() = True`
<br/>
<br/>

Server creation is successful, if server name is displayed on menu page AND server creation buttion is disabled.

##### serverCPC
The serverCPC class contains all methods and variables used to handle incoming and outgoing data. Upoun initialisation, the class creates a socket object, retrieves HOST (device IP) and lists server on global listenings (backendInterface.listServer).
Then the serverCPC class will bind the HOST and Port number (2525) to socket object and begins to listen.

###### server_create
The method server_create is the handler for new connections to server. 
<br/>
<br/>
The server accepts a new unique connection through line below:
<br/>
`self.conn, self.addr = self.sock.accept()`
<br/>
This sock.accept() returns a pair (conn,address) of which conn is a new socket object for that connection (server -> client). Address is the address bound to the socket on the other end of the connection (client).


####Code Blocks (Indented style)

Indented 4 spaces, like `<pre>` (Preformatted Text).

    <?php
        echo "Hello world!";
    ?>
    
Code Blocks (Preformatted text):

    | First Header  | Second Header |
    | ------------- | ------------- |
    | Content Cell  | Content Cell  |
    | Content Cell  | Content Cell  |

####Javascript　

```javascript
function test(){
	console.log("Hello world!");
}
 
(function(){
    var box = function(){
        return box.fn.init();
    };

    box.prototype = box.fn = {
        init : function(){
            console.log('box.init()');

			return this;
        },

		add : function(str){
			alert("add", str);

			return this;
		},

		remove : function(str){
			alert("remove", str);

			return this;
		}
    };
    
    box.fn.init.prototype = box.fn;
    
    window.box =box;
})();

var testBox = box();
testBox.add("jQuery").remove("jQuery");
```

####HTML code

```html
<!DOCTYPE html>
<html>
    <head>
        <mate charest="utf-8" />
        <title>Hello world!</title>
    </head>
    <body>
        <h1>Hello world!</h1>
    </body>
</html>
```

###Images

Image:

![](https://pandao.github.io/editor.md/examples/images/4.jpg)

> Follow your heart.

![](https://pandao.github.io/editor.md/examples/images/8.jpg)

> 图为：厦门白城沙滩 Xiamen

图片加链接 (Image + Link)：

[![](https://pandao.github.io/editor.md/examples/images/7.jpg)](https://pandao.github.io/editor.md/examples/images/7.jpg "李健首张专辑《似水流年》封面")

> 图为：李健首张专辑《似水流年》封面
                
----

###Lists

####Unordered list (-)

- Item A
- Item B
- Item C
     
####Unordered list (*)

* Item A
* Item B
* Item C

####Unordered list (plus sign and nested)
                
+ Item A
+ Item B
    + Item B 1
    + Item B 2
    + Item B 3
+ Item C
    * Item C 1
    * Item C 2
    * Item C 3

####Ordered list
                
1. Item A
2. Item B
3. Item C
                
----
                    
###Tables
                    
First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell 

| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |

| Function name | Description                    |
| ------------- | ------------------------------ |
| `help()`      | Display the help window.       |
| `destroy()`   | **Destroy your computer!**     |

| Item      | Value |
| --------- | -----:|
| Computer  | $1600 |
| Phone     |   $12 |
| Pipe      |    $1 |

| Left-Aligned  | Center Aligned  | Right Aligned |
| :------------ |:---------------:| -----:|
| col 3 is      | some wordy text | $1600 |
| col 2 is      | centered        |   $12 |
| zebra stripes | are neat        |    $1 |
                
----

####HTML entities

&copy; &  &uml; &trade; &iexcl; &pound;
&amp; &lt; &gt; &yen; &euro; &reg; &plusmn; &para; &sect; &brvbar; &macr; &laquo; &middot; 

X&sup2; Y&sup3; &frac34; &frac14;  &times;  &divide;   &raquo;

18&ordm;C  &quot;  &apos;

##Escaping for Special Characters

\*literal asterisks\*

##Markdown extras

###GFM task list

- [x] GFM task list 1
- [x] GFM task list 2
- [ ] GFM task list 3
    - [ ] GFM task list 3-1
    - [ ] GFM task list 3-2
    - [ ] GFM task list 3-3
- [ ] GFM task list 4
    - [ ] GFM task list 4-1
    - [ ] GFM task list 4-2

###Emoji mixed :smiley:

> Blockquotes :star:

####GFM task lists & Emoji & fontAwesome icon emoji & editormd logo emoji :editormd-logo-5x:

- [x] :smiley: @mentions, :smiley: #refs, [links](), **formatting**, and <del>tags</del> supported :editormd-logo:;
- [x] list syntax required (any unordered or ordered list supported) :editormd-logo-3x:;
- [x] [ ] :smiley: this is a complete item :smiley:;
- [ ] []this is an incomplete item [test link](#) :fa-star: @pandao; 
- [ ] [ ]this is an incomplete item :fa-star: :fa-gear:;
    - [ ] :smiley: this is an incomplete item [test link](#) :fa-star: :fa-gear:;
    - [ ] :smiley: this is  :fa-star: :fa-gear: an incomplete item [test link](#);
            
###TeX(LaTeX)
   
$$E=mc^2$$

Inline $$E=mc^2$$ Inline，Inline $$E=mc^2$$ Inline。

$$\(\sqrt{3x-1}+(1+x)^2\)$$
                    
$$\sin(\alpha)^{\theta}=\sum_{i=0}^{n}(x^i + \cos(f))$$
                
###FlowChart

```flow
st=>start: Login
op=>operation: Login operation
cond=>condition: Successful Yes or No?
e=>end: To admin

st->op->cond
cond(yes)->e
cond(no)->op
```

###Sequence Diagram
                    
```seq
Andrew->China: Says Hello 
Note right of China: China thinks\nabout it 
China-->Andrew: How are you? 
Andrew->>China: I am good thanks!
```

###End
