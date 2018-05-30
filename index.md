## Brick

Brick is a programming language able to create blockchains to store data. We create the structure, you determine its application. In Brick, it will be possible to create blockchains, add blocks, mining, and running a node. 

A blockchain is a chain of blocks that contains information. The most important part of the blockchain is that it cannot be backdated or tempered. They have an interesting property, once a data is recorded inside a blockchain is really difficult to change it. Each block contains some data, the hash of the block and the hash of the previous block. Hash are very useful when you want to detach changes to blocks. Blockchains have 3 properties that make them really secure: proof of work (delay to make a change and add a new block), the structure where every block have a reference to the previous block, and that are connected to a P2P network to make them distributed and to verify the blockchain.

Blockchains are becoming very popular lately because of Bitcoin. Cryptocurrency is only a small application of blockchains. In the future blockchains that manage and verify online data can enable us to run companies that are entirely run by algorithms, making self drive cars safer and securing our online identity. The blockchains applications are countless and if we make blockchains more accessible, more people and companies will start using it. 


### Documentation

Brick was designed with simplicity and ease of use in mind.To create your first blockchain write the following line

`blockchain MyBlock = (param1:str, param2:int)`

Voila! Your first blockchain has been created. This blockchain will store a string and an integer. You can create a blockchain with as many parameters as you want. Currently strings and integers are supported. 

Once your blockchain has been initialized, it's now time to add data to it. 

`add MyBlock = (param1:"First time!",param2:25)`

There you go, that easy. The datatype used **must** match the one used when initialized. Consistency is important! Also, very important to understand that this IS NOT A BLOCK. A block contains many of these (what I like to call) _pebbles_, or not, it's up to you.

So you've acummulated enough pebbles, now it's time to mine a block. Even easier.

`mine MyBlock`

MyBlock has been mined. Yeah. Currently the proof of work difficulty is pretty low so it's quick.

So now you're interested on seeing the complete blockchain, simple:

`print MyBlock`

Boom there you go. Printed in its entirety. 

Oh you wanted a file? You didn't want to see it in the console? Good thing this command exists:

`export MyBlock`

A neat json file has been created in your project directory. Huh. Endless possibilities right? Share that blockchain, print the blockchain and hang it on the wall. I don't care, it's your file. Do whatever you want with it.

A very important aspect of the blockchain is missing, decentralization right? Well, Brick kind of has it.

`run MyBlock`

With this command, your blockchain is now hosted in your computer for your local network. People on your network can use your address to see the current blockchain:

http://192.168.1.1/ - Gives the current blockchain

http://192.168.1.1/current - Gives the data that is waiting for a block to be mined

http://192.168.1.1/mine - Mines a block in the blockchain

http://192.168.1.1/data/new - Using Postman, send a json block with the required info for the blockchain to be added to the list

This is a preview of what is to come. Brick should in the future, permit users to connect peer-to-peer and mantain a proper blockchain. The groundwork is there. 



### Video

If that nifty guide wasn't clear enough, here is a video showing you how to install and use Brick.

https://www.youtube.com/watch?v=hQ2JYAa1zTY&feature=youtu.be

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
