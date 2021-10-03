## Purpose:

To create a neural network using tensorflow and keras libraries to identify a traffic sign from its photograph.

## Experimentation Process:

I started with the base neural network that was found in the CS50AI Lecture 5 notes, which consisted of
- 1 Convolutional Layer(32 filters, 3x3 kernel)
- 1 MaxPool layer, using a 2x2 pool size
- 1 Dense layer, with 128 nodes
- 1 Dropout layer, with 0.5 
- 1 output layer!

I noted that on the smaller test set, this network worked without a hitch, but when tested on the actual
data set, the accuracy was low and the loss was high. 

I set out to research better designs for image classification, and came up with many structures:

I experimented with:
- creating multiple layers(i.e., 3 iterations of Conv2D, maxpool, and dropout)
- increasing and decreasing dropout rates to find robust vs. accuracy tradeoff
- creating multiple dense layers

I learned quite a bit here:
- I determined that the multilayer system was somewhat accurate, but had big tradeoffs: more layers decreased accuracy and increased loss, no matter how low I set dropout! 
- dropout is finnicky, and often to increase accuracy using lower dropouts multiple times is better than using high dropouts once
- multiple dense layers can result in overfitting, and also don't offer much benefit overall making them not as necessary

## Final Product:

- 1 layer consisting of:
    - 1 Conv2D layer(32 filters, 3x3 kernel)
    - 1 MaxPool layer, using 2x2 pool size
    - 1 Dropout layer, with 0.3 dropout
- 2nd layer consisting of:
    - 1 Conv2D layer(64 filters, 3x3 kernel)
    - 1 MaxPool layer, using 2x2 pool size
    - 1 Dropout layer, with 0.3 dropout
- 3rd layer consisting of:
    - 1 Dense layer, with 128 nodes
    - 1 Output layer

Of all the formats tested, I found this to be the most robust as well as with considerable accuracy and limited loss

## Thoughts:

This was one of the most fun labs to date as it had a bunch of learning involved. I ended up scouring the internet to determine good image models, and drew from more than 5 sources to learn TensorFlow, Keras, and good model design!






